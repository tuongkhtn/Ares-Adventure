from utils import Button
from config import UIConfig
import pygame
import time

class PlayButton(Button):
    def __init__(self, x, y):
        super().__init__(x, y, UIConfig.PLAY_BUTTON_COLOR, UIConfig.PLAY_BUTTON_TEXT)
        self.is_in_algorithm = False
        self.game_result = 0
        self.is_searching = False

    def setIsInAlgorithm(self, is_in_algorithm):
        self.is_in_algorithm = is_in_algorithm
    def setGameResult(self, game_result):
        self.game_result = game_result
    def setIsSearching(self, is_searching):
        self.is_searching = is_searching
    
    def setColor(self, color):
        self.color = color
    def setText(self, text):
        self.text = text

    def update_theme(self):
        if (self.is_in_algorithm):
            self.setColor(UIConfig.PLAYING_BUTTON_COLOR)
            self.setText(UIConfig.PLAYING_BUTTON_TEXT)
        else:
            self.setColor(UIConfig.PLAY_BUTTON_COLOR)
            self.setText(UIConfig.PLAY_BUTTON_TEXT)

    def handleClick(self, gameObject, algorithm):
        if self.is_in_algorithm:
            self.update_theme()
        self.is_searching = True
        finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath = algorithm(gameObject)
        self.is_searching = False
        if finalPath == "":
            print("No solution")
            self.game_result = -1
            return False
        for step in finalPath: 
            if self.is_in_algorithm == False:
                self.update_theme()
                return True
            self.update_theme()
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
            time.sleep(0.3) 
        
        self.game_result = 1
        return True
        