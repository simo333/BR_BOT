import json

import pyautogui

from userinput import UserInputController
from userinput.Combat import Combat

controller = UserInputController
with open('config.json', 'r') as file:
    config = json.load(file)

with open(config['tacticSource'], 'r') as file:
    mobData = json.load(file)

pyautogui.sleep(2)
print("START")
# FireMob FLOW
combat = Combat(mobData, config)
for i in range(config['repeats']):
    combat.killMob('FireMob')
    if i % 4 == 0:
        controller.leftClick('images/fight/restIcon.png')
        pyautogui.sleep(10)

