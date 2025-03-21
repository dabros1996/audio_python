import keyboard
import signal
import sys
from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def toggle_mute():
    """Mutuje lub odmutowuje dźwięk."""
    CoInitialize()
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        current_mute_state = volume.GetMute()
        volume.SetMute(not current_mute_state, None)
    finally:
        CoUninitialize()

def on_mute_hotkey():
    """Funkcja wywoływana po naciśnięciu skrótu klawiszowego mutowania."""
    toggle_mute()

def on_quit_hotkey(signum, frame):
    """Funkcja obsługująca sygnał Ctrl + Alt + Q."""
    print("Skrypt przerwany przez Ctrl + Alt + Q.")
    sys.exit(0)

# Ustaw skróty klawiszowe
mute_hotkey = "ctrl+alt+m"
quit_hotkey = "ctrl+alt+q"

# Zarejestruj skróty klawiszowe
keyboard.add_hotkey(mute_hotkey, on_mute_hotkey)
keyboard.add_hotkey(quit_hotkey, lambda: signal.raise_signal(signal.SIGINT))

# Obsługa sygnału SIGINT
signal.signal(signal.SIGINT, on_quit_hotkey)

# Wyświetl informacje o opcjach
print("Dostępne opcje:")
print(f"- {mute_hotkey}: Mutuj/odmutuj dźwięk")
print(f"- {quit_hotkey}: Zakończ skrypt")

# Uruchom pętlę, aby skrypt działał w tle
keyboard.wait()