from utils import readCommand
from utils import transferToGameState
from algorithms.ucs import uniformCostSearch
import time
from algorithms.astar import aStarSearch
from utils import PriorityQueue
from utils import costFunction
import time

if __name__ == '__main__':
    start = time.time()
    weights, maze = readCommand()
    gameState = transferToGameState(weights, maze)
    print("gameState: ", gameState)
    posAres = posOfAres(gameState)
    print("posAres: ", posAres)
    posAndWeightStones = posAndWeightOfStones(gameState)
    print("posAndWeightStones: ", posAndWeightStones)
    posSwitches = posOfSwitches(gameState)
    print("posSwitches: ", posSwitches)
    posWalls = posOfWalls(gameState)
    print("posWalls: ", posWalls)

    start = time.time()
    uniformCostSearch(gameState)
    end = time.time()
    print("UCS time: ", end - start)
    start = time.time()
    aStarSearch(gameState)
    end = time.time()
    print("A* time: ", end - start)


