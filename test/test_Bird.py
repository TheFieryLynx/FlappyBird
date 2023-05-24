import unittest
import sys

sys.path.insert(0, '../FlappyBird')

from FlappyBird import Bird, settings

class TestInit(unittest.TestCase):
    def test_init(self):
        bird = Bird()
        # some Bird methods works correctly only for 9 birds
        self.assertEqual(len(bird.birds), 9)
        self.assertEqual(bird.fall, 0)
        self.assertEqual(bird.current_image, 0)
        self.assertEqual(bird.current_bird_idx, 0)
        self.assertEqual(bird.current_bird, bird.birds[0])
        self.assertEqual(bird.image, bird.current_bird[0])
        self.assertEqual(bird.rect, [settings.BIRD_INIT_X, settings.BIRD_INIT_Y])

class TestChangeBird(unittest.TestCase):
    def test_change_bird_right_0(self):
        bird = Bird()
        # works correctly only if there are 9 birds
        self.assertEqual(len(bird.birds), 9)
        before_bird = bird.current_bird_idx
        bird.change_bird_right()
        self.assertEqual(bird.current_bird_idx, before_bird + 1)
