from .Object import Object
from config import ImageConfig, UIConfig
from .Action import Action

class Ares(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def addUI(self):
        return super().addUI(ImageConfig.IMAGE_ARES)
    
    def move(self, action: Action):
        self._x = action.getCoordinate()[0]
        self._y = action.getCoordinate()[1]

        self.screen_position = [
            self._y * UIConfig.TILE_SIZE + UIConfig.OFFSET_X,
            self._x * UIConfig.TILE_SIZE + UIConfig.OFFSET_Y
        ]