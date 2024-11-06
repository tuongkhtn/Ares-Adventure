import pygame
pygame.font.init()

class UIConfig:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 600
    
    CAPTION = "Sokoban - Ares and Stones"

    DEFAULT_TEXT_COLOR = (0, 0, 0)
    
    TILE_SIZE = 40

    # Offset
    OFFSET_X = 40
    OFFSET_Y = 100
    
    MOVE_SPEED = 5  # pixel per frame
    
    # Màu sắc
    # COLOR_BG = (230, 241, 216)
    # COLOR_BG =  (120, 220, 220)
    COLOR_BG =  (20, 20,20)
    ALPHA = 50


    COLOR_WALL = (139, 69, 19)
    
    FONT_SIZE = 24

    STONE_FONT = pygame.font.Font(None, 20)
    STATS_FONT = pygame.font.Font(None, 30)
    BTN_FONT = pygame.font.Font(None, 20)
    MSS_FONT  = pygame.font.Font(None, 40)


    BUTTON_HEIGHT = 40
    BUTTON_WIDTH = 80

    RESET_BUTTON_COLOR = (12, 81, 201)
    RESET_BUTTON_TEXT = "RESET"

    CHOICE_BUTTON_COLOR = (204, 229, 255)
    CHOICE_BUTTON_TEXT_COLOR = (0, 0, 0)
    CHOICE_BUTTON_TEXT = "DFS"


    LEVEL_BUTTON_COLOR = (204, 229, 255)
    LEVEL_BUTTON_TEXT = "Level"

    
    OPTION_BUTTON_COLOR = (150,150, 150)
    OPTION_BUTTON_TEXT = "A*"



    PLAY_BUTTON_COLOR = (12, 81, 201)
    PLAYING_BUTTON_COLOR = (0, 153, 76)

    PLAY_BUTTON_TEXT = "PLAY"
    PLAYING_BUTTON_TEXT = "PLAYING"

    PLAYING_BUTTON_TEXT_COLOR = (255, 255, 255)
    PLAY_BUTTON_TEXT_COLOR = (0, 0, 0)


    ALERT_WIDTH = 350
    ALERT_HEIGHT = 120
    ALERT_COLOR = (204, 255, 204)
    ALERT_TEXT_COLOR = (0, 0, 0)
    ALERT_FONT_SIZE = 50
    ALERT_FONT = pygame.font.Font(None, ALERT_FONT_SIZE)


    MAP_BUTTON_COLOR = (204, 229, 255)
    MAP_BUTTON_TEXT_COLOR = (0, 0, 0)
    MAP_BUTTON_TEXT = "DFS"