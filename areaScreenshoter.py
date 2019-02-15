import sys
import pyscreenshot as ImageGrab
from PIL import Image, ImageTk
from pynput.mouse import Listener as MouseListener
from pynput.mouse import Button as MouseButton
from multiprocessing import Process

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *


# TODO: fix right click on opened window

class AreaScreenshoter:
    @staticmethod
    def run_window(img):
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

    def open_window(self, background_image):
        self.window_process = Process(target=self.run_window, args=(background_image,))
        self.window_process.daemon = True
        self.window_process.start()

        pass

    def close_window(self):
        self.window_process.terminate()
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
        x1, y1 = self.press_coordinates['x'], self.press_coordinates['y']
        x2, y2 = self.release_coordinates['x'], self.release_coordinates['y']
        print("Taking screenshot of: ", x1, y1, x2, y2)
        selected_area_screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        selected_area_screenshot.save("selected_area.png")
        pass

    def __init__(self):
        # Create window

        # Coordinates of mouse press and release. It stands for coordinates of selected rectange area.
        self.press_coordinates = {}
        self.release_coordinates = {}

        self.window_process = Process()


screenshoter_window = AreaScreenshoter()
