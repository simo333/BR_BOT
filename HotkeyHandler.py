import json

import keyboard
import threading
import time


class HotkeyHandler:

    def __init__(self):
        with open('config.json', 'r') as file:
            json_data = file.read()
        self.hotkeys = json.loads(json_data).get("hotkeys", {})
        self.start_listener()

    def start_listener(self):
        # Create a separate thread for the hotkey listener
        hotkey_thread = threading.Thread(target=self.hotkey_listener)

        # Start the thread
        hotkey_thread.start()

    def hotkey_listener(self):
        # Register the hotkey listener
        keyboard.add_hotkey(self.hotkeys.get("startStop"), self.startStopBot)
        keyboard.add_hotkey(self.hotkeys.get("pause"), self.pauseExcetion)

        # Keep the program running to listen for the hotkey
        keyboard.wait()

    def startStopBot(self):
        # This is the operation you want to run when the hotkey is pressed
        print("Hotkey pressed! Start/Stop")
        time.sleep(2)
        from EasyV2 import hunting_V2
        hunting_V2()

    def pauseExcetion(self):
        # This is the operation you want to run when the hotkey is pressed
        print("Hotkey pressed! Pause")
        time.sleep(2)

