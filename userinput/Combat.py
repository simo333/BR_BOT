import os
from datetime import datetime

import pyautogui

from dto.MobTacticDTO import MobTacticDTO
from userinput import UserInputController
from userinput.UserInputController import MouseActions

controller = UserInputController
trash_images_dir = 'images/trashItems'

tacticDictionary = {
    1: "images/fight/tacticOne.png",
    2: "images/fight/tacticTwo.png",
    3: "images/fight/tacticThree.png",
    4: "images/fight/tacticFour.png"
}

potionsDictionary = {
    "hpPotions": "images/fight/healthPotion.png",
    "manaPotions": "images/fight/manaPotion.png",
    "staminaPotions": "images/fight/staminaPotion.png"
}


class TargetAction:
    KILL = 'images/fight/atkIcon.png'
    JOIN = 'images/fight/joinTeamIcon.png'


class Combat:
    ACTUAL_DEATHS = 0

    def __init__(self, mobTacticJson, config):
        self.mobJson = mobTacticJson
        self.config = config
        self.MAX_DEATHS = config['maxDeaths']

    def killMob(self, mobName, attempts=20, isBoss=False, afterDeath=False):
        print(f'{datetime.now()}: Killing {mobName}')
        mobTactic = MobTacticDTO(**self.mobJson[mobName])
        wasFound = targetInteraction(TargetAction.KILL, mobTactic.imgPath, attempts)
        if wasFound:
            if controller.wait_for_image('images/fight/round.png', 20):
                self.proceed_with_combat(mobName, mobTactic, isBoss)
                if mobTactic.saveSS:
                    saveSS(mobName)
                # If resting time is greater than 0, then rest for the given time in seconds
                if mobTactic.restingTime > 0:
                    self.rest(mobTactic.restingTime)
                if not afterDeath:
                    controller.pressWithActiveWindow('esc')
            # Attack until the target is found
            if mobTactic.repeatAttack:
                self.killMob(mobName, attempts, isBoss, False)

    def proceed_with_combat(self, mobName: str, mobTactic: MobTacticDTO, isBoss: bool):
        self.chooseTactic(mobTactic.tacticRound1)
        controller.pressWithActiveWindow('space')
        self.chooseTactic(mobTactic.tacticRest)
        self.finishing_combat(mobName, isBoss)

    def finishing_combat(self, mobName, isBoss: bool):
        mobTactic = MobTacticDTO(**self.mobJson[mobName])
        """
            Wait for the rest icon appears -> fight is over or clock icon -> new round has started;
            Save screenshot if specified in json;
            Press 'esc' to close fight summary
            """
        for i in range(1200):
            if controller.wait_for_image('images/fight/restIcon.png', 0.5, 0.1):
                break
            elif controller.wait_for_image('images/fight/clockBar.png', 0.5, 0.1):
                self.chooseTactic(mobTactic.tacticRest)
                controller.pressWithActiveWindow('space')
            elif controller.wait_for_image('images/fight/deathCard.png', 0.3, 0.1):
                self.handleDeath(mobName, isBoss)
                break

    def handleDeath(self, mobName: str, isBoss: bool):
        Combat.ACTUAL_DEATHS += 1
        if Combat.ACTUAL_DEATHS == self.MAX_DEATHS:
            raise Exception('MAX AMOUNT OF DEATHS REACHED.')
        saveSS("DEAD")
        # Choose card
        controller.mouseAction(MouseActions.LEFT, 'images/fight/deathCard.png')
        pyautogui.sleep(5)
        # Fill resources (hp, mana, stamina)
        self.fillResources()
        # Try to find img of mob that killed you
        self.killMob(mobName, 20, isBoss, True)

    def chooseTactic(self, tactic: int):
        if self.config['takeActionVia'] == 'keyboard':
            controller.pressWithActiveWindow(str(tactic))
        else:
            controller.mouseAction(MouseActions.LEFT, tacticDictionary.get(tactic))

    def rest(self, restingTime):
        if self.config['takeActionVia'] == 'keyboard':
            controller.pressWithActiveWindow('r')
        else:
            controller.mouseAction(MouseActions.LEFT, 'images/fight/restIcon.png')
        pyautogui.sleep(restingTime)

    def fillResources(self):
        controller.pressWithActiveWindow('p')
        pyautogui.sleep(0.5)
        self.fillResource('hpPotions')
        self.fillResource('manaPotions')
        self.fillResource('staminaPotions')
        controller.pressWithActiveWindow('p')

    def fillResource(self, resource: str):
        deathData = self.config['deathHandle']
        for i in range(deathData[resource]):
            controller.mouseAction(MouseActions.LEFT, potionsDictionary[resource])
            pyautogui.sleep(1)


def saveSS(mobName):
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


""" Scenario:
Check if almost full icon is found
No: omit function / Yes: go to weapon section in bag
Check 4 pages of weapons as follows:
Collect all .png files in itemTrash folder and iterate through them
Iterate until any of items was found
If not found -> change page (or finish)
If found -> iterate all the items once again (after throwing later items the ones that were iterated bedore may appear on actual page)"""
def checkIfBagIsAlmostFull():
    isAlmostFullIcon = controller.wait_for_image('images/others/almostFullBagIcon.png', 3, 1)
    if isAlmostFullIcon:
        controller.pressWithActiveWindow('e')
        pyautogui.sleep(0.5)
        controller.mouseAction(MouseActions.LEFT, 'images/others/weaponSectionIcon.png', 2)
        file_list = [os.path.join(trash_images_dir, name) for name in os.listdir(trash_images_dir) if os.path.isfile(
            os.path.join(trash_images_dir, name))]  # Find all files in trashItem folder and return list with full paths

        for i in range(4):
            foundAnyItem = True
            while foundAnyItem:
                foundAnyItem = False
                for full_path in file_list:
                    wasFound = controller.dragAndDrop(full_path, 'images/fight/restIcon.png')
                    if wasFound:
                        foundAnyItem = True
            controller.mouseAction(MouseActions.LEFT, 'images/others/nextPageIcon.png')


def targetInteraction(action: TargetAction, targetImg, attempts):
    pyautogui.moveTo(pyautogui.size().width - 1, pyautogui.size().height * 0.1)
    controller.pressWithActiveWindow('n')
    pyautogui.sleep(0.3)
    controller.mouseAction(MouseActions.LEFT, targetImg, attempts)
    controller.pressWithActiveWindow('n')
    pyautogui.sleep(0.3)
    wasFound = controller.mouseAction(MouseActions.LEFT, action.__str__(), movementDuration=0.1)
    return wasFound
