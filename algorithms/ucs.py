from utils import PriorityQueue
from utils import posOfAres, posAndWeightOfStones, posOfSwitches, posOfWalls
from utils import isEndState
from utils import costFunction
from utils import validActionsInNextStep
from utils import updateState
from utils import CustomSet

def printActions(actions):
    while not actions.isEmpty():
        print(actions.pop())

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
    
    actions = PriorityQueue() # actions store (weight, action), cost
    actions.push((0, ''), float('inf'))
    
    exploredSet = CustomSet() # save state appeared
    
    posWalls = posOfWalls(gameState)
    posSwitches = posOfSwitches(gameState)
    
    cnt = 0
    
    while cnt < 2:
        node = frontier.pop()
        node_action = actions.pop()
        
        posOfStonesLastState = [x[:2] for x in node[-1][-1]]
        
        if isEndState(posOfStonesLastState, posSwitches):
            print("End: ", node_action)
            break
        
        print("Loop:", cnt + 1)
        
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            cost = costFunction(node_action)
            for action in validActionsInNextStep(node[-1][0], node[-1][1], posWalls):
                newState = updateState(node[-1][0], node[-1][1], action) 
                print(action)
                
                frontier.push(node + [newState], cost)
                actions.push((node_action[0] + action[2], node_action[1] + action[-1]), cost)    
        
        printActions(actions)
        
        cnt += 1
        