import json
import alarm.AlarmUtil
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
    alarm.AlarmUtil.alarmChecker(config)
    if i % 4 == 0:
        combat.rest(8)

