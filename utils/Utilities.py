import copy
import heapq
from typing import Tuple
from .Action import Action

class Utilities:
    def isEndState(posOfStones, posOfSwitches):
        return sorted(posOfStones) == sorted(posOfSwitches)
    
    def isFailed(posOfStones, posOfSwitches, posOfWalls):
        rotatePattern = [[0,1,2,3,4,5,6,7,8],
                        [2,5,8,1,4,7,0,3,6],
                        [0,1,2,3,4,5,6,7,8][::-1],
                        [2,5,8,1,4,7,0,3,6][::-1]]
        flipPattern = [[2,1,0,5,4,3,8,7,6],
                        [0,3,6,1,4,7,2,5,8],
                        [2,1,0,5,4,3,8,7,6][::-1],
                        [0,3,6,1,4,7,2,5,8][::-1]]
        allPattern = rotatePattern + flipPattern
        
        posOfStones = posOfStones
        
        for posOfStone in posOfStones:
            if posOfStone not in posOfSwitches:
                x, y = posOfStone
                board = [(x-1, y-1), (x-1, y), (x-1, y+1),
                        (x, y-1), (x, x), (x, y+1),
                        (x+1, y-1), (x+1, y), (x+1, y+1)] # get 3x3 matrix, it is the cells adjacent to the stone under consideration.

                for pattern in allPattern:
                    newBoard = [board[i] for i in pattern]
                    
                    if newBoard[1] in posOfWalls and newBoard[5] in posOfWalls: return True
                    elif newBoard[5] in posOfStones and newBoard[1] in posOfWalls and newBoard[2] in posOfWalls: return True
                    elif newBoard[1] in posOfStones and newBoard[2] in posOfWalls and newBoard[5] in posOfWalls: return True
                    elif newBoard[1] in posOfStones and newBoard[5] in posOfStones and newBoard[2] in posOfWalls: return True
                    elif newBoard[1] in posOfStones and newBoard[2] in posOfStones and newBoard[5] in posOfStones: return True
                    elif newBoard[1] in posOfStones and newBoard[6] in posOfStones and newBoard[2] in posOfWalls and newBoard[3] in posOfWalls and newBoard[8] in posOfWalls: return True

        return False
            
    def isValidAction(posOfAres, posOfStones, posOfWalls, action: Action):
        if action.getDirection().isupper():
            x, y = posOfAres[0] + 2 * action.getCoordinate()[0], posOfAres[1] + 2 * action.getCoordinate()[1] # get stone's next position
        else:
            x, y = posOfAres[0] + action.getCoordinate()[0], posOfAres[1] + action.getCoordinate()[1] # get Ares's next position
        
        return (x, y) not in posOfStones + posOfWalls
    
    def validActionsInNextStep(posOfAres, posOfStones, posOfWalls, weightOfStones):
        actionsAll = [[0, -1, 0, 'l', 'L'], [0, 1, 0, 'r', 'R'], [-1, 0, 0, 'u', 'U'], [1, 0, 0, 'd', 'D']]
        validActions = []
        
        for action in actionsAll:
            xAresNextStep, yAresNextStep = posOfAres[0] + action[0], posOfAres[1] + action[1]
            if (xAresNextStep, yAresNextStep) in posOfStones: # push stone
                action.pop(3) # pop lowercase
                
                index = posOfStones.index((xAresNextStep, yAresNextStep))
                action[2] = weightOfStones[index]
            else:
                action.pop(4) # pop uppercase
            
            actionObject = Action(action[-1])
            actionObject.setWeight(action[2])
                
            if Utilities.isValidAction(posOfAres, posOfStones, posOfWalls, actionObject):
                validActions.append(actionObject)
        
        return validActions
    
    def updateState(posOfAres, posOfStones, action: Action):
        newPosOfAres = posOfAres[0] + action.getCoordinate()[0], posOfAres[1] + action.getCoordinate()[1]
        
        posOfStonesCopy = copy.deepcopy(posOfStones)
        if action.getDirection().isupper():
            index = posOfStonesCopy.index(newPosOfAres)
            newPosOfStone = posOfAres[0] + 2 * action.getCoordinate()[0], posOfAres[1] + 2 * action.getCoordinate()[1]
            posOfStonesCopy[index] = newPosOfStone
        
        return newPosOfAres, posOfStonesCopy
    
    def costFunction(action: Tuple[int, str]) -> int:
        """
        Caculates the total cost based on a list of actions.

        Args:
            action (Tuple[int, str]): A tuple where the first element is an integer (total weight of the action)
            and the second element is a path (the action itself).

        Returns:
            int: The total cost, which is the sum the weight and the number of moves. 
        """
        
        discount = 0.9
        sum = 0.0
        for i in range(len(action[1])):
            sum += ord(action[1][i]) * (discount**i)
            
        return (action[0] + len(action[1])) + sum * 0.00001
    
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