import os
from datetime import datetime

import cv2
import numpy as np
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

    def __init__(self, mobTacticJson, config):
        self.mobJson = mobTacticJson
        self.config = config

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
        self.finishing_combat(mobName)

    def finishing_combat(self, mobName):
        """
            Wait for the rest icon appears -> fight is over or clock icon -> new round has started;
            Save screenshot if specified in json;
            Press 'esc' to close fight summary
            """
        mobTactic = MobTacticDTO(**self.mobJson[mobName])
        for i in range(1200):
            if controller.wait_for_image('images/fight/restIcon.png', 0.5, 0.1):
                break
            elif controller.wait_for_image('images/fight/clockBar.png', 0.5, 0.1):
                self.chooseTactic(mobTactic.tacticRest)
                controller.pressWithActiveWindow('space')
            elif controller.wait_for_image('images/fight/deathCard.png', 0.3, 0.1):
                self.handleDeath(mobName)

    def killMobAssist(self, mobName):
        print(f'{datetime.now()}: Assisting to kill {mobName}')
        mobTactic = MobTacticDTO(**self.mobJson[mobName])
        if controller.wait_for_image('images/fight/round.png', 1200):
            self.proceed_with_combat(mobName, mobTactic)

    def proceed_with_combat_assist(self, mobTactic: MobTacticDTO):
        self.chooseTactic(mobTactic.tacticRound1)
        controller.pressWithActiveWindow('space')
        self.chooseTactic(mobTactic.tacticRest)
        self.finishing_combat_assist()

    def finishing_combat_assist(self):
        """
            Wait for the rest icon appears -> fight is over or clock icon -> new round has started;
            Save screenshot if specified in json;
            Press 'esc' to close fight summary
            """
        for i in range(1200):
            if controller.wait_for_image('images/fight/restIcon.png', 0.5, 0.1):
                break
            elif controller.wait_for_image('images/fight/clockBar.png', 0.5, 0.1):
                controller.pressWithActiveWindow('space')
        if not controller.wait_for_image('images/fight/twoPlayersInTeam.png', 0.3, 0.1):
            joinYourAssist()

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

    def handleDeath(self, mobName: str):
        # Choose card
        controller.mouseAction(MouseActions.LEFT, 'images/fight/deathCard.png')
        saveSS("DEAD")
        pyautogui.sleep(10)
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
            if not controller.wait_for_image('images/fight/twoPlayersInTeam.png', 60):
                moveToInstanceHalfway()
            controller.wait_for_image('images/fight/twoPlayersInTeam.png', 120)

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
    print(f'Saving screenshot - {formatted_date_time}')
    dropScreenshot = pyautogui.screenshot()
    # Create the directory if it doesn't exist
    directory_path = 'C:/brokenRanksHunts/'
    os.makedirs(directory_path, exist_ok=True)
    dropScreenshot.save(f'C:/brokenRanksHunts/{mobName}_{formatted_date_time}.png')


def joinYourAssist():
    controller.pressWithActiveWindow('esc')
    targetInteraction(TargetAction.JOIN, 'images/fight/assistNick.png', 200)


def targetInteraction(action: TargetAction, targetImg, attempts):
    pyautogui.moveTo(pyautogui.size().width - 1, pyautogui.size().height * 0.1)
    controller.pressWithActiveWindow('n')
    pyautogui.sleep(0.3)
    controller.mouseAction(MouseActions.LEFT, targetImg, attempts)
    controller.pressWithActiveWindow('n')
    pyautogui.sleep(0.3)
    wasFound = controller.mouseAction(MouseActions.LEFT, action.__str__(), movementDuration=0.1)
    return wasFound



def setDef(melee: int, dist: int, mental: int):

    # Get the width and height of the screen
    screen_width, screen_height = pyautogui.size()

    # Calculate the height of the region to capture (10% of the screen height)
    capture_height = int(0.1 * screen_height)

    region = (0, screen_height - capture_height, int(screen_width), capture_height)

    # Load the screenshot and the search image
    screenshot = pyautogui.screenshot(region=region)
    screenshotArray = np.array(screenshot)
    search_image = cv2.imread("images/fight/clearDefIcon.png")

    # Convert both images to grayscale
    screenshot_gray = cv2.cvtColor(screenshotArray, cv2.COLOR_BGR2GRAY)
    search_image_gray = cv2.cvtColor(search_image, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, search_image_gray, cv2.TM_CCOEFF_NORMED)

    # Get the locations where the threshold is exceeded
    threshold = 0.8
    locations = np.where(result >= threshold)

    # Extract the coordinates of the top-left corner of each match
    match_locations = list(zip(*locations[::-1]))

    # Filter out duplicate locations based on a minimum distance
    unique_locations = find_unique_locations(match_locations)

    # Adjust height (ss takes lowest 10% of the screen, so we must add the 90% of the screen height to get right coords)
    adjusted_locations = [(location[0], location[1] + int(0.9 * screen_height)) for location in unique_locations]

    reset_def(adjusted_locations)
    set_def(adjusted_locations, 0, melee)
    set_def(adjusted_locations, 1, dist)
    set_def(adjusted_locations, 2, mental)


'''Removes location duplicates - sometimes locations contains the same target that differs 1-2 pixel'''
def find_unique_locations(locations, min_distance=10):
    unique_locations = []
    for loc in locations:
        if all(np.linalg.norm(np.array(loc) - np.array(existing_loc)) > min_distance for existing_loc in unique_locations):
            unique_locations.append(loc)
    return unique_locations


'''Resets current def in following sequence: mental, distance, melee'''
def reset_def(locations: list):
    locations.reverse()
    for location in locations:
        pyautogui.moveTo(location[0], location[1], 0.1)
        pyautogui.leftClick()
    locations.reverse()


'''Sets def value equal to defPoints on zone (0-melee, 1-dist, 2-mental)'''
def set_def(locations, zone: int, defPoints: int):
    if defPoints != 0:
        # defPoint is a representation of 50px on base monitor width resolution (2560) on current resolution
        base_monitor_width = 2560
        defPoint = int(50 * pyautogui.size().width / base_monitor_width)
        defLocation = locations[zone]
        pyautogui.moveTo(defLocation[0], defLocation[1], 0.1)
        pyautogui.moveRel(defPoint * defPoints, 0, 0.1)
        pyautogui.leftClick()

