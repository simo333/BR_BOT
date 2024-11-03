from datetime import datetime

import pyautogui

import alarm.AlarmUtil
import json
from userinput import UserInputController
from userinput import Combat
from userinput.UserInputController import MouseActions

with open('config.json', 'r') as file:
    config = json.load(file)

with open(config['tacticSource'], 'r') as file:
    mobData = json.load(file)

controller = UserInputController
combat = Combat.Combat(mobData, config)


def enterEasyV2():
    print(f'{datetime.now()}: Entering first instance of V2')
    controller.mouseAction(MouseActions.RIGHT, 'images/level0/entranceToInstance.png', movementDuration=0.3)
    if not controller.wait_for_image('images/level0/easyV2Option.png', 3):
        pyautogui.moveTo(300, 300)
        enterEasyV2()
    controller.mouseAction(MouseActions.HOLD_DOWN, 'images/level0/easyV2Option.png')
    if not controller.check_if_target_on_list('images/fight/czujkaOnN.png'):
        enterEasyV2()


def enterSecondLevel():
    print(f'{datetime.now()}: Entering second instance')
    controller.mouseAction(MouseActions.RIGHT, 'images/level1/entranceToLevel2.png')
    if controller.wait_for_image('images/fight/bossOnN.png'):
        return
    else:
        enterSecondLevel()


def enterThirdLevel():
    print(f'{datetime.now()}: Entering third instance')
    controller.mouseAction(MouseActions.RIGHT, 'images/level2/entranceToLevel3.png')
    if controller.wait_for_image('images/fight/bossOnN.png'):
        combat.rest(config['restingTimeAfter2ndInstance'])
        return
    else:
        enterThirdLevel()


def enterFourthLevel():
    print(f'{datetime.now()}: Entering fourth instance')
    controller.mouseAction(MouseActions.RIGHT, 'images/level3/entranceToLevel4.png')
    if controller.wait_for_image('images/fight/bossOnN.png'):
        return
    else:
        enterFourthLevel()


def quitInstance():
    controller.mouseAction(MouseActions.RIGHT, 'images/level4/quit.png')
    pyautogui.sleep(5)
    if not controller.wait_for_image('images/level0/entranceToInstance.png'):
        quitInstance()
        return
    combat.rest(config['restingTimeAfterFinalBoss'])


pyautogui.sleep(2)
print("START")


# V2 FLOW
def hunting_V2():
    pyautogui.moveTo(pyautogui.size().width - 1, pyautogui.size().height * 0.1)  #move mouse to right top area
    controller.pressWithActiveWindow('n')  # show mob list
    for i in range(config['repeats']):
        enterEasyV2()
        alarm.AlarmUtil.alarmChecker(config)
        combat.killMob('Sensor1', 20)
        alarm.AlarmUtil.alarmChecker(config)
        enterSecondLevel()
        alarm.AlarmUtil.alarmChecker(config)
        combat.killMob('Boss1', True)
        alarm.AlarmUtil.alarmChecker(config)
        combat.killMob('Sensor2', 20)
        alarm.AlarmUtil.alarmChecker(config)
        enterThirdLevel()
        alarm.AlarmUtil.alarmChecker(config)
        combat.killMob('Boss2', True)
        alarm.AlarmUtil.alarmChecker(config)
        combat.killMob('Sensor3', 20)
        alarm.AlarmUtil.alarmChecker(config)
        enterFourthLevel()
        alarm.AlarmUtil.alarmChecker(config)
        combat.killMob('V2', True)
        alarm.AlarmUtil.alarmChecker(config)
        quitInstance()
        alarm.AlarmUtil.alarmChecker(config)
        if i == config['repeats']:
            alarm.AlarmUtil.alarmWhenFinishRepeats(config)
        Combat.checkIfBagIsAlmostFull()


hunting_V2()
