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
    
    beginPosAres = posOfAres(gameState)
    beginPosAndWeightStones = posAndWeightOfStones(gameState)
    startState = (beginPosAres, beginPosAndWeightStones)
    
    frontier = PriorityQueue() # frontier save states
    frontier.push([startState], 0)
    
    actions = PriorityQueue() # actions store (totalWeight, path), cost
    actions.push((0, ''), float('inf'))
    
    exploredSet = CustomSet() # save state appeared
    
    posWalls = posOfWalls(gameState)
    posSwitches = posOfSwitches(gameState)
    
    totalWeightAndPath = ""
    minCost = 0
    
    numberOfNodes = 1
    
    while not frontier.isEmpty():
        # print("Loop:", cnt + 1)
        node = frontier.pop()
        node_action = actions.pop()
        # print("Node: ", node)
        # print("Node action:", node_action)
        
        posOfStonesLastState = [x[:2] for x in node[-1][-1]]
        
        if isEndState(posOfStonesLastState, posSwitches):
            minCost = costFunction(node_action)
            totalWeightAndPath = node_action
            break
        
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            # print("Actions:")
            for action in validActionsInNextStep(node[-1][0], node[-1][1], posWalls):
                newState = updateState(node[-1][0], node[-1][1], action) 
                # print(action)
                # print(newState)
                
                if isFailed(newState[1], posWalls, posSwitches):
                   continue
                
                addWeightAndPath = (node_action[0] + action[2], node_action[1] + action[-1])
                cost = costFunction(addWeightAndPath)  
                frontier.push(node + [newState], cost)
                actions.push(addWeightAndPath, cost)   
                numberOfNodes += 1 
        
        # print("Push actions:")
        # printQueue(actions)
        
        # print("Push state:")
        # printQueue(frontier)
        
        # print("######################################################################################\n")
        
        # cnt += 1
    
    path = totalWeightAndPath[1]
    numberOfSteps = len(path)
    totalWeight = totalWeightAndPath[0]
    return numberOfSteps, totalWeight, numberOfNodes, path