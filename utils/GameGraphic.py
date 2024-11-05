import sys
import pygame
from config import UIConfig
from utils import GameObject
from utils import Action
from utils import Utilities
from utils import GameEvent
from utils import Button, PlayButton, ResetButton, PauseButton

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
        self.buttons.append(PlayButton(500, 400))
        
        self.clock = pygame.time.Clock()
        self.running = True

    def draw_all(self):
        self.gameObject.draw(self.screen)
        [button.draw(self.screen) for button in self.buttons]
        
    def run(self):
        while self.running:
            self.screen.fill(UIConfig.COLOR_BG)
            self.draw_all()
            pygame.display.flip()
            self.clock.tick(60)

            posOfAres = self.gameObject.ares.getCoordinate()
            posOfStones = [stone.getCoordinate() for stone in self.gameObject.stones]
            posOfWalls = [wall.getCoordinate() for wall in self.gameObject.walls]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    action = Action('n')
                    if event.key == pygame.K_LEFT:
                        action.setDirection('l')
                    elif event.key == pygame.K_RIGHT:
                        action.setDirection('r')
                    elif event.key == pygame.K_UP:
                        action.setDirection('u')
                    elif event.key == pygame.K_DOWN:
                        action.setDirection('d')
                    
                    if Utilities.isPushStone(posOfAres, posOfStones, action):
                        action.setDirection(action.getDirection().upper())
                        print(action.getDirection())
                    
                    if Utilities.isValidAction(posOfAres, posOfStones, posOfWalls, action):
                        newPosOfAres, newPosOfStones = Utilities.updateState(posOfAres, posOfStones, action)
                        self.gameObject.ares.setCoordinate(newPosOfAres[0], newPosOfAres[1])
                        print(self.gameObject.ares.getCoordinate())
                        for i in range(len(newPosOfStones)):
                            self.gameObject.stones[i].setCoordinate(newPosOfStones[i][0], newPosOfStones[i][1])

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                            
                                    
        pygame.quit()
        sys.exit()