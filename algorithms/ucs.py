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
    """_summary_
    
    Args:
        gameState (Tuple[List[int], np.ndarray): A tuple containing:
            - List[int]: The weights of the stones.
            - np.ndarray: A 2D grid representing the maze.
    """
    
    beginPosAres = posOfAres(gameState)
    beginPosAndWeightStones = posAndWeightOfStones(gameState)
    startState = (beginPosAres, beginPosAndWeightStones)
    
    frontier = PriorityQueue()
    frontier.push([startState], 0)
    
    actions = PriorityQueue() # actions store (totalWeight, path), cost
    actions.push((0, ''), float('inf'))
    
    exploredSet = CustomSet() # save state appeared
    
    posWalls = posOfWalls(gameState)
    posSwitches = posOfSwitches(gameState)
    
    minCost = float('inf')
    
    while not frontier.isEmpty():
        # print("Loop:", cnt + 1)
        node = frontier.pop()
        node_action = actions.pop()
        # print("Node: ", node)
        # print("Node action:", node_action)
        
        posOfStonesLastState = [x[:2] for x in node[-1][-1]]
        
        if isEndState(posOfStonesLastState, posSwitches):
            if minCost > costFunction(node_action):
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
                
                posOfNewStones = [x[:2] for x in newState[1]]
                if isFailed(posOfNewStones, posSwitches, posWalls):
                   continue
                
                addWeightAndPath = (node_action[0] + action[2], node_action[1] + action[-1])
                cost = costFunction(addWeightAndPath)  
                frontier.push(node + [newState], cost)
                actions.push(addWeightAndPath, cost)    
        
        # print("Push actions:")
        # printQueue(actions)
        
        # print("Push state:")
        # printQueue(frontier)
        
        # print("######################################################################################\n")
        
        # cnt += 1
    print("End: ", totalWeightAndPath)
    print("Cost: ", minCost)
    
        