import pygame
import time
import random
from enum import Enum
import os
import sys

# local imports
import settings


class ScreenState(Enum):
    """Enum representing all possible game screen states."""

    MENU = 0
    BACKGROUND_SETTINGS = 1
    BIRD_SETTINGS = 2
    BARRIER_SETTINGS = 3
    GAME_OVER = 4
    PLAY = 5


class Bird(pygame.sprite.Sprite):
    """Class representing and controlling a bird's sprite in the game."""

    def __init__(self):
        """Initialize the bird."""
        pygame.sprite.Sprite.__init__(self)

        self.birds = []
        for i in range(9):
            self.birds.append([
                pygame.image.load(
                    f'FlappyBird/assets/birds/bird-{i}-up.png').convert_alpha(),
                pygame.image.load(
                    f'FlappyBird/assets/birds/bird-{i}-down.png').convert_alpha()
            ])
        self.fall = 0
        self.current_image = 0
        self.current_bird_idx = 0
        self.current_bird = self.birds[self.current_bird_idx]
        self.image = self.current_bird[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.set_position()

    def set_position(self):
        """Set initial bird's coordinates corresponding to settings."""
        self.rect = self.image.get_rect()
        self.rect[0] = settings.BIRD_INIT_X
        self.rect[1] = settings.BIRD_INIT_Y

    def change_bird_right(self):
        """Change the chosen bird to the right side bird on the screen (cyclically)."""
        self.current_bird_idx = (self.current_bird_idx // 3) * 3 + (self.current_bird_idx + 1) % 3
        self.current_bird = self.birds[self.current_bird_idx]
        self.image = self.current_bird[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)

    def change_bird_left(self):
        """Change the chosen bird to the left side bird on the screen (cyclically)."""
        self.current_bird_idx = self.current_bird_idx // 3 * 3 + (self.current_bird_idx - 1) % 3
        self.current_bird = self.birds[self.current_bird_idx]
        self.image = self.current_bird[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)

    def change_bird_up(self):
        """Change the chosen bird to the bird up on the screen (cyclically)."""
        self.current_bird_idx = (self.current_bird_idx - 3) % 9
        self.current_bird = self.birds[self.current_bird_idx]
        self.image = self.current_bird[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)

    def change_bird_down(self):
        """Change the chosen bird to the bird below on the screen (cyclically)."""
        self.current_bird_idx = (self.current_bird_idx + 3) % 9
        self.current_bird = self.birds[self.current_bird_idx]
        self.image = self.current_bird[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)

    def fly(self):
        """Change the bird's picture to a picture depicting the next position of the bird."""
        self.current_image = (self.current_image + 1) % 2
        self.image = self.current_bird[self.current_image]

    def jump(self):
        """Imitate the bird's jump up."""
        self.fall = -27

    def update(self):
        """Imitate the bird moving forward and falling."""
        self.fly()
        self.fall += 3
        self.rect[1] += self.fall

    def reset(self):
        """Reset the bird's position to initial and stop the bird from falling."""
        self.set_position()
        self.fall = 0


class Barrier(pygame.sprite.Sprite):
    """Class representing and controlling a barrier's sprite in the game."""

    def __init__(self):
        """Initialize the barrier."""
        pygame.sprite.Sprite.__init__(self)
        self.barriers = []
        for i in range(2):
            self.barriers.append(
                pygame.image.load(f'FlappyBird/assets/barriers/barrier-{i}.png').convert_alpha(),
            )
        self.current_barrier_idx = 0
        self.image = self.barriers[self.current_barrier_idx]
        self.mask = pygame.mask.from_surface(self.image)
        self.set_position(-100, -250)

    def change_barrier_right(self):
        """Change the chosen barrier to the right side barrier on the screen (cyclically)."""
        self.current_barrier_idx = (
            self.current_barrier_idx + 1) % len(self.barriers)
        self.image = self.barriers[self.current_barrier_idx]
        self.mask = pygame.mask.from_surface(self.image)

    def change_barrier_left(self):
        """Change the chosen barrier to the left side barrier on the screen (cyclically)."""
        self.current_barrier_idx = (
            self.current_barrier_idx - 1) % len(self.barriers)
        self.image = self.barriers[self.current_barrier_idx]
        self.mask = pygame.mask.from_surface(self.image)

    def set_position(self, x, y):
        """Set barrier's coordinates.

        :param x: Horizontal coordinate value to set.
        :type x: int
        :param y: Vertical coordinate value to set.
        :type y: int
        """
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y

    def get_center_position(self):
        """Return the barrier's current center coordinates."""
        return (
            self.rect[0] + self.image.get_width() // 2,
            self.rect[1] + self.image.get_height() // 2)

    def reset(self):
        """Reset the barrier's position to initial."""
        self.set_position(settings.BARRIER_INIT_X, settings.BARRIER_INIT_Y)

    def update(self):
        """Imitate the barrier moving towards the bird."""
        self.rect[0] -= settings.BARRIER_SPEED


class Coin(pygame.sprite.Sprite):
    """Class representing and controlling a coin's sprite in the game."""

    SIZE = 32

    def __init__(self):
        """Initialize the coin."""
        pygame.sprite.Sprite.__init__(self)
        self.STATES = 5

        self.coins = [
            pygame.image.load(f'FlappyBird/assets/coins/coin-{i}-big.png').convert_alpha()
            for i in range(self.STATES)]
        self.cur_coin_idx = 0
        self.image = self.coins[self.cur_coin_idx]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.reset()

    def set_position(self, x, y):
        """Set coin's coordinates.

        :param x: Horizontal coordinate value to set.
        :type x: int
        :param y: Vertical coordinate value to set.
        :type y: int
        """
        self.rect[0] = x
        self.rect[1] = y

    def update(self):
        """Change the coin's to a picture depicting the next position of the coin.
        Move the coin towards the bird.
        """
        self.cur_coin_idx = (self.cur_coin_idx + 1) % len(self.coins)
        self.image = self.coins[self.cur_coin_idx]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect[0] -= settings.BARRIER_SPEED

    def reset(self):
        """Reset the coin's position to initial."""
        self.set_position(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)


class Background():
    """Class representing and controlling the game's background."""

    def __init__(self):
        """Initialize the backround."""
        self.backgrounds = []
        for i in range(3):
            self.backgrounds.append(
                pygame.image.load(f'FlappyBird/assets/backgrounds/background-{i}.png'),
            )
        self.current_background = 0

    def change_background_right(self):
        """Change the chosen baackground to the right side background on the screen (cyclically)."""
        self.current_background = (
            self.current_background + 1) % len(self.backgrounds)

    def change_background_left(self):
        """Change the chosen baackground to the left side background on the screen (cyclically)."""
        self.current_background = (
            self.current_background - 1) % len(self.backgrounds)

    def get_image(self):
        """Return current background image."""
        return self.backgrounds[self.current_background]


class Screen():
    """Class representing and controlling the game's screen."""

    def __init__(self):
        """Initialize the screen."""
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.state = ScreenState.MENU

    def blit(self, image, offset):
        """Display an image on the scrren.

        :param image: Image to display.
        :type image: pygame.Surface
        :param offset: Horizontal and vertical screen offset to display the image.
        :type offset: list
        """
        self.screen.blit(image, offset)


class Frame(pygame.sprite.Sprite):
    """Class representing and controlling the game's frame.
    Frame is a thin line at the bottom of the screen, which is needed
    to control the fall of the bird to the ground.
    """

    def __init__(self):
        """Initialize the frame."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('FlappyBird/assets/ground.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 0


class CoinScore():
    """Class representing and controlling the player's coin score."""

    def __init__(self):
        """Initialize the coin score."""
        self.offset = 10
        self.coin = pygame.image.load('FlappyBird/assets/coins/coin-0-big.png').convert_alpha()
        self.lil_nums = [pygame.image.load(
            f'FlappyBird/assets/numbers/{i}-little.png') for i in range(10)]
        self.score = 0
        self.images = [self.lil_nums[0]]
        self.rect = []
        self.rect.append(self.offset)
        self.rect.append(10)

    def increase(self):
        """Increase the player's coin score by one."""
        self.score += 1
        self.images.clear()
        for num in str(self.score):
            self.images.append(self.lil_nums[int(num)])

    def reset(self):
        """Reset the player's coin score to zero."""
        self.score = 0
        self.images = [self.lil_nums[0]]

    def update(self, screen: Screen):
        """Display current coin score on the screen.

        :param screen: Game's screen.
        :type screen: Screen
        """
        screen.blit(self.coin, self.rect)
        cur_offset = self.coin.get_width() + 5
        for image in self.images:
            screen.blit(image, [self.rect[0] + cur_offset, self.rect[1]])
            cur_offset += image.get_width()


class Score():
    """Class representing and controlling the player's score."""

    def __init__(self):
        """Initialize the score."""
        self.offset = -10
        self.lil_nums = [pygame.image.load(f'FlappyBird/assets/numbers/{i}-little.png') for i in range(10)]
        self.big_nums = [pygame.image.load(f'FlappyBird/assets/numbers/{i}-big.png') for i in range(10)]
        self.score = 0
        self.images = [self.lil_nums[0]]
        self.rect = []
        self.rect.append(settings.WINDOW_WIDTH - self.offset - self.images[0].get_width())
        self.rect.append(10)

    def increase(self):
        """Increase the player's score by one."""
        self.score += 1
        self.images.clear()
        for num in str(self.score):
            self.images.append(self.lil_nums[int(num)])

    def reset(self):
        """Reset the player's score to zero."""
        self.score = 0
        self.images = [self.lil_nums[0]]

    def update(self, screen: Screen):
        """Display current score on the screen.

        :param screen: Game's screen.
        :type screen: Screen
        """
        cur_offset = 0
        for image in self.images[::-1]:
            cur_offset += image.get_width()
            screen.blit(image, [self.rect[0] - cur_offset, self.rect[1]])

    def show(self, screen: Screen):
        """Display final score on the screen.

        :param screen: Game's screen.
        :type screen: Screen
        """
        offset_y = settings.WINDOW_HEIGHT // 2 - 20
        width = 0
        images = []
        for num in str(self.score):
            img = self.big_nums[int(num)]
            width += img.get_width() + 2
            images.append(img)
        cur_offset_x = settings.WINDOW_WIDTH // 2 - width // 2
        for image in images:
            screen.blit(image, [cur_offset_x, offset_y])
            cur_offset_x += image.get_width() + 2


