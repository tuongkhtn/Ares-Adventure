# import collections
# from utils import posOfAres, posAndWeightOfStones, posOfSwitches, posOfWalls
# from utils import isEndState
# from utils import validActionsInNextStep
# from utils import updateState
# from utils import CustomSet
# from utils import isFailed

# def depthFirstSearch(gameState):
#     """
#     Performs the Depth First Search algorithm to find the path for Ares to reach
#     the goal state.
    
#     Args:
#         gameState (Tuple[List[int], np.ndarray): A tuple containing:
#             - List[int]: The weights of the stones.
#             - np.ndarray: A 2D grid representing the maze.
    
#     Returns:
#         numberOfSteps (int): The number of steps in the solution path.
#         totalWeight (int): The total weight accumulated along the solution path.
#         numberOfNodes (int): The total number of nodes expanded during the search.
#         path (str): A string representing the sequence of actions taken in the solution path.
#     """
#     finalWeight = -1
#     finalPath = ""
#     finalNumberOfSteps = -1
#     finalStates = []
#     numberOfNodes = 1

#     startStones = posAndWeightOfStones(gameState)
#     startPosAres = posOfAres(gameState)
#     posSwitches = posOfSwitches(gameState)
#     posWalls = posOfWalls(gameState)

#     startState = (startPosAres, startStones)

#     frontier = collections.deque()
#     frontier.append([startState])

#     actions = collections.deque()
#     actions.append((0, ''))

#     exploredSet = CustomSet()
#     while frontier:
#         node = frontier.pop()
#         node_action = actions.pop()
#         posStonesLastState = [x[:2] for x in node[-1][1]]
#         if isEndState(posOfStones=posStonesLastState, posSwitches=posSwitches):
#             finalWeight = node_action[0]
#             finalPath = node_action[1]
#             finalNumberOfSteps = len(node_action[1])
#             finalStates = node
#             break
#         if node[-1] not in exploredSet:
#             exploredSet.add(node[-1])
#             for action in validActionsInNextStep(posAres=node[-1][0], posAndWeightStones=node[-1][1], posWalls=posWalls):
#                 newState = updateState(posAres=node[-1][0], posAndWeightStones=node[-1][1], action=action) 
#                 if isFailed(posAndWeightStones=newState[1], posWalls=posWalls, posSwitches=posSwitches):
#                     continue
#                 addWeightAndPath = (node_action[0] + action[2], node_action[1] + action[-1])
#                 frontier.append(node + [newState])
#                 actions.append(addWeightAndPath)

#                 numberOfNodes += 1
    
#     return finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath, finalStates