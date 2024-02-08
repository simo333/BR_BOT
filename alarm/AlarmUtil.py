import sys
from datetime import datetime, timedelta

import pyautogui
import pygame

from userinput.UserInputController import wait_for_image, mouseAction, MouseActions


def stop_alarm(closeApp):
    pygame.mixer.music.stop()
    pygame.quit()
    if closeApp:
        sys.exit(400)
    return


def play_alarm(message: str, closeApp=False):
    pygame.init()
    pygame.mixer.music.load("sounds/alarm.wav")
    pygame.mixer.music.play(1)

    show_error_prompt(message, closeApp)


def show_error_prompt(message: str, closeApp=False):
    # Set up the Pygame window for the prompt
    finish_time = datetime.now() + timedelta(seconds=30)
    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("Alarm")

    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(150, 100))

    stop_button = pygame.Rect(100, 150, 100, 50)

    while datetime.now() < finish_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_alarm(closeApp)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if stop_button.collidepoint(event.pos):
                    if closeApp:
                        stop_alarm(closeApp)
                    return

        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, (255, 0, 0), stop_button)
        stop_font = pygame.font.Font(None, 24)
        stop_text = stop_font.render("Stop Alarm", True, (255, 255, 255))
        stop_text_rect = stop_text.get_rect(center=stop_button.center)
        screen.blit(stop_text, stop_text_rect)

        pygame.display.flip()


def alarmChecker(config):
    if config['alarmWhenMsg']:
        if wait_for_image('images/alarm/newMsg.png', 0.5):
            play_alarm("You got a message!", config['closeWhenMsg'])
            mouseAction(MouseActions.LEFT, 'images/alarm/newMsg.png', )
            globalChatPosition = (int(pyautogui.size().width * 0.02), int(pyautogui.size().height * 0.04))
            mouseAction(MouseActions.LEFT, globalChatPosition)
        if config['closeWhenMsg'] and not config['alarmWhenMsg']:
            pygame.init()
            show_error_prompt("You got a message!", True)


def errorAlarm(config):
    if config['alarmWhenError']:
        play_alarm("Error occurred!", True)


def alarmWhenFinishRepeats(config):
    if config['alarmWhenFinishRepeats']:
        play_alarm('Finished repeats!', True)
