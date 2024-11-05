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
        
    def move(self):
        target_x = self._y * UIConfig.TILE_SIZE
        target_y = self._x * UIConfig.TILE_SIZE
        if self.screen_position[0] < target_x:
            self.screen_position[0] += min(UIConfig.MOVE_SPEED, target_x - self.screen_position[0])
        elif self.screen_position[0] > target_x:
            self.screen_position[0] -= min(UIConfig.MOVE_SPEED, self.screen_position[0] - target_x)
        if self.screen_position[1] < target_y:
            self.screen_position[1] += min(UIConfig.MOVE_SPEED, target_y - self.screen_position[1])
        elif self.screen_position[1] > target_y:
            self.screen_position[1] -= min(UIConfig.MOVE_SPEED, self.screen_position[1] - target_y)
    
    

        