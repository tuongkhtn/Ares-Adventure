from config.UIConfig import UIConfig
from .Object import Object
from config import ImageConfig

class Wall(Object):
    def __init__(self, x, y, is_3d=False):
        super().__init__(x, y)
        self.is_3d = is_3d
        
    def addUI(self):
        if self.is_3d:
            return super().addUI(ImageConfig.IMAGE_WALL_3D, height=UIConfig.TILE_SIZE * 1.25)
        else:
            return super().addUI(ImageConfig.IMAGE_WALL)
    
    def draw(self, screen):
        self.screen_position = [self._y * UIConfig.TILE_SIZE, self._x * UIConfig.TILE_SIZE]
        screen.blit(self.image, (self.screen_position[0] + UIConfig.OFFSET_X, self.screen_position[1] + UIConfig.OFFSET_Y))