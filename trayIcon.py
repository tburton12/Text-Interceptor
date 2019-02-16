import pystray
from PIL import Image, ImageDraw
from getTextFromScreen import copy_text_from_screen
from settings import program_settings


class TrayIcon:
    @staticmethod
    def capture_text():
        print("Capture text")
        copy_text_from_screen()
        pass

    def exit_program(self):
        self.icon.stop()
        print("Exiting")
        self.running = False
        pass

    def __setup(self):
        self.visible = True

    def run_icon(self):
        # Create icon thread
        self.icon.run()
        self.running = True

    def __init__(self, title='Python'):
        self.running = False
        self.visible = False

        # Create icon
        self.icon = pystray.Icon(name=title, icon=title, title=title)

        # Use provided image as icon or generate default one
        try:
            image = Image.open('icon.ico')
        except IOError:
            print("Could not find icon file")
            image = None

        if image is not None:
            try:
                self.icon.icon = image
            except Exception as e:
                print(e)
                self.icon.icon = generate_icon()
        else:
            self.icon.icon = generate_icon()

        # Add entries to 'right click' menu
        self.icon.menu = pystray.Menu(pystray.MenuItem(text=program_settings.names['Program name'], action=lambda: None, default=True),
                                      pystray.MenuItem(text="Capture text", action=lambda: self.capture_text()),
                                      pystray.MenuItem(text="Exit", action=lambda: self.exit_program()))


def generate_icon(width=16, height=16, color1=20, color2=400):
    # Generate an image
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)

    return image
