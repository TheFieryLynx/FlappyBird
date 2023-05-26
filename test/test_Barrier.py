import unittest
import sys
from unittest.mock import MagicMock

sys.path.insert(1, 'FlappyBird')
import FlappyBird

def setUpModule():
    FlappyBird.pygame = MagicMock()
    FlappyBird.pygame.image.load().convert_alpha().get_rect = MagicMock(return_value=[0, 0])

class TestInit(unittest.TestCase):
    def test_barrier_init(self):
        barrier = FlappyBird.Barrier()
        self.assertGreater(len(barrier.barriers), 0)
        self.assertEqual(barrier.current_barrier_idx, 0)
        self.assertEqual(barrier.image, barrier.barriers[0])
        barrier.image.get_rect.assert_called_with()
        self.assertEqual(barrier.rect,
                         [FlappyBird.settings.BARRIER_INIT_X, FlappyBird.settings.BARRIER_INIT_Y])

class TestChangeBarrier(unittest.TestCase):
    def setUp(self):
        self.barrier = FlappyBird.Barrier()

    def test_change_barrier_right(self):
        self.assertEqual(self.barrier.current_barrier_idx, 0)
        for i in range(1, len(self.barrier.barriers)):
            self.barrier.change_barrier_right()
            self.assertEqual(self.barrier.current_barrier_idx, i)
        # go cyclically
        self.barrier.change_barrier_right()
        self.assertEqual(self.barrier.current_barrier_idx, 0)

    def test_change_barrier_left(self):
        self.assertEqual(self.barrier.current_barrier_idx, 0)
        # go cyclically
        self.barrier.change_barrier_left()
        self.assertEqual(self.barrier.current_barrier_idx, len(self.barrier.barriers) - 1)
        for i in range(len(self.barrier.barriers) - 2, -1, -1):
            self.barrier.change_barrier_left()
            self.assertEqual(self.barrier.current_barrier_idx, i)

class TestGetCenterPosition(unittest.TestCase):
    def test_get_center_position(self):
        barrier = FlappyBird.Barrier()
        self.assertEqual(barrier.rect,
                         [FlappyBird.settings.BARRIER_INIT_X, FlappyBird.settings.BARRIER_INIT_Y])
        barrier.image.get_width = MagicMock(return_value=(100))
        barrier.image.get_height = MagicMock(return_value=(100))
        center_pos = barrier.get_center_position()
        # the barrier position didn't change
        self.assertEqual(barrier.rect,
                         [FlappyBird.settings.BARRIER_INIT_X, FlappyBird.settings.BARRIER_INIT_Y])
        barrier.image.get_width.assert_called_with()
        barrier.image.get_height.assert_called_with()
        self.assertEqual(center_pos[0], barrier.rect[0] + 50)
        self.assertEqual(center_pos[1], barrier.rect[1] + 50)


class TestPosition(unittest.TestCase):
    def setUp(self):
        self.barrier = FlappyBird.Barrier()
    
    def test_update(self):
        before_coord = self.barrier.rect[0]
        # moving left
        self.barrier.update()
        self.assertEqual(self.barrier.rect[0], before_coord - FlappyBird.settings.BARRIER_SPEED)

    def test_reset(self):
        self.barrier.update()
        # coords changed
        self.barrier.reset()
        self.assertEqual(self.barrier.rect,
                         [FlappyBird.settings.BARRIER_INIT_X, FlappyBird.settings.BARRIER_INIT_Y])
