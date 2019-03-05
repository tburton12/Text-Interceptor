from textInterceptor import attach_listener
import trayIcon
from threading import Thread
from multiprocessing import freeze_support


if __name__ == '__main__':
    freeze_support()

    # Attach keyboard listener to make program works parallel
    listener = Thread(target=attach_listener)
    listener.setDaemon(True)
    listener.start()

    # Create tray icon
    icon = trayIcon.TrayIcon()
    icon.run_icon()
