import pygame
pygame.font.init()

class UIConfig:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 600
    
    CAPTION = "Sokoban - Ares and Stones"
    
    TILE_SIZE = 40

    # Offset
    OFFSET_X = 40
    OFFSET_Y = 100
    
    MOVE_SPEED = 5  # pixel per frame
    
    # Màu sắc
    # COLOR_BG = (230, 241, 216)
    # COLOR_BG =  (120, 220, 220)
    COLOR_BG =  (255, 255,255)


    COLOR_WALL = (139, 69, 19)
    
    FONT_SIZE = 24

    STONE_FONT = pygame.font.Font(None, 20)
    STATS_FONT = pygame.font.Font(None, 30)
    BTN_FONT = pygame.font.Font(None, 20)
    MSS_FONT  = pygame.font.Font(None, 40)


    BUTTON_HEIGHT = 40
    BUTTON_WIDTH = 80

    RESET_BUTTON_COLOR = (0, 0, 255)
    RESET_BUTTON_TEXT = "RESET"

    CHOICE_BUTTON_COLOR = (200, 0, 200)
    CHOICE_BUTTON_TEXT = "A*"

    LEVEL_BUTTON_COLOR = (200, 0, 200)
    LEVEL_BUTTON_TEXT = "Level"

    
    OPTION_BUTTON_COLOR = (150,150, 150)
    OPTION_BUTTON_TEXT = "A*"



    PLAY_BUTTON_COLOR = (0, 0, 255)
    PLAYING_BUTTON_COLOR = (0, 255, 0)

    PLAY_BUTTON_TEXT = "PLAY"
    PLAYING_BUTTON_TEXT = "PLAYING"

    PAUSE_BUTTON_COLOR = (0, 0, 255)
    PAUSE_BUTTON_TEXT = "PAUSE"