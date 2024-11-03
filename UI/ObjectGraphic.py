import pygame
from config import UIConfig

class ObjectGraphic:
    def __init__(self, position, img_path):
        self.position = position
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (UIConfig.TILE_SIZE, UIConfig.TILE_SIZE))
        self.screen_position = [position[1] * UIConfig.TILE_SIZE + UIConfig.OFFSET_X, position[0] * UIConfig.TILE_SIZE + UIConfig.OFFSET_Y]
        
    def draw(self, surface):
        surface.blit(self.image, (self.screen_position[0], self.screen_position[1]))
        