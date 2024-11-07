import time
import psutil
import os
from utils.GameObject import GameObject
from utils.GameGraphic import GameGraphic

def readCommand():
    """
    Processes the command used to run Ares Adventure from the command line.
    
    Args:
        
    Returns:
        weights (List[int]): The weight of the stones.
        maze (List[str]): The structure of the maze represented as a list of strings.
        method (str): The method used to solve the maze.
        level (str): The level of the maze.
    """
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--level', type=str,
                        help='level of game to play', default='input-01.txt')
    parser.add_argument('-m', '--method', type=str,
                        help='algorithm method', default='dfs')
    args = parser.parse_args()
        
    return args

if __name__ == '__main__':
    args = readCommand()
    
    gameObject = GameObject(args.level)
    
    gameGraphic = GameGraphic(gameObject)
    gameGraphic.run()