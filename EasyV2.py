from datetime import datetime

import pyautogui

import alarm.AlarmUtil
import json
from userinput import UserInputController
from userinput.Combat import Combat
from userinput.UserInputController import MouseActions

with open('config.json', 'r') as file:
    config = json.load(file)

with open(config['tacticSource'], 'r') as file:
    mobData = json.load(file)

controller = UserInputController
combat = Combat(mobData, config)


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
    if controller.wait_for_image('images/fight/round.png', 5):
        killSensorIfAttacked('Sensor1')
        enterSecondLevel()
        return
    if not controller.check_if_target_on_list('images/fight/czujkaOnN.png'):
        enterSecondLevel()


def enterThirdLevel():
    print(f'{datetime.now()}: Entering third instance')
    controller.mouseAction(MouseActions.RIGHT, 'images/level2/entranceToLevel3.png')
    if controller.wait_for_image('images/fight/round.png', 5):
        killSensorIfAttacked('Sensor2')
        enterThirdLevel()
        return
    if not controller.check_if_target_on_list('images/fight/czujkaOnN.png'):
        enterThirdLevel()
        return
    combat.rest(15)


def enterFourthLevel():
    print(f'{datetime.now()}: Entering fourth instance')
    controller.mouseAction(MouseActions.RIGHT, 'images/level3/entranceToLevel4.png')
    if controller.wait_for_image('images/fight/round.png', 5):
        killSensorIfAttacked('Sensor3')
        enterFourthLevel()
    if not controller.check_if_target_on_list('images/fight/bossOnN.png'):
        enterFourthLevel()


def killSensorIfAttacked(mobName: str):
    if config['takeActionVia'] == 'keyboard':
        controller.pressWithActiveWindow('2')
    else:
        controller.mouseAction(MouseActions.LEFT, 'images/fight/tacticTwo.png')
    controller.pressWithActiveWindow('space')
    combat.finishing_combat(mobName)
    pyautogui.sleep(0.5)
    controller.pressWithActiveWindow('esc')
    combat.rest(8)


def quitInstance():
    controller.mouseAction(MouseActions.RIGHT, 'images/level4/quit.png')
    pyautogui.sleep(5)
    if not controller.wait_for_image('images/level0/entranceToInstance.png'):
        quitInstance()
        return
    combat.rest(15)


def quitFromSecondLevel():
    controller.mouseAction(MouseActions.RIGHT, 'images/level4/quit.png')
    pyautogui.sleep(3)
    if not controller.wait_for_image('images/level0/entranceToInstance.png'):
        quitInstance()
        return


pyautogui.sleep(2)
print("START")


# V2 FLOW
def hunting_V2():
    for i in range(config['repeats']):
        enterEasyV2()
        alarm.AlarmUtil.alarmChecker(config)
        combat.killMob('Sensor1', 20)
        alarm.AlarmUtil.alarmChecker(config)
        enterSecondLevel()
        if not config['sensorsOnly']:
            alarm.AlarmUtil.alarmChecker(config)
            combat.killMob('Boss1')
            alarm.AlarmUtil.alarmChecker(config)
            combat.killMob('Sensor2', 20)
            alarm.AlarmUtil.alarmChecker(config)
            enterThirdLevel()
            alarm.AlarmUtil.alarmChecker(config)
            combat.killMob('Boss2')
            alarm.AlarmUtil.alarmChecker(config)
            combat.killMob('Sensor3', 20)
            alarm.AlarmUtil.alarmChecker(config)
            enterFourthLevel()
            alarm.AlarmUtil.alarmChecker(config)
            combat.killMob('V2')
            alarm.AlarmUtil.alarmChecker(config)
            quitInstance()
            alarm.AlarmUtil.alarmChecker(config)
        else:
            quitFromSecondLevel()
        if i == config['repeats']:
            alarm.AlarmUtil.alarmWhenFinishRepeats(config)


hunting_V2()
