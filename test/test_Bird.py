import unittest
import sys
from unittest.mock import MagicMock

sys.path.insert(1, 'FlappyBird')
import FlappyBird

def setUpModule():
    FlappyBird.pygame = MagicMock()
    FlappyBird.pygame.image.load().convert_alpha().get_rect = MagicMock(return_value=[0, 0])

class TestInit(unittest.TestCase):
    def test_init(self):
        bird = FlappyBird.Bird()
        # some Bird methods works correctly only for 9 birds
        self.assertEqual(len(bird.birds), 9)
        self.assertEqual(bird.fall, 0)
        self.assertEqual(bird.current_image, 0)
        self.assertEqual(bird.current_bird_idx, 0)
        self.assertEqual(bird.current_bird, bird.birds[0])
        self.assertEqual(bird.image, bird.current_bird[0])
        bird.image.get_rect.assert_called_with()
        self.assertEqual(bird.rect,
                         [FlappyBird.settings.BIRD_INIT_X, FlappyBird.settings.BIRD_INIT_Y])

class TestChangeBird(unittest.TestCase):
    def setUp(self):
        self.bird = FlappyBird.Bird()

    def test_change_bird_right(self):
        # works correctly only if there are 9 birds
        self.assertEqual(len(self.bird.birds), 9)
        for i in range(0, 9, 3):
            self.bird.current_bird_idx = i
            self.bird.change_bird_right()
            self.assertEqual(self.bird.current_bird_idx, i + 1)
            self.bird.change_bird_right()
            self.assertEqual(self.bird.current_bird_idx, i + 2)
            # go cyclically
            self.bird.change_bird_right()
            self.assertEqual(self.bird.current_bird_idx, i)

    def test_change_bird_left(self):
        # works correctly only if there are 9 birds
        self.assertEqual(len(self.bird.birds), 9)
        for i in range(2, 9, 3):
            self.bird.current_bird_idx = i
            self.bird.change_bird_left()
            self.assertEqual(self.bird.current_bird_idx, i - 1)
            self.bird.change_bird_left()
            self.assertEqual(self.bird.current_bird_idx, i - 2)
            # go cyclically
            self.bird.change_bird_left()
            self.assertEqual(self.bird.current_bird_idx, i)

    def test_change_bird_up(self):
        # works correctly only if there are 9 birds
        self.assertEqual(len(self.bird.birds), 9)
        for i in range(6, 9):
            self.bird.current_bird_idx = i
            self.bird.change_bird_up()
            self.assertEqual(self.bird.current_bird_idx, i - 3)
            self.bird.change_bird_up()
            self.assertEqual(self.bird.current_bird_idx, i - 6)
            # go cyclically
            self.bird.change_bird_up()
            self.assertEqual(self.bird.current_bird_idx, i)

    def test_change_bird_down(self):
        # works correctly only if there are 9 birds
        self.assertEqual(len(self.bird.birds), 9)
        for i in range(0, 3):
            self.bird.current_bird_idx = i
            self.bird.change_bird_down()
            self.assertEqual(self.bird.current_bird_idx, i + 3)
            self.bird.change_bird_down()
            self.assertEqual(self.bird.current_bird_idx, i + 6)
            # go cyclically
            self.bird.change_bird_down()
            self.assertEqual(self.bird.current_bird_idx, i)


class TestFly(unittest.TestCase):
    def setUp(self):
        self.bird = FlappyBird.Bird()

    def test_fly(self):
        self.assertEqual(self.bird.current_image, 0)
        self.bird.fly()
        self.assertEqual(self.bird.current_image, 1)
        self.assertEqual(self.bird.image, self.bird.current_bird[self.bird.current_image])
        self.bird.fly()
        self.assertEqual(self.bird.current_image, 0)
        self.assertEqual(self.bird.image, self.bird.current_bird[self.bird.current_image])
    
    def test_jump(self):
        self.bird.jump()
        self.assertEqual(self.bird.fall, -27)
    
    def test_update(self):
        before_coord = self.bird.rect[1]
        self.assertEqual(self.bird.fall, 0)
        self.bird.fly = MagicMock()
        # slowly falling
        self.bird.update()
        self.bird.fly.assert_called_with()
        self.assertEqual(self.bird.fall, 3)
        self.assertEqual(self.bird.rect[1], before_coord + self.bird.fall)
        # jump
        before_coord += 3
        self.bird.jump()
        self.bird.update()
        self.bird.fly.assert_called_with()
        self.assertEqual(self.bird.fall, -24)
        self.assertEqual(self.bird.rect[1], before_coord + self.bird.fall)

    def test_reset(self):
        self.bird.jump()
        self.bird.update()
        # coords & fall changed
        self.bird.reset()
        self.assertEqual(self.bird.rect,
                         [FlappyBird.settings.BIRD_INIT_X, FlappyBird.settings.BIRD_INIT_Y])
        self.assertEqual(self.bird.fall, 0)
