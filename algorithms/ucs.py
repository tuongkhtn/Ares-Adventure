import copy

from utils import PriorityQueue
from utils import costFunction
from utils import CustomSet
from utils import GameObject
from utils import GameState

def printQueue(actions):
    import copy
    
    actions_copy = copy.deepcopy(actions)
    while not actions_copy.isEmpty():
        print(actions_copy.pop())

def uniformCostSearch(gameObject: GameObject):
    """
    Performs the Uniform Cost Search algorithm to find the optimal path for Ares to reach
    the goal state.
    
    Args:
        gameState (Tuple[List[int], np.ndarray): A tuple containing:
            - List[int]: The weights of the stones.
            - np.ndarray: A 2D grid representing the maze.
    
    Returns:
        numberOfSteps (int): The number of steps in the solution path.
        totalWeight (int): The total weight accumulated along the solution path.
        numberOfNodes (int): The total number of nodes expanded during the search.
        path (str): A string representing the sequence of actions taken in the solution path.
    """
    
    finalWeight = -1
    finalPath = ""
    finalNumberOfSteps = -1
    numberOfNodes = 1
    
    posOfWalls = gameObject.positionOfWalls()
    posOfSwitches = gameObject.positionOfSwitches()
    
    openSet = PriorityQueue() # openSet save states
    openSet.push([GameState(gameObject.ares, gameObject.stones)], 0)
    
    actions = PriorityQueue() # actions store (totalWeight, path), cost
    actions.push((0, ''), float('inf'))
    
    exploredSet = CustomSet() # save state appeared
    
    
    while not openSet.isEmpty():
        node = openSet.pop()
        node_action = actions.pop()
                
        if node[-1].isEndState(posOfSwitches):
            finalWeight = node_action[0]
            finalPath = node_action[1]
            finalNumberOfSteps = len(finalPath)
            break
        
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])

            for validAction in node[-1].validActionsInNextStep(posOfWalls):
                newState = copy.deepcopy(node[-1])
                newState.updateState(validAction) 
                
                if newState.isFailed(posOfSwitches, posOfWalls):
                   continue
                
                addWeightAndPath = (node_action[0] + validAction.getWeight(), node_action[1] + validAction.getDirection())
                cost = costFunction(addWeightAndPath)  
                openSet.push(node + [newState], cost)
                actions.push(addWeightAndPath, cost)   
                numberOfNodes += 1 
    
    return finalWeight, finalPath, finalNumberOfSteps, numberOfNodes