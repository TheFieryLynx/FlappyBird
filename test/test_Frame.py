import unittest
import sys
from unittest.mock import MagicMock

sys.path.insert(1, 'FlappyBird')
import FlappyBird

def setUpModule():
    FlappyBird.pygame = MagicMock()
    FlappyBird.pygame.image.load().convert_alpha().get_rect = MagicMock(return_value=[0, 0])

class TestInit(unittest.TestCase):
    def test_frame_init(self):
        frame = FlappyBird.Frame()
        self.assertEqual(frame.image, FlappyBird.pygame.image.load().convert_alpha())
        frame.image.get_rect.assert_called_with()
        self.assertEqual(frame.rect, [0, 0])