from utils import PriorityQueue
from utils import posOfAres, posAndWeightOfStones, posOfSwitches, posOfWalls
from utils import isEndState
from utils import costFunction
from utils import validActionsInNextStep
from utils import updateState
from utils import CustomSet
from utils import isFailed

def printQueue(actions):
    import copy
    
    actions_copy = copy.deepcopy(actions)
    while not actions_copy.isEmpty():
        print(actions_copy.pop())

def uniformCostSearch(gameState):
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
    finalStates = []
    numberOfNodes = 1

    startPosAres = posOfAres(gameState)
    startStones = posAndWeightOfStones(gameState)
    startState = (startPosAres, startStones)
    posSwitches = posOfSwitches(gameState)
    posWalls = posOfWalls(gameState)
    
    openSet = PriorityQueue() # openSet save states
    openSet.push([startState], 0)
    
    actions = PriorityQueue() # actions store (totalWeight, path), cost
    actions.push((0, ''), float('inf'))
    
    exploredSet = CustomSet() # save state appeared
    
    
    while not openSet.isEmpty():
        # print("Loop:", cnt + 1)
        node = openSet.pop()
        node_action = actions.pop()
        # print("Node: ", node)
        # print("Node action:", node_action)
        
        posOfStonesLastState = [x[:2] for x in node[-1][-1]]
        
        if isEndState(posOfStonesLastState, posSwitches):
            finalWeight = node_action[0]
            finalPath = node_action[1]
            finalNumberOfSteps = len(node_action[1])
            finalStates = node
            break
        
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            # print("Actions:")
            for valid_action in validActionsInNextStep(node[-1][0], node[-1][1], posWalls):
                newState = updateState(node[-1][0], node[-1][1], valid_action) 
                # print(valid_action)
                # print(newState)
                
                if isFailed(newState[1], posWalls, posSwitches):
                   continue
                
                addWeightAndPath = (node_action[0] + valid_action[2], node_action[1] + valid_action[-1])
                cost = costFunction(addWeightAndPath)  
                openSet.push(node + [newState], cost)
                actions.push(addWeightAndPath, cost)   
                numberOfNodes += 1 
        
        # print("Push actions:")
        # printQueue(actions)
        
        # print("Push state:")
        # printQueue(openSet)
        
        # print("######################################################################################\n")
        
        # cnt += 1
    
    return finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates