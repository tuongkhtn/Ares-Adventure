# from utils import readCommand
# from utils import transferToGameState, saveStates
# from algorithms import uniformCostSearch, aStarSearch
# from algorithms.dfs import depthFirstSearch
# from algorithms.bfs import breadthFirstSearch
# import time
# import tracemalloc
# import psutil
# import os

# if __name__ == '__main__':
#     # tracemalloc.start()
#     start = time.time()

#     process = psutil.Process(os.getpid())
#     memory_before = process.memory_info().rss / 1024
    
#     weights, maze, method, level = readCommand()
#     print(weights)
#     print(maze)
#     gameState = transferToGameState(weights, maze)
    
#     print(gameState[-1])
    
#     tmp = gameState[-1]
#     tmp = [x.strip() for x in tmp]
#     print(tmp)
    
    
#     # if method == 'dfs':
#     #     finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates = depthFirstSearch(gameState)
#     # elif method == 'bfs':
#     #     finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates = breadthFirstSearch(gameState)
#     # elif method == 'ucs':
#     #     finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates = uniformCostSearch(gameState)
#     # elif method == 'astar':
#     #     finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates = aStarSearch(gameState)
        
#     # end = time.time()
#     # memory_after = process.memory_info().rss / 1024
#     # current = memory_after - memory_before
#     # # current, peak = tracemalloc.get_traced_memory()
#     # # tracemalloc.stop()
    
    
#     # print(method.upper())
#     # print(f"Steps: {finalNumberOfSteps}, Weight: {finalWeight}, Node: {numberOfNodes}, Time (ms): {(end-start):.2f}, Memory (MB): {current / 10**6:.2f}")
#     # print(f"Path: {finalPath}")
    
#     # # fileName = level.split('.')[0]
#     # # saveStates(finalStates, directory="output", filename=f"{fileName}_{method}_states.csv")

#     # print(finalStates)


import numpy as np
from utils.GameObject import GameObject
from utils.Ares import Ares
from utils.Action import Action
from algorithms.ucs import uniformCostSearch
from utils.GameState import GameState
from UI.GameGraphic import GameGraphic
import pygame

if __name__ == "__main__":
    gameObject = GameObject("input-01.txt")
    
    # finalWeight, finalPath, finalNumberOfSteps, numberOfNodes = uniformCostSearch(gameObject)
    
    gameGraphic = GameGraphic(gameObject)
    gameGraphic.run()
    # pygame.init()
    # screen = pygame.display.set_mode((800, 600))  # Kích thước cửa sổ tùy chỉnh
    # pygame.display.set_caption("Game Window")
    # print(gameObject.ares.addUI())