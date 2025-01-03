from utils.Utilities import CustomSet
from utils.Utilities import Utilities
from utils.GameObject import GameObject
from utils.Utilities import PriorityQueue

def uniformCostSearch(gameObject: GameObject):
    """
    Performs the Uniform Cost Search algorithm to find the optimal path for Ares to reach
    the goal state.
    """
    print("uniformCostSearch")
    finalWeight = -1
    finalPath = ""
    finalNumberOfSteps = -1
    numberOfNodes = 1
    
    posOfAres = gameObject.positionOfAres()
    posOfStones = gameObject.positionOfStones()
    posOfWalls = gameObject.positionOfWalls()
    posOfSwitches = gameObject.positionOfSwitches()
    weightOfStones = gameObject.weightOfStones()
    
    openSet = PriorityQueue() # openSet save states
    openSet.push([(posOfAres, posOfStones)], 0)
    
    actions = PriorityQueue() # actions store (totalWeight, path), cost
    actions.push((0, ''), float('inf'))
    
    exploredSet = CustomSet() # save state appeared
    
    
    while not openSet.isEmpty():
        
        node = openSet.pop() # List[Tuple(PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]])]
        node_action = actions.pop() # Tuple(total weight: int, path: str)        

        if Utilities.isEndState(node[-1][-1], posOfSwitches):
            finalWeight = node_action[0]
            finalPath = node_action[1]
            finalNumberOfSteps = len(node_action[1])
            break
        
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])

            for valid_action in Utilities.validActionsInNextStep(posOfAres=node[-1][0], posOfStones=node[-1][1], posOfWalls=posOfWalls, weightOfStones=weightOfStones):  # action Tuple[X: int, Y: int,  stoneWeight: int, command: str]
                newPosOfAres, posOfStonesCopy, _ = Utilities.updateState(node[-1][0], node[-1][1], valid_action)  # newState Tuple[PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]]]
                newState = (newPosOfAres, posOfStonesCopy)
                
                if Utilities.isFailed(posOfStones=node[-1][-1], posOfWalls=posOfWalls, posOfSwitches=posOfSwitches):
                    continue
                
                addWeightAndPath = (node_action[0] + valid_action.getWeight(), node_action[1] + valid_action.getDirection())
                cost = Utilities.costFunction(addWeightAndPath)  
                openSet.push(node + [newState], cost)
                actions.push(addWeightAndPath, cost)   
                numberOfNodes += 1                  
        
    return finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath
