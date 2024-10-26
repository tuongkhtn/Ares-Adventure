from utils import readCommand
from utils import transferToGameState, saveStates
from algorithms import uniformCostSearch, aStarSearch
from algorithms.dfs import depthFirstSearch
from algorithms.bfs import breadthFirstSearch
import time
import tracemalloc
import psutil
import os

if __name__ == '__main__':
    # tracemalloc.start()
    start = time.time()

    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss / 1024
    
    weights, maze, method, level = readCommand()
    gameState = transferToGameState(weights, maze)
    
    
    if method == 'dfs':
        finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates = depthFirstSearch(gameState)
    elif method == 'bfs':
        finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates = breadthFirstSearch(gameState)
    elif method == 'ucs':
        finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates = uniformCostSearch(gameState)
    elif method == 'astar':
        finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates = aStarSearch(gameState)
        
    end = time.time()
    memory_after = process.memory_info().rss / 1024
    current = memory_after - memory_before
    # current, peak = tracemalloc.get_traced_memory()
    # tracemalloc.stop()
    
    
    print(method.upper())
    print(f"Steps: {finalNumberOfSteps}, Weight: {finalWeight}, Node: {numberOfNodes}, Time (ms): {(end-start):.2f}, Memory (MB): {current / 10**6:.2f}")
    print(f"Path: {finalPath}")
    
    # fileName = level.split('.')[0]
    # saveStates(finalStates, directory="output", filename=f"{fileName}_{method}_states.csv")
