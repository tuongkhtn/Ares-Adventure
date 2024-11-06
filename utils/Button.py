import pygame
from config import UIConfig

class Button():
    def __init__(self, x, y, color, text, height=UIConfig.BUTTON_HEIGHT, width=UIConfig.BUTTON_WIDTH):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def handle(self, gameObject):
        pass

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text

    def draw(self, screen):
        text_surface = UIConfig.BTN_FONT.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        pygame.draw.rect(screen, self.color, self.rect)  # Vẽ nút
        screen.blit(text_surface, text_rect)
