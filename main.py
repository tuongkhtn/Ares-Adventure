from utils import readCommand
from utils import transferToGameState
from algorithms.ucs import uniformCostSearch
import time

if __name__ == '__main__':
    start = time.time()
    weights, maze = readCommand()
    gameState = transferToGameState(weights, maze)
    
    uniformCostSearch(gameState)
    
    print("Time: ", time.time() - start)