import time

import cv2
import numpy as np
import pyautogui
import pygetwindow as gw

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
            targetHeight, targetWidth = targetGray.shape[::-1]
            # Calculate the center of the matched region
            centerX = topLeft[0] + targetWidth // 2
            centerY = topLeft[1] + targetHeight // 2
            # Move the mouse to the center of the matched region
            return centerX, centerY
        attempts += 1
        print(f'{maxValue}')
    # Return False if the image is not found
    return None


def wait_for_image(image_path, timeoutSeconds=120, intervalSeconds=1):
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


def mouseAction(mouseActionType: MouseActions, targetImgPath, attempts=20, movementDuration=0.1):
    targetImage = cv2.imread(targetImgPath)
    foundCoordinates = findImagePosition(targetImage, attempts)
    if foundCoordinates:
        activate_game_window()
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
        return True
    print(f'{mouseActionType}: Image not found - {targetImgPath}')
    return False


def pressWithActiveWindow(key):
    activate_game_window()
    pyautogui.keyDown(key)
    pyautogui.sleep(0.1)
    pyautogui.keyUp(key)


def activate_game_window():
    window_title_to_activate = "BrokenRanks"
    try:
        window = gw.getWindowsWithTitle(window_title_to_activate)[0]
        window.activate()
        return True
    except IndexError:
        print(f"Window with title '{window_title_to_activate}' not found.")
        return False

