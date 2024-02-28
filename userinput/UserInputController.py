import time

import cv2
import numpy as np
import pyautogui
from pygetwindow import PyGetWindowException, getWindowsWithTitle

pyautogui.FAILSAFE = False


class MouseActions:
    LEFT = pyautogui.leftClick
    RIGHT = pyautogui.rightClick
    HOLD_DOWN = pyautogui.mouseDown


def findImagePosition(targetImage, maxAttempts):
    attempts = 1
    while attempts <= maxAttempts:
        screenshot = pyautogui.screenshot()
        screenShotArray = np.array(screenshot)
        ssGray = cv2.cvtColor(screenShotArray, cv2.COLOR_BGR2GRAY)
        targetGray = cv2.cvtColor(targetImage, cv2.COLOR_BGR2GRAY)
        # Perform matching
        result = cv2.matchTemplate(ssGray, targetGray, cv2.TM_CCOEFF_NORMED)
        # Get the location with the highest correlation
        minValue, maxValue, minLocation, maxLocation = cv2.minMaxLoc(result)
        # Set a threshold for correlation value (adjust as needed)
        threshold = 0.75

        # Check if the correlation value is above the threshold
        if maxValue >= threshold:
            # Extract the coordinates of the top-left corner of the matched region
            topLeft = maxLocation
            # Get the dimensions of the template image
            targetWidth, targetHeight = targetGray.shape[::-1]
            # Calculate the center of the matched region
            centerX = topLeft[0] + targetWidth // 2
            centerY = topLeft[1] + targetHeight // 2
            # Move the mouse to the center of the matched region
            return centerX, centerY
        attempts += 1
    # Return False if the image is not found
    return None


def wait_for_image(image_path, timeoutSeconds=120, intervalSeconds=0.1):
    start_time = time.time()

    # Load the template image
    template_image = cv2.imread(image_path)
    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    while time.time() - start_time < timeoutSeconds:
        # Take a screenshot
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        # Perform template matching
        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        # Adjust the threshold as needed
        threshold = 0.8

        if max_val >= threshold:
            return True
        time.sleep(intervalSeconds)

    print(f"Timeout: Image not found - {image_path}")
    return False


def mouseAction(mouseActionType: MouseActions, target: str | tuple[int, int], attempts=20, movementDuration=0.1):
    if type(target) == str:
        targetImage = cv2.imread(target)
        foundCoordinates = findImagePosition(targetImage, attempts)
        if foundCoordinates:
            activate_game_window()
            takeMouseAction(foundCoordinates, mouseActionType, movementDuration)
            return True
    elif type(target == tuple[int, int]):
        activate_game_window()
        takeMouseAction(target, mouseActionType, movementDuration)
        return True
    print(f'{mouseActionType}: Image not found - {target}')
    return False


def takeMouseAction(foundCoordinates, mouseActionType, movementDuration):
    pyautogui.moveTo(foundCoordinates[0], foundCoordinates[1], movementDuration)
    if mouseActionType == MouseActions.LEFT:
        pyautogui.mouseDown()
        pyautogui.sleep(0.1)
        pyautogui.mouseUp()
    elif mouseActionType == MouseActions.RIGHT:
        pyautogui.mouseDown(button='right')
        pyautogui.sleep(0.1)
        pyautogui.mouseUp(button='right')
    elif mouseActionType == MouseActions.HOLD_DOWN:
        pyautogui.mouseDown()
        pyautogui.sleep(2)
        pyautogui.mouseUp()


def pressWithActiveWindow(key):
    activate_game_window()
    pyautogui.keyDown(key)
    pyautogui.sleep(0.1)
    pyautogui.keyUp(key)


def check_if_target_on_list(img):
    pyautogui.moveTo(pyautogui.size().width - 1, pyautogui.size().height * 0.1)
    pressWithActiveWindow('n')
    wasFound = wait_for_image(img)
    pyautogui.sleep(0.1)
    if wasFound:
        pressWithActiveWindow('n')
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
    except PyGetWindowException:
        window = getWindowsWithTitle(window_title_to_activate)[0]
        window.minimize()
        pyautogui.sleep(0.1)
        window.maximize()
        activate_game_window()
