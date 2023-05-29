import unittest
import sys
from unittest.mock import MagicMock

sys.path.insert(1, 'FlappyBird')
import FlappyBird


def setUpModule():
    FlappyBird.pygame = MagicMock()
    FlappyBird.pygame.image.load().convert_alpha().get_rect = MagicMock(return_value=[0, 0])


class TestInit(unittest.TestCase):
    def test_coin_init(self):
        coin = FlappyBird.Coin()
        self.assertEqual(len(coin.coins), coin.STATES)
        self.assertEqual(coin.cur_coin_idx, 0)
        self.assertEqual(coin.image, coin.coins[0])
        coin.image.get_rect.assert_called_with()
        self.assertEqual(coin.rect,
                         [FlappyBird.settings.WINDOW_WIDTH, FlappyBird.settings.WINDOW_HEIGHT])


class TestPosition(unittest.TestCase):
    def setUp(self):
        self.coin = FlappyBird.Coin()

    def test_set_position(self):
        self.coin.set_position(100, 500)
        self.assertEqual(self.coin.rect, [100, 500])

    def test_update(self):
        before_coord = self.coin.rect[0]
        before_idx = self.coin.cur_coin_idx
        # moving & spinning
        for i in range(self.coin.STATES):
            self.coin.update()
            self.assertEqual(self.coin.cur_coin_idx, (before_idx + 1) % self.coin.STATES)
            self.assertEqual(self.coin.image, self.coin.coins[self.coin.cur_coin_idx])
            self.assertEqual(self.coin.rect[0], before_coord - FlappyBird.settings.BARRIER_SPEED)
            before_coord -= FlappyBird.settings.BARRIER_SPEED
            before_idx = (before_idx + 1) % self.coin.STATES

    def test_reset(self):
        self.coin.update()
        # coords changed
        self.coin.reset()
        self.assertEqual(self.coin.rect,
                         [FlappyBird.settings.WINDOW_WIDTH, FlappyBird.settings.WINDOW_HEIGHT])
