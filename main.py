import os
import pygame
import time
import random

from enum import Enum

#local imports
import settings
from states import ScreenState

MENU_LAYOUT = pygame.image.load('assets/layouts/menu-layout.png')
BACKGROUND_SETTINGS_LAYOUT = pygame.image.load('assets/layouts/background-settings-layout.png')
BIRD_SETTINGS_LAYOUT = pygame.image.load('assets/layouts/bird-settings-layout.png')
BARRIER_SETTINGS_LAYOUT = pygame.image.load('assets/layouts/barrier-settings-layout.png')
GAME_OVER_LAYOUT = pygame.image.load('assets/layouts/game-over-layout.png')
VERTICAL_FRAME = pygame.image.load('assets/vertical-frame.png')
HORIZONTAL_FRAME = pygame.image.load('assets/horizontal-frame.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.birds = []
        for i in range(9):
            self.birds.append([
                pygame.image.load(f'assets/birds/bird-{i}-up.png').convert_alpha(),
                pygame.image.load(f'assets/birds/bird-{i}-down.png').convert_alpha()
            ])
        self.fall = 0
        self.current_image = 0
        self.current_bird_idx = 0
        self.current_bird = self.birds[self.current_bird_idx]
        self.image = self.current_bird[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.set_position()
        
    def set_position(self):
        self.rect = self.image.get_rect()
        self.rect[0] = settings.BIRD_INIT_X
        self.rect[1] = settings.BIRD_INIT_Y

    def change_bird_right(self):
        if (self.current_bird_idx % 3 != 2):
            self.current_bird_idx = (self.current_bird_idx + 1) % 9
            self.current_bird = self.birds[self.current_bird_idx]
            self.image = self.current_bird[self.current_image]
            self.mask = pygame.mask.from_surface(self.image)

    def change_bird_left(self):
        if (self.current_bird_idx % 3 != 0):
            self.current_bird_idx = (self.current_bird_idx - 1) % 9
            self.current_bird = self.birds[self.current_bird_idx]
            self.image = self.current_bird[self.current_image]
            self.mask = pygame.mask.from_surface(self.image)
    
    def change_bird_up(self):
        if (self.current_bird_idx // 3 != 0):
            self.current_bird_idx = (self.current_bird_idx - 3) % 9
            self.current_bird = self.birds[self.current_bird_idx]
            self.image = self.current_bird[self.current_image]
            self.mask = pygame.mask.from_surface(self.image)
    
    def change_bird_down(self):
        if (self.current_bird_idx // 3 != 2):
            self.current_bird_idx = (self.current_bird_idx + 3) % 9
            self.current_bird = self.birds[self.current_bird_idx]
            self.image = self.current_bird[self.current_image]
            self.mask = pygame.mask.from_surface(self.image)
    
    def set_beige_bird(self):
        self.current_bird = self.birds['beige']

    def fly(self):
        self.current_image = (self.current_image + 1) % 2
        self.image = self.current_bird[self.current_image]
    
    def jump(self):
        self.fall = -27

    def update(self):
        self.fly()
        self.fall += 3
        self.rect[1] += self.fall

    def reset(self):
        self.set_position()
        self.fall = 0

class Barrier(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.barriers = []
        for i in range(2):
            self.barriers.append(
                pygame.image.load(f'assets/barriers/barrier-{i}.png').convert_alpha(),
            )
        self.current_barrier_idx = 0
        self.image = self.barriers[self.current_barrier_idx]
        self.mask = pygame.mask.from_surface(self.image)
        self.set_position(-100, -250)

    def change_barrier_right(self):
        self.current_barrier_idx = (self.current_barrier_idx + 1) % len(self.barriers)
        self.image = self.barriers[self.current_barrier_idx]
        self.mask = pygame.mask.from_surface(self.image)

    def change_barrier_left(self):
        self.current_barrier_idx = (self.current_barrier_idx - 1) % len(self.barriers)
        self.image = self.barriers[self.current_barrier_idx]
        self.mask = pygame.mask.from_surface(self.image)

    def set_position(self, x, y):
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
    
    def get_center_position(self):
        return (
            self.rect[0] + self.image.get_width() // 2,
            self.rect[1] + self.image.get_height() // 2) 

    def reset(self):
        self.set_position(-100, -254)

    def update(self):
        self.rect[0] -= settings.BARRIER_SPEED

class Coin(pygame.sprite.Sprite):
    SIZE = 32

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.STATES = 5

        self.coins = [
            pygame.image.load(f'assets/coins/coin-{i}-big.png').convert_alpha()
            for i in range(self.STATES)]
        self.cur_coin_idx = 0
        self.image = self.coins[self.cur_coin_idx]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.reset()

    def set_position(self, x, y):
        self.rect[0] = x
        self.rect[1] = y
    
    def update(self):
        self.cur_coin_idx = (self.cur_coin_idx + 1) % len(self.coins)
        self.image = self.coins[self.cur_coin_idx]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect[0] -= settings.BARRIER_SPEED
    
    def reset(self):
        self.set_position(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)

class Background():
    def __init__(self):
        self.backgrounds = []
        for i in range(3):
            self.backgrounds.append(
                pygame.image.load(f'assets/backgrounds/background-{i}.png'),
            )
        self.current_background = 0
        
    def change_background_right(self):
        self.current_background = (self.current_background + 1) % len(self.backgrounds)

    def change_background_left(self):
        self.current_background = (self.current_background - 1) % len(self.backgrounds)

    def get_image(self):
        return self.backgrounds[self.current_background]
    
class Screen():
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.state = ScreenState.MENU
    
    def blit(self, image, offset):
        self.screen.blit(image, offset)

class Frame(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/ground.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 0

class CoinScore():
    def __init__(self):
        self.offset = 10
        self.coin = pygame.image.load(f'assets/coins/coin-0-big.png').convert_alpha()
        self.lil_nums = [pygame.image.load(f'assets/numbers/{i}-little.png') for i in range(10)]
        self.score = 0
        self.images = [self.lil_nums[0]]
        self.rect = []
        self.rect.append(self.offset)
        self.rect.append(10)
    
    def increase(self):
        self.score += 1
        self.images.clear()
        for num in str(self.score):
            self.images.append(self.lil_nums[int(num)])
    
    def reset(self):
        self.score = 0
        self.images = [self.lil_nums[0]]
    
    def update(self, screen: Screen):
        screen.blit(self.coin, self.rect)
        cur_offset = self.coin.get_width()
        for image in self.images:
            screen.blit(image, [self.rect[0] + cur_offset, self.rect[1]])
            cur_offset += image.get_width()

class Score():
    def __init__(self):
        self.offset = -10
        self.lil_nums = [pygame.image.load(f'assets/numbers/{i}-little.png') for i in range(10)]
        self.big_nums = [pygame.image.load(f'assets/numbers/{i}-big.png') for i in range(10)]
        self.score = 0
        self.images = [self.lil_nums[0]]
        self.rect = []
        self.rect.append(settings.WINDOW_WIDTH - self.offset - self.images[0].get_width())
        self.rect.append(10)
    
    def increase(self):
        self.score += 1
        self.images.clear()
        for num in str(self.score):
            self.images.append(self.lil_nums[int(num)])
    
    def reset(self):
        self.score = 0
        self.images = [self.lil_nums[0]]
    
    def update(self, screen: Screen):
        cur_offset = 0
        for image in self.images[::-1]:
            cur_offset += image.get_width()
            screen.blit(image, [self.rect[0] - cur_offset, self.rect[1]])
    
    def show(self, screen: Screen):
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

def welcome_screen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screen.state = ScreenState.PLAY
            elif event.key == pygame.K_b:
                screen.state = ScreenState.BIRD_SETTINGS
            elif event.key == pygame.K_f:
                screen.state = ScreenState.BACKGROUND_SETTINGS
            elif event.key == pygame.K_s:
                screen.state = ScreenState.BARRIER_SETTINGS
    screen.blit(MENU_LAYOUT, (0, 0))
    pygame.time.Clock().tick(10)
    bird.fly()
    bird_group.draw(screen.screen)
    frame_group.draw(screen.screen)

def background_settings_screen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                screen.state = ScreenState.MENU
            elif event.key == pygame.K_RIGHT:
                background.change_background_right()
            elif event.key == pygame.K_LEFT:
                background.change_background_left()
    screen.blit(BACKGROUND_SETTINGS_LAYOUT, (0, 0))
    screen.blit(
        VERTICAL_FRAME, 
        (
            settings.BACKGROUND_SETTING_X + settings.BACKGROUND_SETTING_WIDTH * background.current_background, 
            settings.BACKGROUND_SETTING_Y
        )
    )

def bird_settings_screen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                screen.state = ScreenState.MENU
            elif event.key == pygame.K_RIGHT:
                bird.change_bird_right()
            elif event.key == pygame.K_LEFT:
                bird.change_bird_left()
            elif event.key == pygame.K_UP:
                bird.change_bird_up()
            elif event.key == pygame.K_DOWN:
                bird.change_bird_down()
    screen.blit(BIRD_SETTINGS_LAYOUT, (0, 0))
    screen.blit(
        HORIZONTAL_FRAME, 
        (
            settings.BIRD_SETTING_X + settings.BIRD_SETTING_WIDTH * (bird.current_bird_idx % 3), 
            settings.BIRD_SETTING_Y + settings.BIRD_SETTING_HEIGHT * (bird.current_bird_idx // 3)
        )
    )

def barrier_settings_screen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                screen.state = ScreenState.MENU
            elif event.key == pygame.K_RIGHT:
                barrier.change_barrier_right()
            elif event.key == pygame.K_LEFT:
                barrier.change_barrier_left()
    screen.blit(BARRIER_SETTINGS_LAYOUT, (0, 0))
    screen.blit(
        VERTICAL_FRAME, 
        (
            settings.BARRIER_SETTING_X + settings.BARRIER_SETTING_WIDTH * barrier.current_barrier_idx, 
            settings.BARRIER_SETTING_Y
        )
    )

def run_game():
    score.reset()
    score.update(screen)
    passed = False
    new_coin_time = True
    while True:
        pygame.time.Clock().tick(23)
        screen.blit(background.get_image(), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        if barrier_group.sprites()[0].rect[0] + barrier_group.sprites()[0].image.get_width() < 0:
            passed = False
            barrier_group.sprites()[0].set_position(settings.WINDOW_WIDTH, random.randint(-500, 0))
            new_coin = Coin()
            pos = barrier.get_center_position()
            pos = (
                pos[0] - new_coin.image.get_width() // 2,
                pos[1] - new_coin.image.get_height() // 2
            )
            new_coin.set_position(*pos)
            coin_group.add(new_coin)
            new_coin_time = True
        
        if (new_coin_time and
            barrier.rect[0] + barrier.image.get_width() - Coin.SIZE // 2 <= settings.WINDOW_WIDTH // 2):
            new_coin = Coin()
            pos = (settings.WINDOW_WIDTH, random.randint(100, 800))
            new_coin.set_position(*pos)
            coin_group.add(new_coin)
            new_coin_time = False

        bird_group.update()
        barrier_group.update()
        coin_group.update()

        bird_group.draw(screen.screen)
        frame_group.draw(screen.screen)
        barrier_group.draw(screen.screen)
        coin_group.draw(screen.screen)

        if pygame.sprite.groupcollide(bird_group, frame_group, False, False, pygame.sprite.collide_mask) or\
           pygame.sprite.groupcollide(bird_group, barrier_group, False, False, pygame.sprite.collide_mask):
            screen.state = ScreenState.GAME_OVER
            bird.reset()
            barrier.reset()
            time.sleep(1)
            break

        if pygame.sprite.groupcollide(bird_group, coin_group, False, True, pygame.sprite.collide_mask):            coin_score.increase()
        coin_score.update(screen)

        bird_pos = bird_group.sprites()[0].rect[0] + bird_group.sprites()[0].image.get_width() // 2
        barrier_pos =  (
            barrier_group.sprites()[0].rect[0] +
            barrier_group.sprites()[0].image.get_width() // 2
        )

        if not passed and bird_pos >= barrier_pos:
            passed = True
            score.increase()
        
        score.update(screen)
        pygame.display.update()

def game_over():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screen.state = ScreenState.PLAY
            elif event.key == pygame.K_b:
                screen.state = ScreenState.BIRD_SETTINGS
            elif event.key == pygame.K_f:
                screen.state = ScreenState.BACKGROUND_SETTINGS
            elif event.key == pygame.K_s:
                screen.state = ScreenState.BARRIER_SETTINGS
    screen.blit(GAME_OVER_LAYOUT, (0, 0))
    coin_group.empty()
    score.show(screen)
    pygame.time.Clock().tick(10)
    frame_group.draw(screen.screen)

if __name__ == "__main__":
    pygame.init()
    screen = Screen()
    score = Score()
    coin_score = CoinScore()
    
    bird = Bird()
    bird_group = pygame.sprite.Group()
    bird_group.add(bird)

    frame = Frame()
    frame_group = pygame.sprite.Group()
    frame_group.add(frame)

    barrier = Barrier()
    barrier_group = pygame.sprite.Group()
    barrier_group.add(barrier)

    coin_group = pygame.sprite.Group()

    background = Background()
    
    pygame.display.set_caption('Flappy Bird')

    while True:
        screen.blit(background.get_image(), (0, 0))
        coin_score.update(screen)
        if screen.state == ScreenState.MENU:
            welcome_screen()
        elif screen.state == ScreenState.BACKGROUND_SETTINGS:
            background_settings_screen()
        elif screen.state == ScreenState.BIRD_SETTINGS:
            bird_settings_screen()
        elif screen.state == ScreenState.BARRIER_SETTINGS:
            barrier_settings_screen()
        elif screen.state == ScreenState.PLAY:
            run_game()
        elif screen.state == ScreenState.GAME_OVER:
            game_over()

        pygame.display.update()

    
        
    