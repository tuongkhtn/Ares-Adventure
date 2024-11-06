from utils import Button
from config import UIConfig
import pygame

class ALert(Button):
    def __init__(self):
        super().__init__(UIConfig.WINDOW_WIDTH//2 - UIConfig.ALERT_WIDTH//2, UIConfig.WINDOW_HEIGHT//2 - UIConfig.ALERT_HEIGHT//2, UIConfig.ALERT_COLOR, text="")
        self.setHeight(UIConfig.ALERT_HEIGHT)
        self.setWidth(UIConfig.ALERT_WIDTH)
        self.textColor = UIConfig.ALERT_TEXT_COLOR
        self.textFont = UIConfig.ALERT_FONT
    
    def setText(self, text, textColor = UIConfig.ALERT_TEXT_COLOR):
        self.textColor = textColor
        self.text = text

    