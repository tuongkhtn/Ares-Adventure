import sys
from typing import List

def readCommand():
    """
    Processes the command used to run Ares Adventure from the command line.
    
    Args:
        argv (List[str]): The list of command-line arguments passed to the program.
        
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
        maze (List[List[int]]): A 2D list representation of the maze, where each element is an integer.
    """
    
    maze = [x.replace('\n', '') for x in maze]
    maze = [','.join(x) for x in maze]
    maze = [x.split(',') for x in maze]
    maxLenCol = max([len(x) for x in maze])
    
    for x in maze:
        for i in range(len(x)):
            if x[i] == ' ':   # walls
                x[i] = 0
            elif x[i] == '#': # free spaces
                x[i] = 1
            elif x[i] == '$': # stones
                x[i] = 2
            elif x[i] == '@': # Ares
                x[i] = 3
            elif x[i] == '.': # switch
                x[i] = 4
            elif x[i] == '*': # stone in switch
                x[i] = 5
            elif x[i] == '+': # Ares in switch
                x[i] = 6
                
        lenCol = len(x)
        if lenCol < maxLenCol:
            x.extend([1 for _ in range(maxLenCol - lenCol)]) # add walls if lenCol is smaller than maxLenCol

    return weights, maze
    
    

if __name__ == '__main__':
    weights, maze = readCommand()
    gameState = transferToGameState(maze)
    
    print(gameState)
    