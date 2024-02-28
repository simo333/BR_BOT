import os
from datetime import datetime

import pyautogui

from dto.MobTacticDTO import MobTacticDTO
from userinput import UserInputController
from userinput.UserInputController import MouseActions

controller = UserInputController

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

    def killMob(self, mobName, attempts=200, isBoss=False):
        print(f'{datetime.now()}: Killing {mobName}')
        mobTactic = MobTacticDTO(**self.mobJson[mobName])
        wasFound = targetInteraction(TargetAction.KILL, mobTactic.imgPath, attempts)
        if wasFound:
            if controller.wait_for_image('images/fight/round.png', 20):
                self.proceed_with_combat(mobName, mobTactic)
                if mobTactic.saveSS:
                    saveSS(mobName)
                pyautogui.sleep(0.5)
                controller.pressWithActiveWindow('esc')
                # If resting time is greater than 0, then rest for the given time in seconds
                if mobTactic.restingTime > 0:
                    self.rest(mobTactic.restingTime)
                # Attack until the target is found
            if mobTactic.repeatAttack:
                self.killMob(mobName, attempts)
        else:
            if isBoss:
                self.killMob(mobName, attempts, True)

    def proceed_with_combat(self, mobName: str, mobTactic: MobTacticDTO):
        self.chooseTactic(mobTactic.tacticRound1)
        controller.pressWithActiveWindow('space')
        self.chooseTactic(mobTactic.tacticRest)
        self.finishing_combat(mobName, True)

    def finishing_combat(self, mobName, isTeamLeader: bool):
        mobTactic = MobTacticDTO(**self.mobJson[mobName])
        fighting_with_assist = self.config['deathHandle']['withAssist']
        """
            Wait for the rest icon appears -> fight is over or clock icon -> new round has started;
            Save screenshot if specified in json;
            Press 'esc' to close fight summary
            """

        for i in range(1200):
            if controller.wait_for_image('images/fight/restIcon.png', 0.5, 0.1):
                if fighting_with_assist:
                    if isTeamLeader:
                        if not controller.wait_for_image('images/fight/twoPlayersInTeam.png', 400):
                            exit(1)
                    else:
                        controller.pressWithActiveWindow('esc')
                        joinYourAssist()
                break
            elif controller.wait_for_image('images/fight/clockBar.png', 0.5, 0.1):
                self.chooseTactic(mobTactic.tacticRest)
                controller.pressWithActiveWindow('space')
            elif controller.wait_for_image('images/fight/deathCard.png', 0.3, 0.1):
                self.handleDeath(mobName, isTeamLeader)
                break

    def handleDeath(self, mobName: str, isTeamLeader: bool):
        Combat.ACTUAL_DEATHS += 1
        if Combat.ACTUAL_DEATHS == self.MAX_DEATHS:
            raise Exception('MAX AMOUNT OF DEATHS REACHED.')
        saveSS("DEAD")
        # Choose card
        controller.mouseAction(MouseActions.LEFT, 'images/fight/deathCard.png')
        pyautogui.sleep(5)
        # Fill resources (hp, mana, stamina)
        self.fillResources()
        # Check if fighting alone or with someone
        fighting_with_assist = self.config['deathHandle']['withAssist']
        if not fighting_with_assist:
            # Try to find img of mob that killed you
            self.killMob(mobName)
            # If not then walk halfway of instance
            moveToInstanceHalfway()
            if not controller.wait_for_image('images/fight/round.png', 5):
                # Try to find img of mob that killed you again
                self.killMob(mobName)
        else:
            # As team leader wait for the other to finish combat and join your team
            # If not joined then move to halfway of the instance and wait again
            if isTeamLeader:
                if not controller.wait_for_image('images/fight/twoPlayersInTeam.png', 120):
                    moveToInstanceHalfway()
                controller.wait_for_image('images/fight/twoPlayersInTeam.png', 180)
                return
            else:
                joinYourAssist()

    def killMobAssist(self, mobName):
        print(f'{datetime.now()}: Assisting to kill {mobName}')
        mobTactic = MobTacticDTO(**self.mobJson[mobName])
        if controller.wait_for_image('images/fight/round.png', 1200):
            self.proceed_with_combat_assist(mobName, mobTactic)

    def proceed_with_combat_assist(self, mobName, mobTactic: MobTacticDTO):
        self.chooseTactic(mobTactic.tacticRound1)
        controller.pressWithActiveWindow('space')
        self.chooseTactic(mobTactic.tacticRest)
        self.finishing_combat(mobName, False)

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


def moveToInstanceHalfway():
    screen_size = pyautogui.size()
    position_x = int(screen_size.width * 0.74)
    position_y = int(screen_size.height * 0.264)
    controller.mouseAction(MouseActions.LEFT, (position_x, position_y))


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


def joinYourAssist():
    if not targetInteraction(TargetAction.JOIN, 'images/fight/assistNick.png', 100):
        moveToInstanceHalfway()
        joinYourAssist()
    if not controller.wait_for_image('images/fight/twoPlayersInTeam.png', 20):
        joinYourAssist()


def targetInteraction(action: TargetAction, targetImg, attempts):
    pyautogui.moveTo(pyautogui.size().width - 1, pyautogui.size().height * 0.1)
    controller.pressWithActiveWindow('n')
    pyautogui.sleep(0.3)
    controller.mouseAction(MouseActions.LEFT, targetImg, attempts)
    controller.pressWithActiveWindow('n')
    pyautogui.sleep(0.3)
    wasFound = controller.mouseAction(MouseActions.LEFT, action.__str__(), movementDuration=0.1)
    return wasFound
