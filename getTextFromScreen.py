from pynput.keyboard import Listener as KeyboardListener
from settings import program_settings
from areaScreenshoter import screenshoter_window
from PIL import Image
import pyscreenshot as ImageGrab


def get_text_from_screen():

    # Take screenshot of current display
    display_screenshot = ImageGrab.grab()
    display_screenshot.save('full_screenshot.png')

    # Create and open window which print screenshot on fullscreen
    screenshoter_window.open_window(display_screenshot)

    screenshoter_window.select_area()

    screenshoter_window.take_screenshot_of_area()

    screenshoter_window.close_window()


def on_keyboard_press(key):
    print(str(key), " : ", program_settings.capture_action_key)
    if str(key) == program_settings.capture_action_key:
        print(key, " pressed")
        get_text_from_screen()


def attach_listener():
    # Detects key presses
    print("Key listener attached")
    with KeyboardListener(
            on_press=on_keyboard_press
            ) as listener:
        listener.join()
