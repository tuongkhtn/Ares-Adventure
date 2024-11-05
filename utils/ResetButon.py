from utils import Button
from config import UIConfig

class ResetButton(Button):
    def __init__(self, x, y):
        super().__init__(x, y, UIConfig.RESET_BUTTON_COLOR, UIConfig.RESET_BUTTON_TEXT)
    
    def handle(self):
        pass