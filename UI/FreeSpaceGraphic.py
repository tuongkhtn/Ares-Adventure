from .ObjectGraphic import ObjectGraphic
from config import ImageConfig

class FreeSpaceGraphic(ObjectGraphic):
    def __init__(self, position):
        super().__init__(position, ImageConfig.IMAGE_FREE_SPACE)