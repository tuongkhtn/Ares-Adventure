

class Action:
    def __init__(self):
        self.__direction = "n"
        self.__weight = 0
    
    def __init__(self, direction):
        self.__direction = direction
        self.__weight = 0
    
    def getDirection(self):
        return self.__direction
    
    def getWeight(self):
        return self.__weight
    
    def setDirection(self, direction):
        self.__direction = direction
        
    def setWeight(self, weight):
        self.__weight = weight
        
    def getCoordinate(self):
        direction = self.__direction.lower()
        
        if direction == 'l':
            return (0, -1)
        elif direction == 'r':
            return (0, 1)
        elif direction == 'u':
            return (-1, 0)
        elif direction == 'd':
            return (1, 0)
        elif direction == 'n':
            return (0, 0)
            