import sys
import pyscreenshot as ImageGrab
from PIL import ImageTk
from pynput.mouse import Listener as MouseListener
from pynput.mouse import Button as MouseButton
from multiprocessing import Process

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *


class AreaScreenshoter:
    @staticmethod
    def run_window(img):
        """
        Create fullscreen window and print image given in param
        :param img: Image to be printed in window
        :return:
        """
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
        cv.create_image(1,  1, image=photo, anchor='nw')

        w.pack()
        root.mainloop()

    def start_window_process(self, background_image):
        self.window_process = Process(target=self.run_window, args=(background_image,))
        self.window_process.daemon = True
        self.window_process.start()

    def close_window(self):
        if self.window_process.is_alive():
            self.window_process.terminate()

    def is_window_opened(self):
        return self.window_process.is_alive()

    def select_area(self):
        """
        Attach mouse listener to select area
        :return: Coordinates of selected area or False if selecting were interrupted
        """
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
            # Cancel snapping if right mouse button clicked
            elif button == MouseButton.right:
                print("Right button pressed - listening canceled")
                press_coordinates = {'detected': False}
                release_coordinates = {'detected': False}
                # Stop listening
                return False

        # Initialize local coordinates containers
        press_coordinates = {'detected': False}
        release_coordinates = {'detected': False}

        # Get coordinates of selected area
        print("Selecting area")
        with MouseListener(
                on_click=on_mouse_click) as listener:
            listener.join()

        # Assign coordinates to objects variables
        self.press_coordinates = press_coordinates
        self.release_coordinates = release_coordinates

        # Print detected area coordinates
        if press_coordinates['detected'] and release_coordinates['detected']:
            try:
                print("Press: ", press_coordinates['x'], press_coordinates['y'])
                print("Release: ", release_coordinates['x'], release_coordinates['y'])
            except Exception as ex:
                print(ex)

    def take_screenshot_of_area(self):
        # Take screenshot of area
        """
        Take screenshot of previously selected area.
        Coordinates are specified in object variables
        :return: Screenshot of selected area or None if could not take screenshot
        """
        selected_area_screenshot = None

        if self.press_coordinates['detected'] and self.release_coordinates['detected']:
            x1, y1 = self.press_coordinates['x'], self.press_coordinates['y']
            x2, y2 = self.release_coordinates['x'], self.release_coordinates['y']

            print("Taking screenshot of: ", x1, y1, x2, y2)
            try:
                selected_area_screenshot = ImageGrab.grab(bbox=(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))
            except Exception as ex:
                print(ex)
        else:
            print("Cannot take a screenshot without coordinates")

        return selected_area_screenshot

    def __init__(self):
        # Coordinates of mouse press and release. It stands for coordinates of selected rectangle area.
        self.press_coordinates = {}
        self.release_coordinates = {}

        # Initialize variable to store screenshoter window process
        self.window_process = Process()


screenshoter_window = AreaScreenshoter()
