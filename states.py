from enum import Enum

class ScreenState(Enum):
    MENU = 0
    BACKGROUND_SETTINGS = 1
    BIRD_SETTINGS = 2
    BARRIER_SETTINGS = 3
    GAME_OVER = 4
    PLAY = 5