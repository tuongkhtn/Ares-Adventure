from utils import Button
from config import UIConfig

class ChoiceButton(Button):
    def __init__(self, x, y, color =   UIConfig.CHOICE_BUTTON_COLOR, text = UIConfig.CHOICE_BUTTON_TEXT):
        super().__init__(x, y, color, text)
    
    def handle(self, gameObject):
        pass