from utils import Button
from config import UIConfig

class PauseButton(Button):
    def __init__(self, x, y):
        super.__init__(x, y, UIConfig.PAUSE_BUTTON_COLOR, UIConfig.PAUSE_BUTTON_TEXT)
    
    def handle(self):
        pass