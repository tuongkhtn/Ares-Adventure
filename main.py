from utils import readCommand
from utils import transferToGameState
from algorithms import uniformCostSearch, aStarSearch
import time
import tracemalloc

if __name__ == '__main__':
    tracemalloc.start()
    start = time.time()
    
    weights, maze, method = readCommand()
    gameState = transferToGameState(weights, maze)
        
    if method == 'dfs':
        print('dfs')
    elif method == 'bfs':
        print('bfs')
    elif method == 'ucs':
        finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates = uniformCostSearch(gameState)
    elif method == 'astar':
        finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates = aStarSearch(gameState)
        
    end = time.time()
        
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(method.upper())
    print(f"Steps: {finalNumberOfSteps}, Weight: {finalWeight}, Node: {numberOfNodes}, Time (ms): {(end-start):.2f}, Memory (MB): {current / 10**6:.2f}")
    print(f"Path: {finalPath}")