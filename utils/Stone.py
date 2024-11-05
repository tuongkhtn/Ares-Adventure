from .Object import Object
from config import ImageConfig, UIConfig
from utils import Action

class Stone(Object):
    def __init__(self, x, y, weight):
        super().__init__(x, y)
        self.__weight = weight
        
    def getWeight(self):
        return self.__weight
    
    def setWeight(self, weight):
        self.__weight = weight
    
    def addUI(self):
        return super().addUI(ImageConfig.IMAGE_STONE)
        
    def move(self, action: Action):
        self._x = action.getCoordinate()[0]
        self._y = action.getCoordinate()[1]

        self.screen_position = [
            self._y * UIConfig.TILE_SIZE + UIConfig.OFFSET_X,
            self._x * UIConfig.TILE_SIZE + UIConfig.OFFSET_Y
        ]
    
    def draw(self, screen):
        super().draw(screen)
        weight_text = UIConfig.FONT.render(str(self.__weight), True, (0, 0, 0))
        weight_text_rect = weight_text.get_rect(center=(self.screen_position[0] + UIConfig.TILE_SIZE // 2, self.screen_position[1] + UIConfig.TILE_SIZE // 2))
        screen.blit(weight_text, weight_text_rect)

        