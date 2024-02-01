import os
from datetime import datetime

import pyautogui

from dto.MobTacticDTO import MobTacticDTO
from userinput import UserInputController

controller = UserInputController

tacticDictionary = {
    1: "images/fight/tacticOne.png",
    2: "images/fight/tacticTwo.png",
    3: "images/fight/tacticThree.png",
    4: "images/fight/tacticFour.png"
}


def finishing_combat():
    """
        Wait for the armor icon appears -> fight is over or clock icon -> new round has started;
        Save screenshot if specified in json;
        Press 'esc' to close fight summary
        """
    for i in range(1200):
        if controller.wait_for_image('images/fight/clockBar.png', 0.5, 0.5):
            controller.pressWithActiveWindow('space')
        elif controller.wait_for_image('images/fight/restIcon.png', 0.5, 0.5):
            break


class Combat:

    def __init__(self, mobTacticJson, config):
        self.mobJson = mobTacticJson
        self.config = config

    def killMob(self, mobName, attempts=10):
        print(f'Killing {mobName}')
        mobTactic = MobTacticDTO(**self.mobJson[mobName])
        wasFound = controller.rightClick(mobTactic.imgPath, attempts)
        if wasFound:
            controller.wait_for_image('images/fight/round.png')
            self.proceed_with_combat(mobTactic)
            if mobTactic.saveSS:
                saveDropSS(mobName)
            controller.pressWithActiveWindow('esc')
            # If resting time is greater than 0, then rest for the given time in seconds
            if mobTactic.restingTime > 0:
                controller.leftClick('images/fight/restIcon.png')
                pyautogui.sleep(mobTactic.restingTime)
            # Attack until the target is found
            if mobTactic.repeatAttack:
                self.killMob(mobName, attempts)

    def killMobAssist(self, mobName):
        print(f'Assisting to kill {mobName}')
        mobTactic = MobTacticDTO(**self.mobJson[mobName])
        if controller.wait_for_image('images/fight/round.png', 1200):
            self.proceed_with_combat(mobTactic)

    def proceed_with_combat(self, mobTactic):
        self.chooseTactic(mobTactic.tacticRound1)
        controller.pressWithActiveWindow('space')
        self.chooseTactic(mobTactic.tacticRest)
        finishing_combat()

    def chooseTactic(self, tactic: int):
        if self.config['selectTacticVia'] == 'keyboard':
            controller.pressWithActiveWindow(str(tactic))
        else:
            controller.leftClick(tacticDictionary.get(tactic))


def saveDropSS(mobName):
    # Get the current date
    current_date = datetime.now()
    # Format the date as dd-mm-yyyy
    formatted_date_time = current_date.strftime('%d-%m-%YT%H-%M')
    print(f'Saving screenshot of drop - {formatted_date_time}')
    dropScreenshot = pyautogui.screenshot()
    # Create the directory if it doesn't exist
    directory_path = 'C:/brokenRanksHunts/'
    os.makedirs(directory_path, exist_ok=True)
    dropScreenshot.save(f'C:/brokenRanksHunts/{mobName}_{formatted_date_time}.png')
