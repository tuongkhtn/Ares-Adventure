import pygame
pygame.font.init()


class UIConfig:
    # Kích thước cửa sổ
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 600
    
    # Caption
    CAPTION = "Sokoban - Ares and Stones"
    
    # Kích thước ô
    TILE_SIZE = 40

    # Offset
    OFFSET_X = 40
    OFFSET_Y = 80
    
    # Biến tốc độ di chuyển
    MOVE_SPEED = 5  # pixel per frame
    
    # Màu sắc
    COLOR_BG = (230, 241, 216)# Màu nền xanh da trời nhạt
    COLOR_WALL = (139, 69, 19)  # Màu tường nâu
    
    FONT_SIZE = 24
    
    STATS_FONT = pygame.font.Font(None, 36)
    
    BUTTON_HEIGHT = 40
    BUTTON_WIDTH = 80
    
    RESET_BUTTON_COLOR = (0, 0, 255)
    RESET_BUTTON_TEXT = "RESET"

    PLAY_BUTTON_COLOR = (0, 0, 255)
    PLAY_BUTTON_TEXT = "PLAY"

    PAUSE_BUTTON_COLOR = (0, 0, 255)
    PAUSE_BUTTON_TEXT = "PAUSE"