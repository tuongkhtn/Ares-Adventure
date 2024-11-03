import sys
import pygame
from config import UIConfig
from utils import GameObject
from utils import Ares, Stone, Wall, FreeSpace, Switch

class GameGraphic:
    def __init__(self, gameObject: GameObject):
        # Init game
        pygame.init()
        self.screen = pygame.display.set_mode((UIConfig.WINDOW_WIDTH, UIConfig.WINDOW_HEIGHT))
        pygame.display.set_caption(UIConfig.CAPTION)
        self.font = pygame.font.Font(None, 24)
        
        # Init object
        self.initObject(gameObject)
        
        self.clock = pygame.time.Clock()
        self.running = True
        
    def initObject(self, gameObject: GameObject):
        self.ares = gameObject.ares.addUI()
        self.stones = [stone.addUI() for stone in gameObject.stones]
        self.walls = [wall.addUI() for wall in gameObject.walls]
        self.switches = [switch.addUI() for switch in gameObject.switches]
        self.freeSpaces = [freeSpace.addUI() for freeSpace in gameObject.freeSpaces]
        
    def draw_all(self):
        for freeSpace in self.freeSpaces:
            freeSpace.draw(self.screen)
        
        self.ares.draw(self.screen)
        
        for stone in self.stones:
            stone.draw(self.screen)
            
        for wall in self.walls:
            wall.draw(self.screen)
            
        for switch in self.switches:
            switch.draw(self.screen)
        
    def run(self):
        while self.running:
            self.screen.fill(UIConfig.COLOR_BG)
            self.draw_all()
            pygame.display.flip()
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
        pygame.quit()
        sys.exit()