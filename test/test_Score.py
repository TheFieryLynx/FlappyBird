import unittest
import sys
from unittest.mock import MagicMock, ANY

sys.path.insert(1, 'FlappyBird')
import FlappyBird

def setUpModule():
    FlappyBird.pygame = MagicMock()

class TestInit(unittest.TestCase):
    def test_score_init(self):
        FlappyBird.pygame.image.load().get_width = MagicMock(return_value=100)
        score = FlappyBird.Score()
        # there are 10 numbers
        self.assertEqual(len(score.lil_nums), 10)
        self.assertEqual(len(score.big_nums), 10)
        self.assertEqual(score.score, 0)
        self.assertEqual(score.images, [score.lil_nums[0]])
        self.assertEqual(score.rect,
                         [FlappyBird.settings.WINDOW_WIDTH - score.offset - 100, 10])

class TestCounting(unittest.TestCase):
    def setUp(self):
        self.score = FlappyBird.Score()

    def test_increase(self):
        self.assertEqual(self.score.score, 0)
        # with one-digit numbers
        self.score.increase()
        self.assertEqual(self.score.score, 1)
        self.assertEqual(self.score.images, [self.score.lil_nums[1]])
        # with two-digit numbers
        self.score.score = 19
        self.score.increase()
        self.assertEqual(self.score.score, 20)
        self.assertEqual(self.score.images,
                         [self.score.lil_nums[2], self.score.lil_nums[0]])
    
    def test_reset(self):
        # change the score
        self.score.increase()
        # resest
        self.score.reset()
        self.assertEqual(self.score.score, 0)
        self.assertEqual(self.score.images, [self.score.lil_nums[0]])

class TestShowScore(unittest.TestCase):
    def setUp(self):
        self.score = FlappyBird.Score()
        self.screen = FlappyBird.Screen()
        self.screen.blit = MagicMock()
    
    def test_update(self):
        self.score.update(self.screen)
        for num in str(self.score.score):
            self.screen.blit.assert_called_with(self.score.lil_nums[int(num)], ANY)

    def test_show(self):
        self.score.show(self.screen)
        for num in str(self.score.score):
            self.screen.blit.assert_called_with(self.score.big_nums[int(num)], ANY)
