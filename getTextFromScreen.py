from pynput.keyboard import Listener as KeyboardListener
from settings import program_settings
from areaScreenshoter import screenshoter_window
import pyperclip
from PIL import Image as PILImage
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

# Prevent from incorrect cropping of screenshots on high-DPI displays.
# It has to be called before pyscreenhot is imported
from ctypes import windll
user32 = windll.user32
user32.SetProcessDPIAware()
import pyscreenshot as ImageGrab


def copy_text_from_screen():
    # Take screenshot of current display
    display_screenshot = ImageGrab.grab()

    # Create and open window which print screenshot on fullscreen
    screenshoter_window.start_window_process(display_screenshot)

    screenshoter_window.select_area()

    area_screenshot = None
    if screenshoter_window.is_window_opened():
        area_screenshot = screenshoter_window.take_screenshot_of_area()

    screenshoter_window.close_window()

    # Get and copy text from screen
    if area_screenshot is not None:
        # Detect text from screenshot
        detected_text = pytesseract.image_to_string(area_screenshot)
        print("Detected text: ", detected_text)
        # Copy detected text o clipboard
        pyperclip.copy(detected_text)


def on_keyboard_press(key):
    print(str(key), " : ", program_settings.capture_action_key)
    if str(key) == program_settings.capture_action_key:
        print(key, " pressed")
        copy_text_from_screen()


def attach_listener():
    # Detects key presses
    print("Key listener attached")
    with KeyboardListener(
            on_press=on_keyboard_press
            ) as listener:
        listener.join()
