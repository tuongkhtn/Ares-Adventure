from utils import readCommand
from utils import transferToGameState
from utils import posOfAres, posAndWeightOfStones, posOfSwitches, posOfWalls
from utils import isEndState
from utils import validActionsInNextStep
from utils import updateState
from algorithms import uniformCostSearch
from utils import PriorityQueue
from utils import costFunction
import time

if __name__ == '__main__':
    # weights, maze = readCommand()
    # gameState = transferToGameState(weights, maze)
    
    # posAres = posOfAres(gameState)
    # posAndWeightStones = posAndWeightOfStones(gameState)
    # posSwitches = posOfSwitches(gameState)
    # posWalls = posOfWalls(gameState)
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
    
    
    # a = (0, 'ab')
    # b = (0, 'ba')
    # print(costFunction(a))
    # print(costFunction(b))
    
    # actions = PriorityQueue()
    # actions.push((0, 'd'), 2000.0)
    # actions.push((0, 'u'), 2017.0)
    # actions.push((99, 'R'), 1917.0)
    
    # while not actions.isEmpty():
    #     print(actions.pop())
    
    start = time.time()
    weights, maze = readCommand()
    gameState = transferToGameState(weights, maze)
    
    uniformCostSearch(gameState)
    
    print("Time: ", time.time() - start)
    
    