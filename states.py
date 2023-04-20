from enum import Enum

class ScreenState(Enum):
    MENU = 0
    BACKGROUND_SETTINGS = 1
    BIRD_SETTINGS = 2
    COLUMN_SETTINGS = 3
    GAME_OVER = 4
    PLAY = 5