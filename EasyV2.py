
from datetime import datetime

import cv2

import json

import pyautogui

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


def enterSecondLevel():
    print(f'{datetime.now()}: Entering second instance')
    controller.mouseAction(MouseActions.RIGHT, 'images/level1/entranceToLevel2.png')
    if controller.wait_for_image('images/fight/round.png', 5):
        killSensorIfAttacked('Sensor1')
        enterSecondLevel()


def enterThirdLevel():
    print(f'{datetime.now()}: Entering third instance')
    controller.mouseAction(MouseActions.RIGHT, 'images/level2/entranceToLevel3.png')
    if controller.wait_for_image('images/fight/round.png', 5):
        killSensorIfAttacked('Sensor2')
        enterThirdLevel()
    else:
        combat.rest(15)


def enterFourthLevel():
    print(f'{datetime.now()}: Entering fourth instance')
    controller.mouseAction(MouseActions.RIGHT, 'images/level3/entranceToLevel4.png')
    if controller.wait_for_image('images/fight/round.png', 5):
        killSensorIfAttacked('Sensor3')
        enterFourthLevel()


def killSensorIfAttacked(mobName: str):
    if config['takeActionVia'] == 'keyboard':
        controller.pressWithActiveWindow('2')
    else:
        controller.mouseAction(MouseActions.LEFT, 'images/fight/tacticTwo.png')
    controller.pressWithActiveWindow('space')
    combat.finishing_combat(mobName)
    pyautogui.sleep(0.1)
    controller.pressWithActiveWindow('esc')
    combat.rest(8)


def quitInstance():
    controller.mouseAction(MouseActions.RIGHT, 'images/level4/quit.png')
    pyautogui.sleep(5)
    combat.rest(15)


pyautogui.sleep(2)
print("START")


# V2 FLOW
def hunting_V2():
    for i in range(config['repeats']):
        enterEasyV2()
        combat.killMob('Sensor1', 20)
        enterSecondLevel()
        combat.killMob('Boss1')
        combat.killMob('Sensor2', 20)
        enterThirdLevel()
        combat.killMob('Boss2')
        combat.killMob('Sensor3', 20)
        enterFourthLevel()
        combat.killMob('V2')
        quitInstance()


hunting_V2()
