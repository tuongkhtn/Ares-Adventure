from .Object import Object
from config import ImageConfig

class Wall(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        
    def addUI(self, is_3d=False):
        if is_3d:
            return super().addUI(ImageConfig.IMAGE_WALL_3D)
        else:
            return super().addUI(ImageConfig.IMAGE_WALL)