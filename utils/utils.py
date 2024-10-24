import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import List, Tuple
import heapq
import numpy as np
import copy

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0
        
    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
    
    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0
    def peek_all(self):
        heap_copy = self.heap[:]
        result = []
        while heap_copy:
            (priority, _, item) = heapq.heappop(heap_copy)
            result.append((item, priority))
        return result
    
class CustomSet(set):
    def add(self, item):
        item_hashable = (item[0], frozenset(item[1]))
        super().add(item_hashable)
        
    def __contains__(self, item):
        item_hashable = (item[0], frozenset(item[1]))
        return super().__contains__(item_hashable)

def readCommand():
    """
    Processes the command used to run Ares Adventure from the command line.
    
    Args:
        
    Returns:
        weights (List[int]): The weight of the stones.
        maze (List[str]): The structure of the maze represented as a list of strings.
    """
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--level', type=str,
                        help='level of game to play', default='input-01.txt')
    # parser.add_argument('-m', '--method', )
    args = parser.parse_args()
    
    with open(args.level, 'r') as f:
        lines = f.readlines()
        
    weights = [int(x) for x in lines[0].strip().split()]
    maze = lines[1:]
    
    return weights, maze

def transferToGameState(weights: List[int], maze: List[str]):
    """
    Converts the input maze into a 2D grid where each character is replaced by a corresponding integer 
    representing different game elements.

    Args:
        weights (List[int]): The weight of the stones.
        maze (List[str]): The structure of the maze, where each string represents a row.
        
    Returns:
        weights (List[int]): The weight of the stones.
        maze (np.ndarray): A 2D list representation of the maze, where each element is an integer.
    """
    
    maze = [x.replace('\n', '') for x in maze]
    maze = [','.join(x) for x in maze]
    maze = [x.split(',') for x in maze]
    maxLenCol = max([len(x) for x in maze])
    
    for x in maze:
        for i in range(len(x)):
            if x[i] == ' ':   # free spaces
                x[i] = 0
            elif x[i] == '#': # walls
                x[i] = 1
            elif x[i] == '$': # stones
                x[i] = 2
            elif x[i] == '@': # Ares
                x[i] = 3
            elif x[i] == '.': # switches
                x[i] = 4
            elif x[i] == '*': # stone on a switch
                x[i] = 5
            elif x[i] == '+': # Ares on a switch
                x[i] = 6
                
        lenCol = len(x)
        if lenCol < maxLenCol:
            x.extend([1 for _ in range(maxLenCol - lenCol)]) # add walls if lenCol is smaller than maxLenCol

    return weights, np.array(maze)

def posOfAres(gameState):
    """
    Find the position of Ares in the game state represented by a maze.
    
    Args:
        gameState (Tuple[List[int], np.ndarray): A tuple containing:
            - List[int]: The weights of the stones.
            - np.ndarray: A 2D grid representing the maze.
            
    Returns:
        Tuple[int, int]: The position of Ares in the maze as (row, column).
    """
    
    return tuple(np.argwhere(gameState[1] == 3)[0].tolist())

def posAndWeightOfStones(gameState):
    """
    Find the positions and weights of all stones in the game state represented by a maze.

    Args:
        gameState (Tuple[List[int], np.ndarray): A tuple containing:
            - List[int]: The weights of the stones.
            - np.ndarray: A 2D grid representing the maze.
    
    Returns:
        listStones (List[Tuple[int, int, int]]): A list of tuples, where each tuple (x, y, weight) represents the
        coordinates (row, column) of a stone and its corresponding weight.
    """
    
    listStones = [tuple(x.tolist()) for x in np.argwhere((gameState[1] == 2) | (gameState[1] == 5))]
    for i in range(len(listStones)):
        listStones[i] += (gameState[0][i],)
    return listStones

def posOfWalls(gameState):
    """
    Find the positions of walls in the game state represented by a maze.
    
    Args:
        gameState (Tuple[List[int], np.ndarray): A tuple containing:
            - List[int]: The weights of the stones.
            - np.ndarray: A 2D grid representing the maze.
            
    Returns:
        List[Tuple[int, int]]: A list of tuples, where each tuple (row, column) represents the 
        coordinates of a wall in the maze.
    """
    
    return [tuple(x.tolist()) for x in np.argwhere(gameState[1] == 1)]

def posOfSwitches(gameState):
    """
    Find the positions of switches in the game state represented by a maze.
    
    Args:
        gameState (Tuple[List[int], np.ndarray): A tuple containing:
            - List[int]: The weights of the stones.
            - np.ndarray: A 2D grid representing the maze.
            
    Returns:
        List[Tuple[int, int]]: A list of tuples, where each tuple (row, column) represents the 
        coordinates of a switch, stone on a switch and Ares on a switch in the maze.
    """
    
    return [tuple(x.tolist()) for x in np.argwhere((gameState[1] == 4) | (gameState[1] == 5) | (gameState[1] == 6))]

def isEndState(posOfStones: List[Tuple[int, int]], posSwitches: List[Tuple[int, int]]) -> bool:
    """
    Check if the positions of the stones match the positions of the switches.

    Args:
        posOfStones (List[Tuple[int, int]]): A list of tuples representing the coordinates of the stones.
        posSwitches (List[Tuple[int, int]]): A list of tuples representing the coordinates of the switches.

    Returns:
        bool: True if the stones are in the same positions as the switches, otherwise False.
    """
    
    return sorted(posOfStones) == sorted(posSwitches)

def isValidAction(
    action: List[int], 
    posAres: Tuple[int, int], 
    posOfStones: List[Tuple[int, int]], 
    posWalls: List[Tuple[int, int]]
) -> bool:
    """
    Check if the given action is valid based on the current position of Ares, the stones, and the walls.

    Args:
        action (List[int]): The action Ares is attempting to take.
        posAres (Tuple[int, int]): A tuple representing the current position of Ares (x, y).
        posOfStones (List[Tuple[int, int]]): A list of tuples where each tuple contains
                                           the coordinates (x, y) of a stone.
        posWalls (List[Tuple[int, int]]): A list of tuples representing the coordinates of the walls.

    Returns:
        bool: True if the action is valid, False otherwise.
        
    The function handles two cases:
    1. If Ares is pushing a stone (uppercase action), it checks if the stone's next position after being 
    pushed is either another stone's position or a wall's position.
    2. If it's a normal move (lowercase action), check if Ares's next position is wall.
    """
    
    if action[-1].isupper():
        x1, y1 = posAres[0] + 2 * action[0], posAres[1] + 2 * action[1] # get stone's next position
    else:
        x1, y1 = posAres[0] + action[0], posAres[1] + action[1] # get Ares's next position
    
    return (x1, y1) not in posOfStones + posWalls
    

def validActionsInNextStep(
    posAres: Tuple[int, int], 
    posAndWeightStones: List[Tuple[int, int, int]], 
    posWalls: List[Tuple[int, int]]
):
    """
    Determines valid actions for Ares in the next step based on the current position of Ares and the
    positions and weights of the stones.

    Args:
        posAres (Tuple[int, int]): A tuple representing the current position of Ares (x, y).
        posAndWeightStones (List[Tuple[int, int, int]]): A list of tuples where each tuple contains
                                                         the coordinates (x, y) of a stone and its weight.
        posWalls (List[Tuple[int, int]]): A list of tuples representing the coordinates of the walls.

    Returns:
        List[Tuple[int, int, int, str]]: A list of valid actions.
    """
    
    actionsAll = [[0, -1, 0, 'l', 'L'], [0, 1, 0, 'r', 'R'], [-1, 0, 0, 'u', 'U'], [1, 0, 0, 'd', 'D']]
    validActions = []
    
    posOfStones = [x[:2] for x in posAndWeightStones]
    for action in actionsAll:
        xAresNextStep, yAresNextStep = posAres[0] + action[0], posAres[1] + action[1]
        if (xAresNextStep, yAresNextStep) in posOfStones: # push stone
            action.pop(3) # pop lowercase
            
            index = posOfStones.index((xAresNextStep, yAresNextStep))
            action[2] = posAndWeightStones[index][-1]  # update weight
        else:
            action.pop(4) # pop uppercase
            
        if isValidAction(action, posAres, posOfStones, posWalls):
            validActions.append(tuple(action))
    
    return validActions

def updateState(
    posAres: Tuple[int, int], 
    posAndWeightStones: List[Tuple[int, int, int]], 
    action: Tuple[int, int, int, int]
):
    """
    Update the state of the game by calculating the next position of Ares and adjusting the positions of the 
    stones based on the action taken.

    Args:
        posAres (Tuple[int, int]): A tuple representing the current position of Ares (x, y).
        posAndWeightStones (List[Tuple[int, int, int]]): A list of tuples where each tuple contains
                                                         the coordinates (x, y) of a stone and its weight.
        action (Tuple[int, int, int, int]): The action Ares is attempting to take.

    Returns:
        nextPosOfAres (Tuple[int, int]): The updated position of Ares.
        posAndWeightOfStones (List[Tuple[int, int, int]]): The updated list of stone positions and weights.
    """
    
    nextPosOfAres = (posAres[0] + action[0], posAres[1] + action[1])
    posAndWeightStones_copy = copy.deepcopy(posAndWeightStones)
    posOfStones = [x[:2] for x in posAndWeightStones_copy]
    if action[-1].isupper(): # push stone
        index = posOfStones.index(nextPosOfAres)
        nextPosAndWeightOfStone = (posAres[0] + 2 * action[0], posAres[1] + 2 * action[1], posAndWeightStones_copy[index][-1])
        posAndWeightStones_copy.pop(index)
        posAndWeightStones_copy.append(nextPosAndWeightOfStone)
        
        
    return nextPosOfAres, sorted(posAndWeightStones_copy)
    
def costFunction(action: Tuple[int, str]) -> int:
    """
    Caculates the total cost based on a list of actions.

    Args:
        action (Tuple[int, str]): A tuple where the first element is an integer (weight of the action)
        and the second element is a string (the action itself).

    Returns:
        int: The total cost, which is the sum the weight and the number of moves. 
    """
    
    discount = 0.9
    sum = 0.0
    for i in range(len(action[1])):
        sum += ord(action[1][i]) * 10 * (discount**i)
        
    return (action[0] + len(action[1])) + sum*0.00001


def isFailed(stones, posWalls, posSwitches):
    """This function used to observe if the state is potentially failed, then prune the search.
    
    It checks if any of the stones is blocked by walls and other stones. The check is done by
    rotating and flipping the board and checking if the stone is blocked in any of the 8 
    possible orientations.
    
    Args:
        stones (List[Tuple[int, int, int]]): A list of tuples where each tuple contains the 
                                            coordinates (x, y) of a stone and its weight.
        posWalls (List[Tuple[int, int]]): A list of tuples representing the coordinates of the walls.
        posSwitches (List[Tuple[int, int]]): A list of tuples representing the coordinates of the switches.
    
    Returns:
        bool: True if the state is potentially failed, False otherwise.
    """
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


def manhattanDistance (pos1, pos2):
    """
    Calculate the Manhattan distance between two positions.

    Args:
        pos1 (Tuple[int, int]): The first position as a tuple of (x, y) coordinates.
        pos2 (Tuple[int, int]): The second position as a tuple of (x, y) coordinates.

    Returns:
        int: The Manhattan distance between the two positions.
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
