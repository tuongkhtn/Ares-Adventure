import pygame
from utils import Button
from config import UIConfig

class LevelButton(Button):
    def __init__(self, x, y, color=UIConfig.LEVEL_BUTTON_COLOR, text=UIConfig.LEVEL_BUTTON_TEXT):
        super().__init__(x, y, color, text)
    
    def handle(self, screen, buttons):
        white = (255, 255, 255)
        black = (0, 0, 0)

        window_rect = pygame.Rect(UIConfig.WINDOW_WIDTH // 4, UIConfig.WINDOW_HEIGHT // 4, UIConfig.WINDOW_WIDTH // 2, UIConfig.WINDOW_HEIGHT // 2)
        pygame.draw.rect(screen, white, window_rect)
        pygame.draw.rect(screen, black, window_rect, 2)

        title_text = UIConfig.STATS_FONT.render("SELECT LEVEL", True, black)
        title_rect = title_text.get_rect(center=(UIConfig.WINDOW_WIDTH // 2, UIConfig.WINDOW_HEIGHT // 4 + 50))

        screen.blit(title_text, title_rect)

        for button in buttons:
            button.draw(screen)