import pystray
from PIL import Image, ImageDraw


class TrayIcon:
    def open_window(self):
        print("Open window")
        pass

    def capture_text(self):
        print("Capture text")
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

    def __init__(self, title='Python', image=None):
        self.running = False
        self.visible = False

        # Create icon
        self.icon = pystray.Icon(name=title, icon=title, title=title)

        # Use provided image as icon or generate default one
        if image is not None:
            try:
                self.icon.icon = image
            except Exception as e:
                print(e)
                self.icon.icon = image
        else:
            self.icon.icon = generate_icon()

        # Add entries to 'right click' menu
        self.icon.menu = pystray.Menu(pystray.MenuItem(text="Open", action=lambda: self.open_window(), default=True),
                                      pystray.MenuItem(text="Capture text", action=lambda: self.capture_text()),
                                      pystray.MenuItem(text="Exit", action=lambda: self.exit_program()))


def generate_icon(width=16, height=16, color1=20, color2=400):
    # Generate an image
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)

    return image
