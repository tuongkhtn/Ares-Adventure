import sys
import pygame
from config import UIConfig
from utils import GameObject
from utils import Action
from utils import Utilities

class GameGraphic:
    def __init__(self, gameObject: GameObject):
        # Init game
        pygame.init()
        self.screen = pygame.display.set_mode((UIConfig.WINDOW_WIDTH, UIConfig.WINDOW_HEIGHT))
        pygame.display.set_caption(UIConfig.CAPTION)
        self.font = pygame.font.Font(None, UIConfig.FONT_SIZE)
        
        # Init object
        self.gameObject = gameObject.addUI()
        
        self.clock = pygame.time.Clock()
        self.running = True

    def draw_all(self):
        self.gameObject.draw(self.screen)
        # for button in self.buttons:
        #     button.draw(self.screen)
        
    def run(self):
        movement_delay = 100
        last_move_time = pygame.time.get_ticks()
        while self.running:
            self.screen.fill(UIConfig.COLOR_BG)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if pygame.time.get_ticks() - last_move_time > movement_delay:
                        posOfAres = self.gameObject.ares.getCoordinate()
                        posOfStones = [stone.getCoordinate() for stone in self.gameObject.stones]
                        posOfWalls = [wall.getCoordinate() for wall in self.gameObject.walls]
                        
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
                            newPosOfAres, newPosOfStones, _ = Utilities.updateState(posOfAres, posOfStones, action)
                            self.gameObject.ares.setCoordinate(newPosOfAres[0], newPosOfAres[1])
                            print(self.gameObject.ares.getCoordinate())
                            for i in range(len(newPosOfStones)):
                                self.gameObject.stones[i].setCoordinate(newPosOfStones[i][0], newPosOfStones[i][1])                            
            self.gameObject.ares.move()
            for stone in self.gameObject.stones:
                stone.move()
            self.draw_all()
                                    
            pygame.display.update() # Cập nhật màn hình sau khi vẽ
            self.clock.tick(60)  # Giới hạn FPS của trò chơi