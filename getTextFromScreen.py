from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from pynput.mouse import Button as MouseButton
from settings import program_settings
# import pyscreenshot


def on_mouse_click(x, y, button, pressed):
    global press_coordinates
    global release_coordinates

    # If button were pressed
    if button == MouseButton.left:
        if pressed:
            print("Left button pressed")
            press_coordinates = {'detected': True, 'button': button, 'event': 'pressed', 'x': x, 'y': y}
        # If button were released
        else:
            print("Left button released")
            release_coordinates = {'detected': True, 'button': button, 'event': 'released', 'x': x, 'y': y}
            # Stop listening
            return False
    # Cancel snapping if mouse right button clicked
    elif button == MouseButton.right:
        print("Right button pressed")
        press_coordinates = {'detected': False}
        release_coordinates = {'detected': False}
        # Stop listening
        return False


press_coordinates = {}
release_coordinates = {}


def take_screenshot():
    # screenshot = pyscreenshot.grab()

    print("Mouse listener attached")
    with MouseListener(
            on_click=on_mouse_click) as listener:
        listener.join()

        # if snapping has not been cancelled
        if press_coordinates['detected'] and release_coordinates['detected']:
            try:
                print("Press: ", press_coordinates['x'], press_coordinates['y'])
                print("Release: ", release_coordinates['x'], release_coordinates['y'])
            except:
                pass


def on_keyboard_press(key):
    print(str(key), " : ", program_settings.capture_action_key)
    if str(key) == program_settings.capture_action_key:
        print(key, " pressed")
        take_screenshot()


def attach_listener():
    # Detects key presses
    print("Key listener attached")
    with KeyboardListener(
            on_press=on_keyboard_press
            ) as listener:
        listener.join()
