import pygame
from config.UIConfig import UIConfig

class Button():
    def __init__(self, x, y, color, text, height=UIConfig.BUTTON_HEIGHT, width=UIConfig.BUTTON_WIDTH, corner_radius=10):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.corner_radius = corner_radius
        self.textColor = UIConfig.DEFAULT_TEXT_COLOR
        self.textFont = UIConfig.BTN_FONT
    
    def handle(self, gameObject):
        pass

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text
    def setHeight(self, height):
        self.height = height

    def setWidth(self, width):
        self.width = width
    
    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setTextColor(self, color):
        self.textColor = color

    def setTextFont(self, font):
        self.textFont = font
    def draw(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.corner_radius)
        
        text_surface = self.textFont.render(self.text, True, self.textColor)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
