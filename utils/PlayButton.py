from utils import Button
from config import UIConfig
import pygame
import time

class PlayButton(Button):
    def __init__(self, x, y):
        super().__init__(x, y, UIConfig.PLAY_BUTTON_COLOR, UIConfig.PLAY_BUTTON_TEXT)
        self.is_in_algorithm = False

    def setIsInAlgorithm(self, is_in_algorithm):
        self.is_in_algorithm = is_in_algorithm
    
    def setColor(self, color):
        self.color = color
    def setText(self, text):
        self.text = text
    def handleClick(self, gameObject, algorithm):
        print("gameObject: ", gameObject.maze)

        finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath = algorithm(gameObject)
        if finalPath == "":
            return False
        for step in finalPath: 
            if self.is_in_algorithm == False:
                self.setColor(UIConfig.PLAY_BUTTON_COLOR)
                self.setText(UIConfig.PLAY_BUTTON_TEXT)
                return True
            self.setColor(UIConfig.PLAYING_BUTTON_COLOR)
            self.setText(UIConfig.PLAYING_BUTTON_TEXT)
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
        return True
        