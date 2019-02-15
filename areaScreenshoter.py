import sys
from PIL import Image, ImageTk
from pynput.mouse import Listener as MouseListener
from pynput.mouse import Button as MouseButton
from threading import Thread

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *


class AreaScreenshoter:
    def create_window(self, img):
        # Create window root
        root = Tk()
        w = Label(root)
        root.overrideredirect(True)
        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        root.bind('<Escape>', lambda e: root.destroy())
        # root.after(1, lambda: root.focus_force())
        root.lift()
        root.attributes("-topmost", True)
        root.focus_force()

        photo = ImageTk.PhotoImage(img)
        cv = Canvas()
        cv.pack(side='top', fill='both', expand='yes')
        cv.create_image(10,  10, image=photo, anchor='nw')

        w.pack()

        root.mainloop()

    def open_window(self):
        pass

    def close_window(self):
        pass

    # Attaches a mouse listener to get select area and returns coordinates
    def select_area(self):
        def on_mouse_click(x, y, button, pressed):
            nonlocal press_coordinates
            nonlocal release_coordinates
            # If button were pressed
            if button == MouseButton.left:
                if pressed:
                    print("Left button pressed")
                    press_coordinates = {'detected': True, 'button': button, 'event': 'pressed', 'x': x, 'y': y}
                # If button were released
                else:
                    print("Left button released")
                    release_coordinates = {'detected': True, 'button': button, 'event': 'released', 'x': x, 'y': y}
                    # Stop listening on button release
                    return False
            # Cancel snapping if mouse right button clicked
            elif button == MouseButton.right:
                print("Right button pressed - listening canceled")
                press_coordinates = {'detected': False}
                release_coordinates = {'detected': False}
                # Stop listening
                return False

        # initialize local coordinates containers
        press_coordinates = {}
        release_coordinates = {}

        # Selected area coordinates getter
        print("Selecting area")
        with MouseListener(
                on_click=on_mouse_click) as listener:
            listener.join()

        # assign coordinates to object variables
        self.press_coordinates = press_coordinates
        self.release_coordinates = release_coordinates

        # if snapping has not been cancelled
        if press_coordinates['detected'] and release_coordinates['detected']:
            try:
                print("Press: ", press_coordinates['x'], press_coordinates['y'])
                print("Release: ", release_coordinates['x'], release_coordinates['y'])
            except Exception as ex:
                print(ex)

    def take_screenshot_of_area(self):
        # Take screenshot of area
        print("Taking screenshot")
        pass

    def __init__(self):
        # Create window

        # Coordinates of mouse press and release. It stands for coordinates of selected rectange area.
        self.press_coordinates = {}
        self.release_coordinates = {}


screenshoter_window = AreaScreenshoter()
