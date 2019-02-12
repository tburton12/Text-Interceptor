from getTextFromScreen import attach_listener
import trayIcon
from threading import Thread


def main():

    # Create program handler
    listener = Thread(target=attach_listener)
    listener.setDaemon(True)
    listener.start()

    # Create tray icon
    icon = trayIcon.TrayIcon(title='Text capture')
    icon.run_icon()


main()
