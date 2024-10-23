import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import List, Tuple
import heapq
import numpy as np

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
    
    return tuple(np.argwhere(gameState[1] == 3)[0])

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
    
    listStones = [tuple(x) for x in np.argwhere((gameState[1] == 2) | (gameState[1] == 5))]
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
    
    return [tuple(x) for x in np.argwhere(gameState[1] == 1)]

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
    
    return [tuple(x) for x in np.argwhere((gameState[1] == 4) | (gameState[1] == 5) | (gameState[1] == 6))]

def isEndState(posStones: List[Tuple[int, int]], posSwitches: List[Tuple[int, int]]) -> bool:
    """
    Check if the positions of the stones match the positions of the switches.

    Args:
        posStones (List[Tuple[int, int]]): A list of tuples representing the coordinates of the stones.
        posSwitches (List[Tuple[int, int]]): A list of tuples representing the coordinates of the switches.

    Returns:
        bool: True if the stones are in the same positions as the switches, otherwise False.
    """
    
    return sorted(posStones) == sorted(posSwitches)

def costFunction(actions: Tuple[int, str]) -> int:
    """
    Caculates the total cost based on a list of actions.

    Args:
        actions (Tuple[int, str]): A tuple where the first element is an integer (weight of the action)
        and the second element is a string (the action itself).

    Returns:
        int: The total cost, which is the sum the weight and the number of moves. 
    """
    
    return sum([x[0] + len(x[1]) for x in actions])
    

def validActionsInNextStep(posAres: Tuple[int, int], posAndWeightStones: List[Tuple[int, int, int]]):
    """
    Determines valid actions for Ares in the next step based on the current position of Ares and the
    positions and weights of the stones.

    Args:
        posAres (Tuple[int, int]): A tuple representing the current position of Ares (x, y).
        posAndWeightStones (List[Tuple[int, int, int]]): A list of tuples where each tuple contains
        the coordinates (x, y) of a stone and its weight.

    Returns:
        List[Tuple[int, str]]: A list of valid actions.
    """
    
    actionsAll = [[0, -1, 0, 'l', 'L'], [0, 1, 0, 'r', 'R'], [-1, 0, 0, 'u', 'U'], [1, 0, 0, 'd', 'D']]
    validActions = []
    
    posStones = [x[:2] for x in posAndWeightStones]
    for action in actionsAll:
        xAresNextStep, yAresNextStep = posAres[0] + action[0], posAres[1] + action[1]
        if (xAresNextStep, yAresNextStep) in posStones: # push stone
            action.pop(3) # pop lowercase
            
            index = posStones.index((xAresNextStep, yAresNextStep))
            action[3] = posAndWeightStones[index][-1]  # update weight
        else:
            action.pop(4) # pop uppercase
    
        validActions.append((action[2], action[-1]))
    
    return validActions

def updateState(posAres, posAndWeightStones, action):
    return 0
    