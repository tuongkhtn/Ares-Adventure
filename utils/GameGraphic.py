import sys
import pygame
from config import UIConfig
from utils import GameObject
from utils import Action
from utils import Utilities
from utils import Button, PlayButton, ResetButton, PauseButton
from utils.ChoiceButton import ChoiceButton

from algorithms.astar import aStarSearch
from algorithms.bfs import breadthFirstSearch
from algorithms.dfs import depthFirstSearch
from algorithms.ucs import uniformCostSearch
import threading
import copy

algorithms = ["DFS", "BFS", "UCS", "A*"]
search_functions = {
    "DFS": depthFirstSearch,
    "BFS": breadthFirstSearch,
    "UCS": uniformCostSearch,
    "A*": aStarSearch
}

class GameGraphic:
    def __init__(self, gameObject: GameObject):
        # Init game
        pygame.init()
        self.screen = pygame.display.set_mode((UIConfig.WINDOW_WIDTH, UIConfig.WINDOW_HEIGHT))
        pygame.display.set_caption(UIConfig.CAPTION)
        self.font = pygame.font.Font(None, UIConfig.FONT_SIZE)
        
        # Init game state
        self.running = True
        self.is_in_algorithm = False
        self.current_algorithm_index = 0
        self.show_algorithm_list = False
        self.result_game = 0
        self.is_searching = False
        

        # Init object
        self.gameObject = gameObject.addUI()

        self.buttons = []
        self.buttons.append(PlayButton(y=10, x=UIConfig.WINDOW_WIDTH - 150))
        self.buttons.append(ResetButton(y=60, x=UIConfig.WINDOW_WIDTH - 150))
        self.buttons.append(ChoiceButton(y = 10, x=UIConfig.WINDOW_WIDTH - 250, text=algorithms[self.current_algorithm_index]))
        self.algorithms_buttons = [ChoiceButton(y=10 + 40 * (i + 1), x=UIConfig.WINDOW_WIDTH - 250, text=algorithms[i], color=UIConfig.OPTION_BUTTON_COLOR) for i in range(len(algorithms))]
        
        self.clock = pygame.time.Clock()


    def draw_all(self):
        self.gameObject.draw(self.screen)
        [button.draw(self.screen) for button in self.buttons]
        if self.show_algorithm_list:
            [button.draw(self.screen) for button in self.algorithms_buttons]
        steps_text = UIConfig.STATS_FONT.render(f"Step: {self.gameObject.stepCount}", True, (0, 0, 0))
        weight_text = UIConfig.STATS_FONT.render(f"Weight: {self.gameObject.totalWeight}", True, (0, 0, 0))
        self.screen.blit(steps_text, (40, 10))
        self.screen.blit(weight_text, (40, 40))

        if self.is_in_algorithm and self.is_searching:
            message = UIConfig.MSS_FONT.render(f"SEARCHING", True, (255, 255, 0))
            self.screen.blit(message, (250, 20))
        elif self.result_game == -1:
            message = UIConfig.MSS_FONT.render(f"FAIL", True, (255, 0, 0))
            self.screen.blit(message, (250, 20))
        elif self.result_game == 1:
            message = UIConfig.MSS_FONT.render(f"SUCCESS", True, (0, 255, 0))
            self.screen.blit(message, (250, 20))
        
    def run(self):
        while self.running:
            self.screen.fill(UIConfig.COLOR_BG)
            
            posOfAres = self.gameObject.ares.getCoordinate()
            posOfStones = [stone.getCoordinate() for stone in self.gameObject.stones]
            posOfWalls = [wall.getCoordinate() for wall in self.gameObject.walls]
            posOfSwitches = [switch.getCoordinate() for switch in self.gameObject.switches]

            self.is_searching = self.buttons[0].is_searching
            self.is_in_algorithm = self.buttons[0].is_in_algorithm
            if self.is_in_algorithm:
                self.result_game = self.buttons[0].game_result
                
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.is_in_algorithm:
                        self.is_in_algorithm = False
                        self.buttons[0].setIsInAlgorithm(self.is_in_algorithm)
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
                    
                    if Utilities.isValidAction(posOfAres, posOfStones, posOfWalls, action):
                        newPosOfAres, newPosOfStones, index = Utilities.updateState(posOfAres, posOfStones, action)
                        self.gameObject.ares.setCoordinate(newPosOfAres[0], newPosOfAres[1])

                        self.gameObject.stepCount += 1
                        if index != None:
                            self.gameObject.totalWeight += self.gameObject.stones[index].getWeight()

                        for i in range(len(newPosOfStones)):
                            self.gameObject.stones[i].setCoordinate(newPosOfStones[i][0], newPosOfStones[i][1])

                    if Utilities.isEndState(posOfStones, posOfSwitches):
                        self.result_game = 1
                    elif Utilities.isFailed(posOfStones, posOfSwitches, posOfWalls):
                        self.result_game = -1

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # PlayButton
                    if self.buttons[0].rect.collidepoint(mouse_pos):
                        if self.is_in_algorithm:
                            self.is_in_algorithm = False
                            self.buttons[0].setIsInAlgorithm(self.is_in_algorithm)
                            continue
                        self.is_in_algorithm = True
                        self.buttons[0].setIsInAlgorithm(self.is_in_algorithm)
                        running_algo = search_functions[algorithms[self.current_algorithm_index]]
                        algo_thread = threading.Thread(target=self.buttons[0].handleClick, args=([copy.deepcopy(self.gameObject), running_algo]))
                        algo_thread.start()
                    # ResetButton
                    if self.buttons[1].rect.collidepoint(mouse_pos):
                        self.result_game = 0

                        if self.is_in_algorithm:
                            self.is_in_algorithm = False
                            self.buttons[0].setIsInAlgorithm(self.is_in_algorithm)
                            self.buttons[0].setIsSearching(False)
                            self.buttons[0].setGameResult(0)
                            self.buttons[0].update_theme()
                        self.gameObject = self.buttons[1].handle(self.gameObject)
                        self.gameObject = self.gameObject.addUI()
                        self.draw_all()
                    # ChoiceButton
                    if self.buttons[2].rect.collidepoint(mouse_pos):
                        self.show_algorithm_list = not self.show_algorithm_list
                    if self.show_algorithm_list:
                        for i, button in enumerate(self.algorithms_buttons):
                            if button.rect.collidepoint(mouse_pos):
                                print(algorithms[i])
                                self.current_algorithm_index = i
                                self.buttons[2].setText(algorithms[i])
                                self.show_algorithm_list = False
                                break



                                    
            self.gameObject.ares.move()
            for stone in self.gameObject.stones:
                stone.move()
            self.draw_all()
                                    
            pygame.display.update() 
            self.clock.tick(60) 