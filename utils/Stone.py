from .Object import Object
from config import ImageConfig, UIConfig
from utils import Action

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
        
    def move(self, action: Action):
        self.screen_position = [
            self._y * UIConfig.TILE_SIZE + UIConfig.OFFSET_X,
            self._x * UIConfig.TILE_SIZE + UIConfig.OFFSET_Y
        ]
    
    

        