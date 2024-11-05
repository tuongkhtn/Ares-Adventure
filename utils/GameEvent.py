import pygame
from utils import Action
from utils import Utilities

class GameEvent:
    def __init__(self, gameObject):
        self.gameObject = gameObject
        
    def run(self, event):
        running = True
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            self.keyBoard(event)
            
        return running, self.gameObject
            
    def keyBoard(self, event):
        posOfAres = self.gameObject.ares.getCoordinate()
        posOfStones = [stone.getCoordinate() for stone in self.gameObject.stones]
        posOfWalls = [wall.getCoordinate() for wall in self.gameObject.walls]
        
        action = Action('n')
        if event.key == pygame.K_LEFT:
            action.setDirection('l')
        elif event.key == pygame.K_RIGHT:
            action.setDirection('r')
        elif event.key == pygame.K_UP:
            action.setDirection('u')
        elif event.key == pygame.K_DOWN:
            action.setDirection('d')
        
        if Utilities.isPushStone(posOfAres, posOfStones, action):
            action.setDirection(action.getDirection().upper())
            print(action.getDirection())
        
        if Utilities.isValidAction(posOfAres, posOfStones, posOfWalls, action):
            newPosOfAres, newPosOfStones = Utilities.updateState(posOfAres, posOfStones, action)
            self.gameObject.ares.setCoordinate(newPosOfAres[0], newPosOfAres[1])
            print(self.gameObject.ares.getCoordinate())
            for i in range(len(newPosOfStones)):
                self.gameObject.stones[i].setCoordinate(newPosOfStones[i][0], newPosOfStones[i][1])