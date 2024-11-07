import collections
from utils.Utilities import CustomSet
from utils.Utilities import Utilities
from utils.GameObject import GameObject

def breadthFirstSearch(gameObject: GameObject):
    """
    Performs the Breadth First Search algorithm to find the path for Ares to reach
    the goal state.
    
    Args:
        gameObject (GameObject)
    
    Returns:
        numberOfSteps (int): The number of steps in the solution path.
        totalWeight (int): The total weight accumulated along the solution path.
        numberOfNodes (int): The total number of nodes expanded during the search.
        path (str): A string representing the sequence of actions taken in the solution path.
    """
    print("breadthFirstSearch")
    finalWeight = -1
    finalPath = ""
    finalNumberOfSteps = -1
    numberOfNodes = 1

    startPosStones = gameObject.positionOfStones()
    weightStones = gameObject.weightOfStones()
    startPosAres = gameObject.positionOfAres()
    posSwitches = gameObject.positionOfSwitches()
    posWalls = gameObject.positionOfWalls()

    startState = (startPosAres, startPosStones)

    frontier = collections.deque()
    frontier.append([startState])

    actions = collections.deque()
    actions.append((0, ''))

    exploredSet = CustomSet()
    while frontier:
        node = frontier.popleft()
        node_action = actions.popleft()
        posStonesLastState = node[-1][1]

        if Utilities.isEndState(posOfStones=posStonesLastState, posOfSwitches=posSwitches):
            finalWeight = node_action[0]
            finalPath = node_action[1]
            finalNumberOfSteps = len(node_action[1])
            break
        
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            for action in Utilities.validActionsInNextStep(posOfAres=node[-1][0], posOfStones=node[-1][1], posOfWalls=posWalls, weightOfStones=weightStones):
                newPosOfAres, posOfStonesCopy, _ = Utilities.updateState(node[-1][0], node[-1][1], action)  # newState Tuple[PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]]]
                newState = (newPosOfAres, posOfStonesCopy)                
                if Utilities.isFailed(posOfStones=newState[1], posOfSwitches=posSwitches, posOfWalls=posWalls):
                    continue
                addWeightAndPath = (node_action[0] + action.getWeight(), node_action[1] + action.getDirection())
                frontier.append(node + [newState])
                actions.append(addWeightAndPath)

                numberOfNodes += 1
    
    return finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath
