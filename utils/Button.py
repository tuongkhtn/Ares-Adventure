import pygame
from config import UIConfig

class Button():
    def __init__(self, x, y, color, text):
        self.x = x
        self.y = y
        self.height = UIConfig.BUTTON_HEIGHT
        self.width = UIConfig.BUTTON_WIDTH
        self.color = color
        self.text = text
    
    def handle(self):
        pass

    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        text_surface = UIConfig.STATS_FONT.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        pygame.draw.rect(screen, self.color, rect)  # Vẽ nút
        screen.blit(text_surface, text_rect)
