from utils import readCommand
from utils import transferToGameState
from algorithms import uniformCostSearch, aStarSearch
import time
import tracemalloc
from algorithms.astar import aStarSearch
import time

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
        steps, weight, nodes, path = uniformCostSearch(gameState)
    elif method == 'astar':
        aStarSearch(gameState)
        
    end = time.time()
        
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(method.upper())
    print(f"Steps: {steps}, Weight: {weight}, Node: {nodes}, Time (ms): {(end-start):.2f}, Memory (MB): {current / 10**6:.2f}")
    print(path)
