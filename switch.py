# Importy niezbędnych bibliotek
# keyboard - obsługa globalnych skrótów klawiszowych
# signal - obsługa sygnałów systemowych (np. do zamykania programu)
# ctypes - interfejs do funkcji Windows API
# pycaw - kontrola dźwięku w systemie Windows
# pynput - symulacja klawiszy multimedialnych
import keyboard
import signal
import sys
import ctypes
import os
import time
from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import wintypes
from pynput.keyboard import Key, Controller
import os
from threading import Lock

# Inicjalizacja kontrolera klawiatury do symulacji klawiszy multimedialnych
keyboard_controller = Controller()
# Blokada wątku do synchronizacji dostępu do współdzielonych zasobów
input_lock = Lock()
# Zmienne do kontroli częstotliwości wejść użytkownika
last_input_time = 0
INPUT_DELAY = 0.3  # 300ms opóźnienia między wejściami
# Stan odtwarzania (playing/paused)
is_playing = False

def is_admin():
    """Sprawdza czy skrypt ma uprawnienia administratora.
    Jest to wymagane do kontroli dźwięku systemowego."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def clear_console():
    """Czyści ekran konsoli.
    Używa odpowiedniej komendy w zależności od systemu operacyjnego."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu(mute_hotkey, play_pause_hotkey, next_track_hotkey, prev_track_hotkey, quit_hotkey):
    """Wyświetla menu z dostępnymi opcjami i aktualnym stanem.
    
    Args:
        mute_hotkey: Skrót do wyciszania
        play_pause_hotkey: Skrót do play/pause
        next_track_hotkey: Skrót do następnego utworu
        prev_track_hotkey: Skrót do poprzedniego utworu
        quit_hotkey: Skrót do wyjścia
    """
    clear_console()
    print("\n=== Audio Control Menu ===")
    print(f"- {mute_hotkey}: Mutuj/odmutuj dźwięk")
    print(f"- {play_pause_hotkey}: Play/Pause (Current state: {'Playing' if is_playing else 'Paused'})")
    print(f"- {next_track_hotkey}: Następny utwór")
    print(f"- {prev_track_hotkey}: Poprzedni utwór")
    print(f"- {quit_hotkey}: Zakończ skrypt")
    print("\nStatus: Running...")
    print("=" * 23)

def can_accept_input():
    """Sprawdza czy minął wystarczający czas od ostatniego wejścia.
    Zapobiega to przypadkowemu podwójnemu wciśnięciu klawiszy.
    
    Returns:
        bool: True jeśli można przyjąć nowe wejście, False w przeciwnym razie
    """
    global last_input_time
    current_time = time.time()
    if current_time - last_input_time >= INPUT_DELAY:
        last_input_time = current_time
        return True
    return False

def notify(message):
    """Wyświetla powiadomienie w konsoli i odświeża menu.
    
    Args:
        message: Tekst powiadomienia do wyświetlenia
    """
    with input_lock:
        print(f"\n{message}")
        time.sleep(0.5)  # Krótkie opóźnienie dla widoczności powiadomienia
        display_menu(mute_hotkey, play_pause_hotkey, next_track_hotkey, prev_track_hotkey, quit_hotkey)

def toggle_mute():
    """Przełącza stan wyciszenia dźwięku systemowego.
    Używa biblioteki pycaw do kontroli głośności Windows."""
    if not can_accept_input():
        return
        
    CoInitialize()  # Inicjalizacja COM dla Windows Audio
    try:
        # Pobieranie interfejsu głośników systemowych
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        # Pobranie i zmiana stanu wyciszenia
        current_mute_state = volume.GetMute()
        volume.SetMute(not current_mute_state, None)
        notify("Audio: " + ("Muted" if not current_mute_state else "Unmuted"))
    except Exception as e:
        notify(f"Error: {str(e)}")
    finally:
        CoUninitialize()  # Zwolnienie zasobów COM

def play_pause():
    """Przełącza odtwarzanie/pauzę poprzez symulację klawisza multimedialnego."""
    if not can_accept_input():
        return
        
    global is_playing
    is_playing = not is_playing
    # Symulacja wciśnięcia klawisza play/pause
    keyboard_controller.press(Key.media_play_pause)
    keyboard_controller.release(Key.media_play_pause)
    notify(f"Media: {'Playing' if is_playing else 'Paused'}")

def next_track():
    """Przełącza na następny utwór poprzez symulację klawisza multimedialnego."""
    if not can_accept_input():
        return
        
    keyboard_controller.press(Key.media_next)
    keyboard_controller.release(Key.media_next)
    notify("Media: Next Track")

def previous_track():
    """Przełącza na poprzedni utwór poprzez symulację klawisza multimedialnego."""
    if not can_accept_input():
        return
        
    keyboard_controller.press(Key.media_previous)
    keyboard_controller.release(Key.media_previous)
    notify("Media: Previous Track")

def on_mute_hotkey():
    """Obsługuje zdarzenie wciśnięcia skrótu do wyciszenia."""
    toggle_mute()

def on_quit_hotkey(signum=None, frame=None):
    """Obsługuje zdarzenie wciśnięcia skrótu do wyjścia.
    Czyści zarejestrowane skróty przed zamknięciem."""
    print("\nSkrypt przerwany przez Ctrl + Alt + Q.")
    keyboard.unhook_all()
    sys.exit(0)

# Definicja skrótów klawiszowych
mute_hotkey = "ctrl+alt+m"
quit_hotkey = "ctrl+alt+q"
play_pause_hotkey = "ctrl+alt+p"
next_track_hotkey = "ctrl+alt+right"
prev_track_hotkey = "ctrl+alt+left"

def main():
    """Główna funkcja programu."""
    # Sprawdzenie i żądanie uprawnień administratora
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    try:
        # Rejestracja skrótów klawiszowych
        keyboard.add_hotkey(mute_hotkey, on_mute_hotkey)
        keyboard.add_hotkey(quit_hotkey, lambda: signal.raise_signal(signal.SIGINT))
        keyboard.add_hotkey(play_pause_hotkey, play_pause)
        keyboard.add_hotkey(next_track_hotkey, next_track)
        keyboard.add_hotkey(prev_track_hotkey, previous_track)

        # Obsługa sygnału przerwania (Ctrl+C)
        signal.signal(signal.SIGINT, on_quit_hotkey)

        # Wyświetlenie początkowego menu
        display_menu(mute_hotkey, play_pause_hotkey, next_track_hotkey, prev_track_hotkey, quit_hotkey)
        
        # Oczekiwanie na zdarzenia klawiatury
        keyboard.wait()
    except Exception as e:
        notify(f"Error: {str(e)}")
        sys.exit(1)

# Punkt wejścia programu
if __name__ == "__main__":
    main()