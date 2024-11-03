from .ObjectGraphic import ObjectGraphic
from config import ImageConfig

class WallGraphic(ObjectGraphic):
    def __init__(self, position, is_3d=False):
        if is_3d:
            super().__init__(position, ImageConfig.IMAGE_WALL_3D)
        else:
            super().__init__(position, ImageConfig.IMAGE_WALL)