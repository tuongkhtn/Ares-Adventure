import copy

from utils import PriorityQueue
from utils import CustomSet
from utils import GameObject
from utils import Utilities
from scipy.optimize import linear_sum_assignment
import numpy as np


def manhattanDistance(pos1, pos2):
    """
    Calculate the Manhattan distance between two points.

    Parameters
    ----------
    pos1 : Tuple[int, int]
        The coordinates of the first point.
    pos2 : Tuple[int, int]
        The coordinates of the second point.

    Returns
    -------
    int
        The Manhattan distance between the two points.
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

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

    posStones, weightsOfStones = stones
    completes = set(switches) & set(posStones)
    sortedStones = list(set(posStones).difference(completes))
    sortedSwitches = list(set(switches).difference(completes))
    if not sortedStones or not sortedSwitches:
        return 0
    

    cost_matrix = np.zeros((len(posStones), len(switches)))
    
    # Calculate the cost matrix
    for i in range(len(posStones)):
        for j in range(len(switches)):
            cost_matrix[i][j] = manhattanDistance(posStones[i], switches[j])*weightsOfStones[i]
    
    # Use linear_sum_assignment to find the optimal assignment
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    # Calculate the total distance
    total_distance = cost_matrix[row_ind, col_ind].sum()
    
    return total_distance


def aStarSearch(gameObject: GameObject):

    finalWeight = -1
    finalPath = ""
    finalNumberOfSteps = -1
    numberOfNodes = 1


    posOfAres = gameObject.positionOfAres()
    posOfStones = gameObject.positionOfStones()
    posOfWalls = gameObject.positionOfWalls()
    posOfSwitches = gameObject.positionOfSwitches()
    weightOfStones = gameObject.weightOfStones()

    startState = (posOfAres, posOfStones) # Tuple(PosAres: Tuple(int, int), Stones: List[Stone: Tuple(X: int, Y: int, Weight: int)]))

    openSet = PriorityQueue() # PriorityQueue(State: Tuple(PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]]), Cost f(x): int)
    openSet.push([startState], 0)

    exploredSet = CustomSet()

    actions = PriorityQueue() # PriorityQueue(Tuple(total weight: int, path: str), value: int)
    actions.push((0, ''), float('inf')) 

    numberOfNodes = 1
    while not openSet.isEmpty():
        
        node = openSet.pop() # List[Tuple(PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]])]
        node_action = actions.pop() # Tuple(total weight: int, path: str)

        posOfStonesLastState = node[-1][-1]


        if Utilities.isEndState(posOfStonesLastState, posOfSwitches):
            finalWeight = node_action[0]
            finalPath = node_action[1]
            finalNumberOfSteps = len(node_action[1])
            break
        
        
        if node[-1] not in exploredSet:
            # print("node[-1]: ", node[-1])
            exploredSet.add(node[-1])

            for valid_action in Utilities.validActionsInNextStep(posOfAres=node[-1][0], posOfStones=node[-1][1], posOfWalls=posOfWalls, weightOfStones=weightOfStones):  # action Tuple[X: int, Y: int,  stoneWeight: int, command: str]
                # print("valid_action: ", valid_action)
                newPosOfAres, posOfStonesCopy, _ = Utilities.updateState(node[-1][0], node[-1][1], valid_action)  # newState Tuple[PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]]]
                newState = (newPosOfAres, posOfStonesCopy)
                if Utilities.isFailed(posOfStones=node[-1][-1], posOfWalls=posOfWalls, posOfSwitches=posOfSwitches):
                    continue
                
                
                heuristic_hx = heuristic(switches=posOfSwitches, stones=(newState[1], weightOfStones))
                
                cost_gx = Utilities.costFunction((node_action[0] + valid_action.getWeight(), node_action[1] +  valid_action.getDirection()))
                cost_fx = heuristic_hx + cost_gx

                openSet.push(node + [newState], cost_fx)
                actions.push((node_action[0] + valid_action.getWeight(), node_action[1] +  valid_action.getDirection()), cost_fx)   
                numberOfNodes+=1
        
    return finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath