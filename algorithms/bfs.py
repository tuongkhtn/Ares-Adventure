import collections
from utils import CustomSet
from utils import Utilities
from utils import GameObject

def breadthFirstSearch(gameObject: GameObject):
    """
    Performs the Breadth First Search algorithm to find the path for Ares to reach
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
            finalStates = node
            break
        
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            for action in Utilities.validActionsInNextStep(posOfAres=node[-1][0], posOfStones=node[-1][1], posOfWalls=posWalls, weightOfStones=weightStones):
                newState = Utilities.updateState(posOfAres=node[-1][0], posOfStones=node[-1][1], action=action)
                if Utilities.isFailed(posOfStones=newState[1], posOfSwitches=posSwitches, posOfWalls=posWalls):
                    continue
                addWeightAndPath = (node_action[0] + action.getWeight(), node_action[1] + action.getDirection())
                frontier.append(node + [newState])
                actions.append(addWeightAndPath)

                numberOfNodes += 1
    
    return finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates