from utils import Button
from config import UIConfig
import pygame
import time

class PlayButton(Button):
    def __init__(self, x, y):
        super().__init__(x, y, UIConfig.PLAY_BUTTON_COLOR, UIConfig.PLAY_BUTTON_TEXT)
    
    def handleClick(self, gameObject, algorithm):
        finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath = algorithm(gameObject)
        for step in finalPath: 
            if step.lower() == "u":  
                event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
                pygame.event.post(event) 
            elif step.lower() == "d": 
                event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
                pygame.event.post(event)  
            elif step.lower() == "l": 
                event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
                pygame.event.post(event) 
            elif step.lower() == "r": 
                event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
                pygame.event.post(event)
            print("handle step: ", step)
            time.sleep(0.3) 
        