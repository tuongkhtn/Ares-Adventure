from utils import PriorityQueue
from utils import posOfAres, posAndWeightOfStones, posOfSwitches, posOfWalls
from utils import isEndState
from utils import costFunction
from utils import validActionsInNextStep
from utils import updateState
from utils import CustomSet

def manhattanDistance (pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def heuristic(switches, stones):
    """A heuristic function to calculate the overall distance between the else boxes and the else goals"""
    distance = 0
    posStones = [x[:2] for x in stones]
    completes = set(switches) & set(posStones)
    sortedStones = list(set(posStones).difference(completes))
    sortedSwitches = list(set(switches).difference(completes))
    for i in range(len(sortedStones)):
        distance += (manhattanDistance(sortedStones[i][:2], sortedSwitches[i]))
    return distance

def printActions(actions):
    while not actions.isEmpty():
        print(actions.pop())


def isFailed(stones, posWalls, posSwitches):
    """This function used to observe if the state is potentially failed, then prune the search"""
    rotatePattern = [[0,1,2,3,4,5,6,7,8],
                    [2,5,8,1,4,7,0,3,6],
                    [0,1,2,3,4,5,6,7,8][::-1],
                    [2,5,8,1,4,7,0,3,6][::-1]]
    flipPattern = [[2,1,0,5,4,3,8,7,6],
                    [0,3,6,1,4,7,2,5,8],
                    [2,1,0,5,4,3,8,7,6][::-1],
                    [0,3,6,1,4,7,2,5,8][::-1]]
    allPattern = rotatePattern + flipPattern

    posStones = [stone[:2] for stone in stones]  
    for box in posStones:
        if  box not in posSwitches:
            board = [(box[0] - 1, box[1] - 1), (box[0] - 1, box[1]), (box[0] - 1, box[1] + 1), 
                    (box[0], box[1] - 1), (box[0], box[1]), (box[0], box[1] + 1), 
                    (box[0] + 1, box[1] - 1), (box[0] + 1, box[1]), (box[0] + 1, box[1] + 1)]
            for pattern in allPattern:
                newBoard = [board[i] for i in pattern]
                if newBoard[1] in posWalls and newBoard[5] in posWalls: return True
                elif newBoard[1] in posStones and newBoard[2] in posWalls and newBoard[5] in posWalls: return True
                elif newBoard[1] in posStones and newBoard[2] in posWalls and newBoard[5] in posStones: return True
                elif newBoard[1] in posStones and newBoard[2] in posStones and newBoard[5] in posStones: return True
                elif newBoard[1] in posStones and newBoard[6] in posStones and newBoard[2] in posWalls and newBoard[3] in posWalls and newBoard[8] in posWalls: return True
    return False

def aStarSearch(gameState):
    startPosAres = posOfAres(gameState)
    startStones = posAndWeightOfStones(gameState)
    startState = (startPosAres, startStones)
    posSwitches = posOfSwitches(gameState)
    posWalls = posOfWalls(gameState)

    
    print("startPosAres: ", startPosAres)
    print("startPosAndWeightStones: ", startStones)
    print("startState: ", startState)
    print("posSwitches: ", posSwitches)

    startState = (startPosAres, startStones) # Tuple(PosAres: Tuple(int, int), Stones: List[Stone: Tuple(X: int, Y: int, Weight: int)]))

    openSet = PriorityQueue() # PriorityQueue(State: Tuple(PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]]), Cost f(x): int)
    openSet.push([startState], 0 + heuristic(posSwitches, startStones))

    exploredSet = CustomSet()

    actions = PriorityQueue() # PriorityQueue(Tuple(total weight: int, path: str), value: int)

    actions.push((0, ''), heuristic(posSwitches, startStones)) 

    while not openSet.isEmpty():
        print("-"*100)
        node = openSet.pop() # Tuple(PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]])
        

        print("actions: ", actions.peek_all())
        node_action = actions.pop() # Tuple(total weight: int, path: str)
        print('node_action', node_action)

        if isEndState(node[0][0], posSwitches):
            print("End: ", node_action)
            break
        print("node", node)
        print("node[-1]", node[-1])
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            cost_gx = len([x for x in node_action[1] if x.islower()])
            for valid_action in validActionsInNextStep(node[-1][0], node[-1][1], posWalls):  # action Tuple[X: int, Y: int,  stoneWeight: int, command: str]
                print("valid_action", valid_action)
                newState = updateState(node[-1][0], list(node[-1][1]), valid_action)  # newState Tuple[PosAres: Tuple(int, int), Stones: List[Stone: Tuple[X: int, Y: int, Weight: int]]]
                print('newState', newState)
                if isFailed(stones=newState[1], posWalls=posWalls, posSwitches=posSwitches):
                    continue
                heuristic_hx = heuristic(posSwitches, newState[1])
                print("heuristic_hx", heuristic_hx)
                cost_fx = heuristic_hx + cost_gx
                print("cost_fx", cost_fx)
                openSet.push(node + [newState], cost_fx)
                actions.push((node_action[0] + valid_action[2], node_action[1] + valid_action[-1]), cost_fx) 
                # print('(node_action[0] + action[2], node_action[1] + action[-1])', (node_action[0] + action[2], node_action[1] + action[-1]))


        print("valid_action", valid_action)
        




    