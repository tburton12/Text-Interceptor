import configparser
from pynput.keyboard import Key
import os.path


class Settings:
    @staticmethod
    def __generate_config_file():
        print("Creating conf.ini")
        config_file = open("conf.ini", "w")
        try:
            config = configparser.ConfigParser()
            config.add_section('Control')
            config.set('Control', 'Capture Key', str(Key.f8))
            config.write(config_file)
        except Exception as ex:
            print(ex)
        finally:
            config_file.close()

    def __init__(self):
        # Generate conf file if it is not existing
        if os.path.isfile("conf.ini") is not True:
            self.__generate_config_file()

        self.conf = configparser.ConfigParser()
        self.conf.read("conf.ini")

        try:
            self.capture_action_key = self.conf.get('Control', 'Capture Key')
        except Exception as ex:
            print(ex)
            # Assign default action key
            self.capture_action_key = Key.f8


program_settings = Settings()
