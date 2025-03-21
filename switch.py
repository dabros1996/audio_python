import keyboard
import signal
import sys
import win32api
import win32con
import win32com.client
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

def change_audio_output():
    """Zmienia domyślne urządzenie audio."""
    CoInitialize()
    try:
        devices = AudioUtilities.GetSpeakers()
        current_default_id = devices.GetId()
        enumerator = AudioUtilities.GetDeviceEnumerator()
        device_collection = enumerator.EnumAudioEndpoints(0, 1) # 0 = render, 1 = all states
        device_count = device_collection.GetCount()
        for i in range(device_count):
            device = device_collection.Item(i)
            if device.GetId() != current_default_id:
                policy_config = win32com.client.CreateObject("PolicyConfig.CPolicyConfigClient")
                policy_config.SetDefaultEndpoint(device.GetId(), 0) # 0 = eConsole
                print(f"Zmieniono domyślne urządzenie audio na: {device.GetFriendlyName()}")
                break
    except Exception as e:
        print(f"Błąd zmiany urządzenia audio: {e}")
    finally:
        CoUninitialize()

def on_output_hotkey():
    """Funkcja wywoływana po naciśnięciu skrótu klawiszowego zmiany wyjścia audio."""
    change_audio_output()

# Ustaw skróty klawiszowe
mute_hotkey = "ctrl+alt+m"
quit_hotkey = "ctrl+alt+q"
output_hotkey = "ctrl+alt+o"

# Zarejestruj skróty klawiszowe
keyboard.add_hotkey(mute_hotkey, on_mute_hotkey)
keyboard.add_hotkey(quit_hotkey, lambda: signal.raise_signal(signal.SIGINT))
keyboard.add_hotkey(output_hotkey, on_output_hotkey)

# Obsługa sygnału SIGINT
signal.signal(signal.SIGINT, on_quit_hotkey)

# Wyświetl informacje o opcjach
print("Dostępne opcje:")
print(f"- {mute_hotkey}: Mutuj/odmutuj dźwięk")
print(f"- {output_hotkey}: Zmień wyjście audio")
print(f"- {quit_hotkey}: Zakończ skrypt")

# Uruchom pętlę, aby skrypt działał w tle
keyboard.wait()