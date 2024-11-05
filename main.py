import time
import psutil
import os
from algorithms import uniformCostSearch
from utils import GameObject

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
    start = time.time()

    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss / 1024
    
    args = readCommand()
    
    gameObject = GameObject(args.level)
    
    
    if args.method == 'dfs':
        # finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath = depthFirstSearch(gameState)
        print("dfs")
    elif args.method == 'bfs':
        # finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath = breadthFirstSearch(gameState)
        print("bfs")
    elif args.method == 'ucs':
        finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath = uniformCostSearch(gameObject)
    elif args.method == 'astar':
        # finalNumberOfSteps, finalWeight,  numberOfNodes, finalPath = aStarSearch(gameState)
        print("astar")
        
    end = time.time()
    memory_after = process.memory_info().rss / 1024
    current = memory_after - memory_before
    
    
    # print(method.upper())
    print(f"Steps: {finalNumberOfSteps}, Weight: {finalWeight}, Node: {numberOfNodes}, Time (ms): {(end-start)*1000:.2f}, Memory (MB): {current / 10**6:.2f}")