import unittest
import sys
from unittest.mock import MagicMock

sys.path.insert(1, 'FlappyBird')
import FlappyBird


def setUpModule():
    FlappyBird.pygame = MagicMock()
    FlappyBird.pygame.image.load().convert_alpha().get_rect = MagicMock(return_value=[0, 0])


class TestInit(unittest.TestCase):
    def test_background_init(self):
        background = FlappyBird.Background()
        self.assertGreater(len(background.backgrounds), 0)
        self.assertEqual(background.current_background, 0)


class TestChangeBackground(unittest.TestCase):
    def setUp(self):
        self.background = FlappyBird.Background()

    def test_change_background_right(self):
        self.assertEqual(self.background.current_background, 0)
        for i in range(1, len(self.background.backgrounds)):
            self.background.change_background_right()
            self.assertEqual(self.background.current_background, i)
        # go cyclically
        self.background.change_background_right()
        self.assertEqual(self.background.current_background, 0)

    def test_change_background_left(self):
        self.assertEqual(self.background.current_background, 0)
        # go cyclically
        self.background.change_background_left()
        self.assertEqual(self.background.current_background,
                         len(self.background.backgrounds) - 1)
        for i in range(len(self.background.backgrounds) - 2, -1, -1):
            self.background.change_background_left()
            self.assertEqual(self.background.current_background, i)


class TestGetImage(unittest.TestCase):
    def test_get_image(self):
        background = FlappyBird.Background()
        self.assertEqual(background.get_image(),
                         background.backgrounds[background.current_background])
