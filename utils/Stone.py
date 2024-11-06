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
        
    def move(self):
        target_x = self._y * UIConfig.TILE_SIZE + UIConfig.OFFSET_X
        target_y = self._x * UIConfig.TILE_SIZE + UIConfig.OFFSET_Y
        if self.screen_position[0] < target_x:
            self.screen_position[0] += min(UIConfig.MOVE_SPEED, target_x - self.screen_position[0])
        elif self.screen_position[0] > target_x:
            self.screen_position[0] -= min(UIConfig.MOVE_SPEED, self.screen_position[0] - target_x)
        if self.screen_position[1] < target_y:
            self.screen_position[1] += min(UIConfig.MOVE_SPEED, target_y - self.screen_position[1])
        elif self.screen_position[1] > target_y:
            self.screen_position[1] -= min(UIConfig.MOVE_SPEED, self.screen_position[1] - target_y)    
    
    def draw(self, screen, offset_x=0, offset_y=0):
        super().draw(screen, offset_x, offset_y)
        weight_text = UIConfig.STONE_FONT.render(str(self.__weight), True, (0, 0, 0))
        weight_text_rect = weight_text.get_rect(center=(self.screen_position[0] + offset_x + UIConfig.TILE_SIZE // 2, self.screen_position[1] + offset_y + UIConfig.TILE_SIZE // 2))
        screen.blit(weight_text, weight_text_rect)

        