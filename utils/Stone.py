from .Object import Object
from config import ImageConfig

class Stone(Object):
    def __init__(self, x, y, weight):
        super().__init__(x, y)
        self.__weight = weight
        
    def getWeight(self):
        return self.__weight
    
    def setWeight(self, weight):
        self.__weight = weight
    
    def addUI(self, is_on_switch=False):
        if is_on_switch:
            return super().addUI(ImageConfig.IMAGE_STONE_ON_SWITCH)
        else:
            return super().addUI(ImageConfig.IMAGE_STONE)
    
    

        