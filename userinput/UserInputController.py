import time

import cv2
import numpy as np
import pyautogui
import pygetwindow as gw

pyautogui.FAILSAFE = False


def findImagePosition(targetImage, maxAttempts, movementDuration=0.1):
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
            pyautogui.moveTo(centerX, centerY, movementDuration)
            return True
        attempts += 1
        print(f'{maxValue}')
        if attempts % 10 == 1:
            moveCharacter()
        pyautogui.sleep(0.1)
    # Return False if the image is not found
    return False


def moveCharacter():
    # Get the screen size
    screen_width, screen_height = pyautogui.size()

    # Calculate the center position
    center_x = screen_width // 2
    center_y = screen_height // 2
    pyautogui.moveTo(center_x + screen_width * 0.03, center_y - screen_height * 0.05)
    pyautogui.leftClick()


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


def leftClick(targetPath, attempts=20):
    targetImage = cv2.imread(targetPath)
    wasFound = findImagePosition(targetImage, attempts)
    if wasFound:
        activate_game_window()
        pyautogui.leftClick()
        return True
    print(f'LEFT CLICK: Image not found - {targetPath}')
    return False


def rightClick(targetPath, attempts=20, movementDuration=0.1):
    targetImage = cv2.imread(targetPath)
    wasFound = findImagePosition(targetImage, attempts, movementDuration)
    if wasFound:
        pyautogui.rightClick()
        return True
    print(f'RIGHT CLICK: Image not found - {targetPath}')
    return False


def leftMouseDown(targetPath, attempts=20):
    targetImage = cv2.imread(targetPath)
    wasFound = findImagePosition(targetImage, attempts)
    if wasFound:
        pyautogui.mouseDown()
        pyautogui.sleep(2)
        pyautogui.mouseUp()
        return True
    print(f'LEFT MOUSE DOWN: Image not found - {targetPath}')
    return False


def pressWithActiveWindow(key):
    activate_game_window()
    pyautogui.press(key)


def activate_game_window():
    window_title_to_activate = "BrokenRanks"
    try:
        window = gw.getWindowsWithTitle(window_title_to_activate)[0]
        window.activate()
        return True
    except IndexError:
        print(f"Window with title '{window_title_to_activate}' not found.")
        return False

