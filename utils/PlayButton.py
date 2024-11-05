from utils import Button
from config import UIConfig

class PlayButton(Button):
    def __init__(self, x, y):
        super().__init__(x, y, UIConfig.PLAY_BUTTON_COLOR, UIConfig.PLAY_BUTTON_TEXT)
    
    def handle(self):
        print("hello")