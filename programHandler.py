from getTextFromScreen import attach_listener
import trayIcon
from threading import Thread


def main():

    # Create program handler
    get_text_from_screen_handler = Thread(target=attach_listener)
    get_text_from_screen_handler.setDaemon(True)
    get_text_from_screen_handler.start()

    # Create tray icon
    icon = trayIcon.TrayIcon(title='Text capture')
    icon.run_icon()


main()
