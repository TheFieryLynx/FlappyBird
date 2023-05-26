import unittest
import sys
from unittest.mock import MagicMock

sys.path.insert(1, 'FlappyBird')
import FlappyBird

def setUpModule():
    FlappyBird.pygame = MagicMock()
    FlappyBird.pygame.display.set_mode = MagicMock()

class TestInit(unittest.TestCase):
    def test_screen_init(self):
        screen = FlappyBird.Screen()
        FlappyBird.pygame.display.set_mode.assert_called_with((
            FlappyBird.settings.WINDOW_WIDTH,
            FlappyBird.settings.WINDOW_HEIGHT
        ))
        self.assertEqual(screen.screen, FlappyBird.pygame.display.set_mode())
        self.assertEqual(screen.state, FlappyBird.ScreenState.MENU)

class TestBlit(unittest.TestCase):
    def test_blit(self):
        screen = FlappyBird.Screen()
        screen.blit('image', 'offset')
        screen.screen.blit.assert_called_with('image', 'offset')
