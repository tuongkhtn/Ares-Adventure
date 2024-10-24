from utils import PriorityQueue
from utils import posOfAres, posAndWeightOfStones, posOfSwitches, posOfWalls
from utils import isEndState
from utils import costFunction
from utils import validActionsInNextStep
from utils import updateState
from utils import CustomSet
from scipy.optimize import linear_sum_assignment
import numpy as np
from utils import manhattanDistance
from utils import isFailed


def heuristic(switches, stones):
    """
    A heuristic function to calculate the overall distance between the else boxes and the else goals.

    Parameters
    ----------
    switches : List[Tuple[int, int]] The coordinates of the switches.
    stones : List[Tuple[int, int, int]] The coordinates and weights of the stones.

    Returns
    int: The overall distance between the else boxes and the else goals.
    """
    posStones = [x[:2] for x in stones]
    completes = set(switches) & set(posStones)
    sortedStones = list(set(posStones).difference(completes))
    sortedSwitches = list(set(switches).difference(completes))

    if not sortedStones or not sortedSwitches:
        return 0
    

    cost_matrix = np.zeros((len(sortedStones), len(sortedSwitches)))
    
    # Calculate the cost matrix
    for i in range(len(sortedStones)):
        for j in range(len(sortedSwitches)):
            weight = [stone[-1] for stone in stones if tuple(stone[:2]) == sortedStones[i]][0]
            cost_matrix[i][j] = manhattanDistance(sortedStones[i], sortedSwitches[j])*weight
    
    # Use linear_sum_assignment to find the optimal assignment
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    # Calculate the total distance
    total_distance = cost_matrix[row_ind, col_ind].sum()
    
    return total_distance


def aStarSearch(gameState):
    """
    Perform the A* search algorithm to find the optimal path from the start state to the end state.
    Args:
        gameState (Tuple[List[Stones's Weight: int], np.ndarray]): The initial game state containing stone weights and the maze layout.
    Return: 

    """
    startPosAres = posOfAres(gameState)
    startStones = posAndWeightOfStones(gameState)
    startState = (startPosAres, startStones)
    posSwitches = posOfSwitches(gameState)
    posWalls = posOfWalls(gameState)

    startState = (startPosAres, startStones) # Tuple(PosAres: Tuple(int, int), Stones: List[Stone: Tuple(X: int, Y: int, Weight: int)]))

    openSet = PriorityQueue() # PriorityQueue(State: Tuple(PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]]), Cost f(x): int)
    openSet.push([startState], 0)

    exploredSet = CustomSet()

    actions = PriorityQueue() # PriorityQueue(Tuple(total weight: int, path: str), value: int)
    actions.push((0, ''), float('inf')) 
    cnt = 0
    while not openSet.isEmpty():
        cnt+=1
        print("-"*100)
        print("Loop:", cnt)
        if (cnt > 20):
            break
        
        node = openSet.pop() # List[Tuple(PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]])]
        node_action = actions.pop() # Tuple(total weight: int, path: str)

        posOfStonesLastState = [x[:2] for x in node[-1][-1]]

        print("node: ", node)
        print("node_action: ", node_action)


        if isEndState(posOfStonesLastState, posSwitches):
            print("End: ", node_action)
            # for x in node:
            #     print(x)
            break
        
        
        if node[-1] not in exploredSet:
            print("node[-1]: ", node[-1])
            exploredSet.add(node[-1])

            for valid_action in validActionsInNextStep(node[-1][0], node[-1][1], posWalls):  # action Tuple[X: int, Y: int,  stoneWeight: int, command: str]
                print("valid_action: ", valid_action)
                newState = updateState(node[-1][0], node[-1][1], valid_action)  # newState Tuple[PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]]]
                print("newState: ", newState)
                if isFailed(stones=newState[1], posWalls=posWalls, posSwitches=posSwitches):
                    continue
                
                heuristic_hx = heuristic(posSwitches, newState[1])
                
                cost_gx = costFunction((node_action[0] + valid_action[2], node_action[1] + valid_action[-1]))
                cost_fx = heuristic_hx + cost_gx

                openSet.push(node + [newState], cost_fx)
                actions.push((node_action[0] + valid_action[2], node_action[1] + valid_action[-1]), cost_fx) 

        




    