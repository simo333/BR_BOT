import alarm.AlarmUtil
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
    alarm.AlarmUtil.alarmChecker(config)
    combat.killMobAssist('Sensor1')
    alarm.AlarmUtil.alarmChecker(config)
    combat.killMobAssist('Sensor1')
    alarm.AlarmUtil.alarmChecker(config)
    combat.killMobAssist('Sensor1')
    alarm.AlarmUtil.alarmChecker(config)
    combat.killMobAssist('Boss1')
    alarm.AlarmUtil.alarmChecker(config)
    combat.killMobAssist('Sensor2')
    alarm.AlarmUtil.alarmChecker(config)
    combat.killMobAssist('Sensor2')
    alarm.AlarmUtil.alarmChecker(config)
    combat.killMobAssist('Boss2')
    alarm.AlarmUtil.alarmChecker(config)
    combat.killMobAssist('Sensor3')
    alarm.AlarmUtil.alarmChecker(config)
    combat.killMobAssist('Sensor3')
    alarm.AlarmUtil.alarmChecker(config)
    combat.killMobAssist('V2')
    alarm.AlarmUtil.alarmChecker(config)
    pyautogui.sleep(20)
