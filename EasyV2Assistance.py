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
# V2 FLOW
combat = Combat(mobData, config)
for i in range(config['repeats']):
    combat.killMobAssist('Sensor1')
    combat.killMobAssist('Sensor1')
    combat.killMobAssist('Sensor1')
    combat.killMobAssist('Sensor1')
    combat.killMobAssist('Boss1')
    combat.killMobAssist('Sensor2')
    combat.killMobAssist('Sensor2')
    combat.killMobAssist('Boss2')
    combat.killMobAssist('Sensor3')
    combat.killMobAssist('Sensor3')
    combat.killMobAssist('V2')
    pyautogui.sleep(20)
