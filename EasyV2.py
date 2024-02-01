import userinput

import json

import pyautogui

from userinput import UserInputController
from userinput.Combat import Combat, finishing_combat

with open('config.json', 'r') as file:
    config = json.load(file)

with open(config['tacticSource'], 'r') as file:
    mobData = json.load(file)

controller = UserInputController
combat = Combat(mobData, config)


def enterEasyV2():
    controller.rightClick('images/level0/entranceToInstance.png', movementDuration=0.3)
    if not controller.wait_for_image('images/level0/easyV2Option.png', 3, 1):
        pyautogui.moveTo(300, 300)
        enterEasyV2()
    controller.leftMouseDown('images/level0/easyV2Option.png')


def enterSecondLevel():
    controller.rightClick('images/level1/entranceToLevel2.png')
    if controller.wait_for_image('images/fight/round.png', 5, 1):
        killSensorIfAttacked()
        enterSecondLevel()


def enterThirdLevel():
    controller.rightClick('images/level2/entranceToLevel3.png')
    if controller.wait_for_image('images/fight/round.png', 5, 1):
        if config['selectTacticVia'] == 'keyboard':
            controller.pressWithActiveWindow('2')
        else:
            controller.leftClick('images/fight/tacticTwo.png')
        controller.pressWithActiveWindow('space')
        finishing_combat()
        controller.leftClick('images/fight/restIcon.png')
        controller.pressWithActiveWindow('esc')
        enterThirdLevel()
    else:
        controller.leftClick('images/fight/restIcon.png')
        pyautogui.sleep(15)


def enterFourthLevel():
    controller.rightClick('images/level3/entranceToLevel4.png')
    if controller.wait_for_image('images/fight/round.png', 5, 1):
        killSensorIfAttacked()
        enterFourthLevel()


def killSensorIfAttacked():
    if config['selectTacticVia'] == 'keyboard':
        controller.pressWithActiveWindow('2')
    else:
        controller.leftClick('images/fight/tacticTwo.png')
    controller.pressWithActiveWindow('space')
    finishing_combat()
    controller.leftClick('images/fight/restIcon.png')
    controller.pressWithActiveWindow('esc')
    pyautogui.sleep(8)


def quitInstance():
    controller.rightClick('images/level4/quit.png')
    pyautogui.sleep(5)
    controller.leftClick('images/fight/restIcon.png')
    pyautogui.sleep(15)


pyautogui.sleep(2)
print("START")


# V2 FLOW
def hunting_V2():
    for i in range(config['repeats']):
        enterEasyV2()
        combat.killMob('Sensor1', 20)
        enterSecondLevel()
        combat.killMob('Boss1', 200)
        combat.killMob('Sensor2', 20)
        enterThirdLevel()
        combat.killMob('Boss2', 200)
        combat.killMob('Sensor3', 20)
        enterFourthLevel()
        combat.killMob('V2', 200)
        quitInstance()


hunting_V2()
