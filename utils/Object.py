import pygame
from config.UIConfig import UIConfig


class Object:
    def __init__(self, x, y):
        self._x = x
        self._y = y
            
    def addUI(self, img_path, height=UIConfig.TILE_SIZE, width=UIConfig.TILE_SIZE):
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.screen_position = [self._y * height + UIConfig.OFFSET_X, self._x * width + UIConfig.OFFSET_Y]
        return self

    def getX(self):
        return self._x
    
    def getY(self):
        return self._y
    
    def getCoordinate(self):
        return self._x, self._y
    
    def setX(self, x):
        self._x = x
        
    def setY(self, y):
        self._y = y
        
    def setCoordinate(self, x, y):
        self._x = x
        self._y = y

    def draw(self, screen, offset_x=0, offset_y=0):
        screen.blit(self.image, (self.screen_position[0] + offset_x, self.screen_position[1] + offset_y))     
    
