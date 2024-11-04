import copy

from utils import PriorityQueue
from utils import costFunction
from utils import CustomSet
from utils import GameObject
from utils import GameState
from utils import Utilities

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
    
    posOfAres = gameObject.positionOfAres()
    posOfStones = gameObject.positionOfStones()
    posOfWalls = gameObject.positionOfWalls()
    posOfSwitches = gameObject.positionOfSwitches()
    
    openSet = PriorityQueue() # openSet save states
    openSet.push([(posOfAres, posOfStones)], 0)
    
    actions = PriorityQueue() # actions store (totalWeight, path), cost
    actions.push((0, ''), float('inf'))
    
    exploredSet = CustomSet() # save state appeared
    
    
    while not openSet.isEmpty():
        
        node = openSet.pop() # List[Tuple(PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]])]
        node_action = actions.pop() # Tuple(total weight: int, path: str)


        # print("node: ", node)
        # print("node_action: ", node_action)


        if Utilities.isEndState(node[-1][-1], posOfSwitches):
            finalWeight = node_action[0]
            finalPath = node_action[1]
            finalNumberOfSteps = len(node_action[1])
            finalStates = node
            break
        
        
        if node[-1] not in exploredSet:
            # print("node[-1]: ", node[-1])
            exploredSet.add(node[-1])

            for valid_action in Utilities.validActionsInNextStep(node[-1][0], node[-1][1], posWalls):  # action Tuple[X: int, Y: int,  stoneWeight: int, command: str]
                # print("valid_action: ", valid_action)
                newState = updateState(node[-1][0], node[-1][1], valid_action)  # newState Tuple[PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]]]
                # print("newState: ", newState)

                if isFailed(posAndWeightStones=newState[1], posWalls=posWalls, posSwitches=posSwitches):
                    continue
                
                heuristic_hx = heuristic(posSwitches, newState[1])
                
                cost_gx = costFunction((node_action[0] + valid_action[2], node_action[1] + valid_action[-1]))
                cost_fx = heuristic_hx + cost_gx

                openSet.push(node + [newState], cost_fx)
                actions.push((node_action[0] + valid_action[2], node_action[1] + valid_action[-1]), cost_fx) 

                numberOfNodes+=1
        
    return finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates