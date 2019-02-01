from pynput.keyboard import Listener
from settings import program_settings


def on_press(key):
    if str(key) == program_settings.capture_action_key:
        print(key, " pressed")


def attach_listener():
    # Detects key presses
    with Listener(
            on_press=on_press
            ) as listener:
        listener.join()
