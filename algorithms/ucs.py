from utils import PriorityQueue
from utils import posOfAres, posAndWeightOfStones, posOfSwitches
from utils import isEndState
from utils import costFunction
from utils import validActionsInNextStep
from utils import updateState

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
    actions.push((0, ''), 0)
    
    exploredSet = set() # save state appeared
    
    while frontier:
        node = frontier.pop()
        node_action = actions.pop()
        
        posOfStonesLastState = [x[:2] for x in node[-1][-1]]
        
        if isEndState(posOfStonesLastState, posOfSwitches(gameState)):
            print("End: ", node_action)
            break
        
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            cost = costFunction(node_action)
            for action in validActionsInNextStep(node[-1][0], node[-1][1]):
                newState = updateState(node[-1][0], node[-1][1], action) 
                
                frontier.push(node + [newState], cost)
                actions.push((node_action[0] + action[0], node_action[1] + action[1]), cost)
    