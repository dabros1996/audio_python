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

keyboard_controller = Controller()
input_lock = Lock()
last_input_time = 0
INPUT_DELAY = 0.3  # 300ms delay between inputs
is_playing = False  # Track play state

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def clear_console():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu(mute_hotkey, play_pause_hotkey, next_track_hotkey, prev_track_hotkey, quit_hotkey):
    """Display the menu options."""
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
    """Check if enough time has passed since last input."""
    global last_input_time
    current_time = time.time()
    if current_time - last_input_time >= INPUT_DELAY:
        last_input_time = current_time
        return True
    return False

def notify(message):
    """Show a non-modal notification."""
    with input_lock:
        print(f"\n{message}")
        time.sleep(0.5)  # Give time for the message to be visible
        display_menu(mute_hotkey, play_pause_hotkey, next_track_hotkey, prev_track_hotkey, quit_hotkey)

def toggle_mute():
    """Mute or unmute audio with notification."""
    if not can_accept_input():
        return
        
    CoInitialize()
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        current_mute_state = volume.GetMute()
        volume.SetMute(not current_mute_state, None)
        notify("Audio: " + ("Muted" if not current_mute_state else "Unmuted"))
    except Exception as e:
        notify(f"Error: {str(e)}")
    finally:
        CoUninitialize()

def play_pause():
    """Toggle play/pause for media."""
    if not can_accept_input():
        return
        
    global is_playing
    is_playing = not is_playing
    keyboard_controller.press(Key.media_play_pause)
    keyboard_controller.release(Key.media_play_pause)
    notify(f"Media: {'Playing' if is_playing else 'Paused'}")

def next_track():
    """Switch to next track."""
    if not can_accept_input():
        return
        
    keyboard_controller.press(Key.media_next)
    keyboard_controller.release(Key.media_next)
    notify("Media: Next Track")

def previous_track():
    """Switch to previous track."""
    if not can_accept_input():
        return
        
    keyboard_controller.press(Key.media_previous)
    keyboard_controller.release(Key.media_previous)
    notify("Media: Previous Track")

def on_mute_hotkey():
    """Handler for mute hotkey."""
    toggle_mute()

def on_quit_hotkey(signum=None, frame=None):
    """Handler for quit signal with cleanup."""
    print("\nSkrypt przerwany przez Ctrl + Alt + Q.")
    keyboard.unhook_all()  # Cleanup keyboard hooks
    sys.exit(0)

# Define hotkeys at module level for access in notify function
mute_hotkey = "ctrl+alt+m"
quit_hotkey = "ctrl+alt+q"
play_pause_hotkey = "ctrl+alt+p"
next_track_hotkey = "ctrl+alt+right"
prev_track_hotkey = "ctrl+alt+left"

def main():
    if not is_admin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    try:
        # Register hotkeys
        keyboard.add_hotkey(mute_hotkey, on_mute_hotkey)
        keyboard.add_hotkey(quit_hotkey, lambda: signal.raise_signal(signal.SIGINT))
        keyboard.add_hotkey(play_pause_hotkey, play_pause)
        keyboard.add_hotkey(next_track_hotkey, next_track)
        keyboard.add_hotkey(prev_track_hotkey, previous_track)

        # Handle SIGINT
        signal.signal(signal.SIGINT, on_quit_hotkey)

        # Show initial menu
        display_menu(mute_hotkey, play_pause_hotkey, next_track_hotkey, prev_track_hotkey, quit_hotkey)
        
        # Keep the script running
        keyboard.wait()
    except Exception as e:
        notify(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()