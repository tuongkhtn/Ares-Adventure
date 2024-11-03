from .ObjectGraphic import ObjectGraphic
from config import UIConfig
from config import ImageConfig

class AresGraphic(ObjectGraphic):
    def __init__(self, position):
        super().__init__(position, ImageConfig.IMAGE_ARES)
        
    def move(self, new_position):
        self.position = new_position
        self.screen_position = [new_position[1] * UIConfig.TILE_SIZE + UIConfig.OFFSET_X, new_position[0] * UIConfig.TILE_SIZE + UIConfig.OFFSET_Y]