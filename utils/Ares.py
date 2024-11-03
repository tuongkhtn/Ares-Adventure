from .Object import Object
from config import ImageConfig

class Ares(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def addUI(self):
        return super().addUI(ImageConfig.IMAGE_ARES)