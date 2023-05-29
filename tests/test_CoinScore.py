import unittest
import sys
from unittest.mock import MagicMock, ANY

sys.path.insert(1, 'FlappyBird')
import FlappyBird


def setUpModule():
    FlappyBird.pygame = MagicMock()


class TestInit(unittest.TestCase):
    def test_score_init(self):
        score = FlappyBird.CoinScore()
        # there are 10 numbers
        self.assertEqual(score.coin, FlappyBird.pygame.image.load().convert_alpha())
        self.assertEqual(len(score.lil_nums), 10)
        self.assertEqual(score.score, 0)
        self.assertEqual(score.images, [score.lil_nums[0]])
        self.assertEqual(score.rect, [score.offset, 10])


class TestCounting(unittest.TestCase):
    def setUp(self):
        self.score = FlappyBird.CoinScore()

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
    def test_update(self):
        score = FlappyBird.CoinScore()
        screen = FlappyBird.Screen()
        screen.blit = MagicMock()
        score.update(screen)
        for num in str(score.score):
            screen.blit.assert_called_with(score.lil_nums[int(num)], ANY)
