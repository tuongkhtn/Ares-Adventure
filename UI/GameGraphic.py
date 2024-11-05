import sys
import pygame
from config import UIConfig
from utils import GameObject
from utils import Action
from utils import Utilities
from .GameEvent import GameEvent
from utils import Button

class GameGraphic:
    def __init__(self, gameObject: GameObject):
        # Init game
        pygame.init()
        self.screen = pygame.display.set_mode((UIConfig.WINDOW_WIDTH, UIConfig.WINDOW_HEIGHT))
        pygame.display.set_caption(UIConfig.CAPTION)
        self.font = pygame.font.Font(None, UIConfig.FONT_SIZE)
        
        # Init object
        self.gameObject = gameObject.addUI()
        self.gameEvent = GameEvent(self.gameObject)

        self.buttons = []
        button = Button(500, 400, UIConfig.PLAY_BUTTON_COLOR, UIConfig.PLAY_BUTTON_TEXT)
        self.buttons.append(button)
        # playbutton = PlayButton(500, 400)
        # self.buttons.append(playbutton)
        
        self.clock = pygame.time.Clock()
        self.running = True

    def draw_all(self):
        self.gameObject.draw(self.screen)
        # [button.draw(self.screen) for button in self.button]
        
    def run(self):
        while self.running:
            self.screen.fill(UIConfig.COLOR_BG)
            self.draw_all()
            pygame.display.flip()
            self.clock.tick(60)
            
            for event in pygame.event.get():
                self.running, self.gameObject = self.gameEvent.run(event)
                            
                                    
        pygame.quit()
        sys.exit()