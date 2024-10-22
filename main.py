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

def isEndState(posStones, posSwitches):
    return sorted(posStones) == sorted(posSwitches)
    

if __name__ == '__main__':
    weights, maze = readCommand()
    gameState = transferToGameState(weights, maze)
    
    print(posOfSwitchs(gameState))
    