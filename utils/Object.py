import pygame
from config import UIConfig

class Object:
    def __init__(self, x, y):
        self._x = x
        self._y = y
            
    def addUI(self, img_path):
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (UIConfig.TILE_SIZE, UIConfig.TILE_SIZE))
        self.screen_position = [self._y * UIConfig.TILE_SIZE, self._x * UIConfig.TILE_SIZE]
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
        
    def draw(self, surface):
        surface.blit(self.image, (self.screen_position[0] + UIConfig.OFFSET_X, self.screen_position[1] + UIConfig.OFFSET_Y))
        
    def setScreenPosition(self, x, y):
        self.screen_position = [y * UIConfig.TILE_SIZE, x * UIConfig.TILE_SIZE]
        