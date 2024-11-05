from .Object import Object
from config import ImageConfig, UIConfig
from .Action import Action

class Ares(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def addUI(self):
        return super().addUI(ImageConfig.IMAGE_ARES) 
    
    def move(self):
        target_x = self._y * UIConfig.TILE_SIZE + UIConfig.OFFSET_X
        target_y = self._x * UIConfig.TILE_SIZE + UIConfig.OFFSET_Y
        if self.screen_position[0] < target_x:
            self.screen_position[0] += min(UIConfig.MOVE_SPEED, target_x - self.screen_position[0])
        elif self.screen_position[0] > target_x:
            self.screen_position[0] -= min(UIConfig.MOVE_SPEED, self.screen_position[0] - target_x)
            
        if self.screen_position[1] < target_y:
            self.screen_position[1] += min(UIConfig.MOVE_SPEED, target_y - self.screen_position[1])
        elif self.screen_position[1] > target_y:
            self.screen_position[1] -= min(UIConfig.MOVE_SPEED, self.screen_position[1] - target_y)