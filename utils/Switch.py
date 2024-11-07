from .Object import Object
from config.ImageConfig import ImageConfig

class Switch(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def addUI(self):
        return super().addUI(ImageConfig.IMAGE_SWITCH)
        