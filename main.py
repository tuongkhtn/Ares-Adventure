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


    aStarSearch(gameState)

    # posStones = [x[:2] for x in posAndWeightOfStones(gameState)]
    
    # print("Maze:\n", gameState[1])
    # print("Position of Ares: ", posAres)
    # print("Position of Stones: ", posAndWeightStones)
    # print("Position of Switches: ", posSwitches)
    # print("Position of Walls: ", posWalls)
    
    # print("End state: ", isEndState(posStones, posSwitches))
    
    # validActions = validActionsInNextStep(posAres, posAndWeightStones, posWalls)
    # print("Valid actions: ", validActions)
    
    # nextPosOfAres, newPosAndWeightStones = updateState(posAres, posAndWeightStones, (0, -1, 1, 'L'))
    # print("Next position of Ares: ", nextPosOfAres)
    # print("New position and weight of stones: ", newPosAndWeightStones)
    

