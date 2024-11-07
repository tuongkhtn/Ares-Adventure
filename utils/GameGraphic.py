import pygame
from config import UIConfig
from utils import GameObject
from utils import Action
from utils import Utilities
from utils import Button, PlayButton, ResetButton, Alert
from config.ImageConfig import ImageConfig
from utils.LevelButton import LevelButton

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
        self.background_image = pygame.image.load(str(ImageConfig.IMAGE_BG))
        self.background_image = pygame.transform.scale(self.background_image, (UIConfig.WINDOW_WIDTH, UIConfig.WINDOW_HEIGHT))
        self.background_image.set_alpha(UIConfig.ALPHA)
        self.current_level = "1"
        
        # Init game state
        self.running = True
        self.is_in_algorithm = False
        self.current_algorithm_index = 0
        self.show_algorithm_list = False
        self.result_game = 0
        self.is_searching = False
        self.show_level_choice = False

        # Init object
        self.gameObject = gameObject.addUI()

        # Init button

        self.buttons = []
        self.buttons.append(PlayButton(y=10, x=UIConfig.WINDOW_WIDTH - 150))
        self.buttons.append(ResetButton(y=60, x=UIConfig.WINDOW_WIDTH - 150))
        self.buttons.append(Button(y=10, x=UIConfig.WINDOW_WIDTH - 250, text=algorithms[self.current_algorithm_index], color=UIConfig.CHOICE_BUTTON_COLOR))
        self.buttons[2].setTextColor(UIConfig.CHOICE_BUTTON_TEXT_COLOR)
        self.buttons.append(LevelButton(y=10, x=UIConfig.WINDOW_WIDTH - 350))
        self.algorithms_buttons = [Button(y=10 + 40 * (i + 1), x=UIConfig.WINDOW_WIDTH - 250, text=algorithms[i], color=UIConfig.OPTION_BUTTON_COLOR, corner_radius=0) for i in range(len(algorithms))]
        self.level_buttons = [Button(UIConfig.WINDOW_WIDTH // 4 + 25 + 90 * (i % 5), UIConfig.WINDOW_HEIGHT // 4 + 100 + (i // 5) * 100, UIConfig.OPTION_BUTTON_COLOR, f"Level {i + 1}") for i in range(10)]
        self.level_buttons.append(Button(x=UIConfig.WINDOW_WIDTH * 3 // 4 - 30, y=UIConfig.WINDOW_HEIGHT // 4 + 5, color=(0,0,0), text="X", height=20, width=20))

        self.alert = Alert.ALert()
        self.clock = pygame.time.Clock()


    def draw_all(self):
        self.gameObject.draw(self.screen)
        [button.draw(self.screen) for button in self.buttons]
        if self.show_algorithm_list:
            [button.draw(self.screen) for button in self.algorithms_buttons]
        steps_text = UIConfig.STATS_FONT.render(f"Step: {self.gameObject.stepCount}", True, (255, 255, 255))
        weight_text = UIConfig.STATS_FONT.render(f"Weight: {self.gameObject.totalWeight}", True, (255, 255, 255))
        level_text = UIConfig.STATS_FONT.render(f"Level {self.current_level}", True, (255, 255, 255))

        self.screen.blit(steps_text, (40, 10))
        self.screen.blit(weight_text, (40, 40))
        self.screen.blit(level_text, (UIConfig.WINDOW_WIDTH // 2 - 30, 20))

    
        if self.is_in_algorithm and self.is_searching:
            self.alert.setText("SEARCHING...", (0, 0, 255))
            self.alert.draw(self.screen)
        elif self.result_game == -1:
            self.alert.setText("FAILED", (255, 0, 0))
            self.alert.draw(self.screen)
        elif self.result_game == 1:
            self.alert.setText("SUCCESS", (45, 200, 12))
            self.alert.draw(self.screen)
        
    def run(self):
        while self.running:
            self.screen.fill(UIConfig.COLOR_BG)
            self.screen.blit(self.background_image, (0, 0))
            
            posOfAres = self.gameObject.ares.getCoordinate()
            posOfStones = [stone.getCoordinate() for stone in self.gameObject.stones]
            posOfWalls = [wall.getCoordinate() for wall in self.gameObject.walls]
            posOfSwitches = [switch.getCoordinate() for switch in self.gameObject.switches]

            self.is_searching = self.buttons[0].is_searching
            self.is_in_algorithm = self.buttons[0].is_in_algorithm
            if self.is_in_algorithm:
                self.result_game = self.buttons[0].game_result
                
            if Utilities.isEndState(posOfStones, posOfSwitches):
                self.result_game = 1
            elif Utilities.isFailed(posOfStones, posOfSwitches, posOfWalls):
                self.result_game = -1  
                          
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.is_in_algorithm:
                        self.is_in_algorithm = False
                        self.buttons[0].setIsInAlgorithm(self.is_in_algorithm)
                    self.running = False
                    pygame.quit()
                    return
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
                    else:
                        continue

                    
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
                        algo_thread = threading.Thread(target=self.buttons[0].handle, args=([copy.deepcopy(self.gameObject), running_algo]))
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
                            self.buttons[0].resetMemAndTime()
                        self.buttons[0].algo_time = 0
                        self.buttons[1].memory = 0
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
                    # Level Button
                    if self.buttons[3].rect.collidepoint(mouse_pos):
                        self.show_level_choice = not self.show_level_choice
                    
                    if self.show_level_choice and self.level_buttons[len(self.level_buttons) - 1].rect.collidepoint(mouse_pos):
                        self.show_level_choice = False

                    for i in range(len(self.level_buttons) - 1):
                        if self.level_buttons[i].rect.collidepoint(mouse_pos):
                            filename = ""
                            if i + 1 < 10:
                                filename = "input-0" + str(i + 1) + ".txt"
                            else:
                                filename = "input-" + str(i + 1) + ".txt"
                            self.gameObject = GameObject(filename)
                            self.show_level_choice = False
                            self.current_level = i + 1
                            self.gameObject = self.gameObject.addUI()
                            self.draw_all()

            self.gameObject.ares.move()
            for stone in self.gameObject.stones:
                stone.move()
            self.draw_all()

            if self.show_level_choice:
                self.buttons[3].handle(self.screen, self.level_buttons)
                                    
            pygame.display.update() 
            self.clock.tick(60) 