import time
from datetime import datetime

import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
from pygetwindow import getWindowsWithTitle

pyautogui.FAILSAFE = False


class MouseActions:
    LEFT = pyautogui.leftClick
    RIGHT = pyautogui.rightClick
    HOLD_DOWN = pyautogui.mouseDown
    DRAG = pyautogui.mouseDown
    DROP = pyautogui.mouseUp


def findImagePosition(targetImage, maxAttempts):
    attempts = 1
    while attempts <= maxAttempts:
        screenshot = pyautogui.screenshot()
        screenShotArray = np.array(screenshot)
        # ssGray = cv2.cvtColor(screenShotArray, cv2.COLOR_BGR2GRAY)
        # targetGray = cv2.cvtColor(targetImage, cv2.COLOR_BGR2GRAY)
        # Perform matching
        result = cv2.matchTemplate(screenShotArray, targetImage, cv2.TM_CCOEFF_NORMED)
        # Get the location with the highest correlation
        minValue, maxValue, minLocation, maxLocation = cv2.minMaxLoc(result)
        # Set a threshold for correlation value (adjust as needed)
        threshold = 0.75

        # Check if the correlation value is above the threshold
        if maxValue >= threshold:
            # Extract the coordinates of the top-left corner of the matched region
            topLeft = maxLocation
            # Get the dimensions of the template image
            targetWidth, targetHeight = targetImage.shape[1], targetImage.shape[0]
            # Calculate the center of the matched region
            centerX = topLeft[0] + targetWidth // 2
            centerY = topLeft[1] + targetHeight // 2
            # Move the mouse to the center of the matched region
            return centerX, centerY
        attempts += 1
    # Return False if the image is not found
    return None


def wait_for_image(image_path, timeoutSeconds=20, intervalSeconds=0.1):
    start_time = time.time()

    # Load the template image
    template_image = cv2.imread(image_path)
    # template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    while time.time() - start_time < timeoutSeconds:
        # Take a screenshot
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        # screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        # Perform template matching
        result = cv2.matchTemplate(screenshot_np, template_image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        # Adjust the threshold as needed
        threshold = 0.8

        if max_val >= threshold:
            return True
        time.sleep(intervalSeconds)

    print(f"{datetime.now()}: Timeout: Image not found - {image_path}")
    return False


def mouseAction(mouseActionType: MouseActions, target: str | tuple[int, int], attempts=20, movementDuration=0.1, dragAndDropFlag=False):
    if type(target) == str:
        targetImage = cv2.imread(target)
        foundCoordinates = findImagePosition(targetImage, attempts)
        if foundCoordinates:
            activate_game_window()
            takeMouseAction(mouseActionType, foundCoordinates, movementDuration, dragAndDropFlag)
            return True
    elif type(target == tuple[int, int]):
        activate_game_window()
        takeMouseAction(mouseActionType, target, movementDuration, dragAndDropFlag)
        return True
    print(f'{datetime.now()}: {mouseActionType}: Image not found - {target}')
    return False


def takeMouseAction(mouseActionType, foundCoordinates, movementDuration, dragAndDropFlag=False):
    pyautogui.moveTo(foundCoordinates[0], foundCoordinates[1], movementDuration)
    if mouseActionType == MouseActions.LEFT:
        pyautogui.mouseDown()
        pyautogui.sleep(0.1)
        pyautogui.mouseUp()
    elif mouseActionType == MouseActions.RIGHT:
        pyautogui.mouseDown(button='right')
        pyautogui.sleep(0.1)
        pyautogui.mouseUp(button='right')
    elif mouseActionType == MouseActions.HOLD_DOWN and not dragAndDropFlag:
        pyautogui.mouseDown()
        pyautogui.sleep(2)
        pyautogui.mouseUp()
    elif mouseActionType == MouseActions.DRAG and dragAndDropFlag:
        pyautogui.mouseDown()
        pyautogui.sleep(0.05)
    elif mouseActionType == MouseActions.DROP and dragAndDropFlag:
        pyautogui.mouseUp()


def dragAndDrop(targetDrag, targetDrop):
    targetDragImage = cv2.imread(targetDrag)
    targetDropImage = cv2.imread(targetDrop)
    dragPosition = findImagePosition(targetDragImage, 1)
    if dragPosition:
        mouseAction(MouseActions.DRAG, dragPosition, 1, dragAndDropFlag=True)
        dropPosition = findImagePosition(targetDropImage, 1)
        if dropPosition:
            dropPosition = (dropPosition[0], dropPosition[1] - pyautogui.size().height * 0.05)  # move a little above rest icon
            mouseAction(MouseActions.DROP, dropPosition, 1, 0.5, True)
            mouseAction(MouseActions.LEFT, "images/others/confirmButton.png", 1)
            return True
        print(f'{datetime.now()}: DROP MOUSE: Image not found - {targetDrop}')
        return False
    print(f'{datetime.now()}: DRAG MOUSE: Image not found - {targetDrag}')
    return False


def pressWithActiveWindow(key):
    activate_game_window()
    pyautogui.keyDown(key)
    pyautogui.sleep(0.1)
    pyautogui.keyUp(key)


def check_if_target_on_list(img):
    wasFound = wait_for_image(img, 3)
    if wasFound:
        return True
    return False


def activate_game_window():
    window_title_to_activate = "BrokenRanks"
    try:
        window = getWindowsWithTitle(window_title_to_activate)[0]
        window.activate()
        return True
    except IndexError:
        window = getWindowsWithTitle(window_title_to_activate)[0]
        window.minimize()
        pyautogui.sleep(0.1)
        window.maximize()
        activate_game_window()
    except gw.PyGetWindowException:
        window = getWindowsWithTitle(window_title_to_activate)[0]
        window.minimize()
        pyautogui.sleep(0.1)
        window.maximize()
        activate_game_window()
