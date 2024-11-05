from config.UIConfig import UIConfig
from .Object import Object
from config import ImageConfig

class Wall(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        
    def addUI(self):
        return super().addUI(ImageConfig.IMAGE_WALL, height=UIConfig.TILE_SIZE * 1.3)
    
    def draw(self, screen):
        self.screen_position = [self._y * UIConfig.TILE_SIZE + UIConfig.OFFSET_X, self._x * UIConfig.TILE_SIZE - 0.3 * UIConfig.TILE_SIZE + UIConfig.OFFSET_Y]
        screen.blit(self.image, (self.screen_position[0], self.screen_position[1]))
