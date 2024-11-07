import numpy as np
from .Ares import Ares
from .Wall import Wall
from .Stone import Stone
from .Switch import Switch
from .FreeSpace import FreeSpace
from config import UIConfig

class GameObject:
    def __init__(self, filename):
        weights, maze = self.readFile(filename)   
        self.weights = weights
        self.maze = maze
        self.filename = filename
        
        self.totalWeight = 0
        self.stepCount = 0
        
        self.ares = [Ares(x.tolist()[0], x.tolist()[1]) for x in np.argwhere((maze == 3) | (maze == 6))][0]
        self.walls = [Wall(x.tolist()[0], x.tolist()[1]) for x in np.argwhere(maze == 1)]
        self.switches = [Switch(x.tolist()[0], x.tolist()[1]) for x in np.argwhere((maze == 4) | (maze == 5) | (maze == 6))]
        self.freeSpaces = [FreeSpace(x.tolist()[0], x.tolist()[1]) for x in np.argwhere((maze != 1) & (maze != -1))]
        
        stones = [Stone(x.tolist()[0], x.tolist()[1], 0) for x in np.argwhere((maze == 2) | (maze == 5))]
        for i in range(len(stones)):
            stones[i].setWeight(weights[i])
        
        self.stones = stones   

        # Offset
        self.offsetX = (UIConfig.WINDOW_WIDTH -max([len(x) for x in self.maze])*UIConfig.TILE_SIZE)//2 - 40
        self.offsetY = (UIConfig.WINDOW_HEIGHT -len(self.maze)*UIConfig.TILE_SIZE)//2 - 100
        
    def readFile(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        weights = [int(x) for x in lines[0].strip().split()]
        maze = [x.replace('\n', '') for x in lines[1:]]
        maze = [x.lstrip().rjust(len(x), 'E') for x in maze]
        maze = [x.rstrip().ljust(len(x), "E") for x in maze]
    
        maze = [','.join(x) for x in maze]
        maze = [x.split(',') for x in maze]
        maxLenCol = max([len(x) for x in maze])
        
        
        for x in maze:
            for i in range(len(x)):
                if x[i] == 'E': # no object
                    x[i] = -1
                elif x[i] == ' ':   # free spaces
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
                x.extend([-1 for _ in range(maxLenCol - lenCol)]) # add walls if lenCol is smaller than maxLenCol

        return weights, np.array(maze)

    def reset(self):
        return GameObject(self.filename)
        
    def positionOfAres(self):
        return self.ares.getCoordinate()
    
    def positionOfStones(self):
        return [stone.getCoordinate() for stone in self.stones]
    
    def weightOfStones(self):
        return [stone.getWeight() for stone in self.stones]
    
    def positionOfSwitches(self):
        return [swich.getCoordinate() for swich in self.switches]
    
    def positionOfWalls(self):
        return [wall.getCoordinate() for wall in self.walls]
    
    def positionOfFreeSpaces(self):
        return [freeSpace.getCoordinate() for freeSpace in self.freeSpaces]
    
    def addUI(self):
        self.ares = self.ares.addUI()
        self.stones = [stone.addUI() for stone in self.stones]
        self.walls = [wall.addUI() for wall in self.walls]
        self.switches = [switch.addUI() for switch in self.switches]
        self.freeSpaces = [freeSpace.addUI() for freeSpace in self.freeSpaces]
        return self
    
    def draw(self, screen):
        for freeSpace in self.freeSpaces:
            freeSpace.draw(screen, self.offsetX, self.offsetY)
        
        for switch in self.switches:
            switch.draw(screen, self.offsetX, self.offsetY)
        
        self.ares.draw(screen, self.offsetX, self.offsetY)

        for stone in self.stones:
            stone.draw(screen, self.offsetX, self.offsetY)
            
        for wall in self.walls:
            wall.draw(screen, self.offsetX, self.offsetY)
        