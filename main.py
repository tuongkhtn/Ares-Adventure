from utils import readCommand
from utils import transferToGameState
from utils import posOfAres, posAndWeightOfStones, posOfSwitches, posOfWalls
from utils import isEndState
from utils import validActionsInNextStep
from utils import updateState
from algorithms.ucs import uniformCostSearch
from algorithms.astar import aStarSearch
from utils import PriorityQueue
from utils import costFunction
import time

if __name__ == '__main__':
    weights, maze = readCommand()
    print("weights: ", weights)
    print("maze: ", maze)
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


