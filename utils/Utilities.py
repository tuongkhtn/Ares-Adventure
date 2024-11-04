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
                action[2] = weightOfStones[index].getWeight()
            else:
                action.pop(4) # pop uppercase
            
            actionObject = Action(action[-1])
            actionObject.setWeight(action[2])
                
            if Utilities.isValidAction(posOfAres, posOfStones, posOfWalls, actionObject):
                validActions.append(actionObject)
        
        return validActions