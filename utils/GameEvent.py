import pygame
from config import UIConfig
from utils import GameObject

class GameEvent(GameObject):
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((UIConfig.WINDOW_WIDTH, UIConfig.WINDOW_HEIGHT))
        
