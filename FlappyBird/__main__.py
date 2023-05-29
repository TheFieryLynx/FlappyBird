from __init__ import ScreenState
from __init__ import Bird
from __init__ import Barrier
from __init__ import Coin
from __init__ import Background
from __init__ import Screen
from __init__ import Frame
from __init__ import CoinScore
from __init__ import Score


import random
import time
import pygame
import os
import sys

import settings


def welcome_screen():
    """Display game start screen and listen for keydown events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
    """Display background settings screen and listen for keydown events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
            settings.BACKGROUND_SETTING_X + settings.BACKGROUND_SETTING_WIDTH
            * background.current_background,
            settings.BACKGROUND_SETTING_Y
        )
    )


def bird_settings_screen():
    """Display bird settings screen and listen for keydown events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
            settings.BIRD_SETTING_X + settings.BIRD_SETTING_WIDTH
            * (bird.current_bird_idx % 3),
            settings.BIRD_SETTING_Y + settings.BIRD_SETTING_HEIGHT
            * (bird.current_bird_idx // 3)
        )
    )


def barrier_settings_screen():
    """Display barrier settings screen and listen for keydown events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
            settings.BARRIER_SETTING_X + settings.BARRIER_SETTING_WIDTH
            * barrier.current_barrier_idx,
            settings.BARRIER_SETTING_Y
        )
    )


def run_game():
    """Start the game and update every game component on clock tick or keydown event."""
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
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        if barrier_group.sprites()[0].rect[0] + barrier_group.sprites()[0].image.get_width() < 0:
            passed = False
            barrier_group.sprites()[0].set_position(
                settings.WINDOW_WIDTH, random.randint(-500, 0))
            new_coin = Coin()
            pos = barrier.get_center_position()
            pos = (
                pos[0] - new_coin.image.get_width() // 2,
                pos[1] - new_coin.image.get_height() // 2
            )
            new_coin.set_position(*pos)
            coin_group.add(new_coin)
            new_coin_time = True

        if (new_coin_time
            and barrier.rect[0] + barrier.image.get_width()
                - Coin.SIZE // 2 <= settings.WINDOW_WIDTH // 2):
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

        if pygame.sprite.groupcollide(bird_group, coin_group, False, True, pygame.sprite.collide_mask):
            coin_score.increase()
        coin_score.update(screen)

        bird_pos = bird_group.sprites(
        )[0].rect[0] + bird_group.sprites()[0].image.get_width() // 2
        barrier_pos = (
            barrier_group.sprites()[0].rect[0]
            + barrier_group.sprites()[0].image.get_width() // 2
        )

        if not passed and bird_pos >= barrier_pos:
            passed = True
            score.increase()

        score.update(screen)
        pygame.display.update()


def game_over():
    """Display game over screen and listen for keydown events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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


path = os.path.join(os.path.dirname(__file__), f'assets')
MENU_LAYOUT = pygame.image.load(path + '/layouts/menu-layout.png')
BACKGROUND_SETTINGS_LAYOUT = pygame.image.load(path + '/layouts/background-settings-layout.png')
BIRD_SETTINGS_LAYOUT = pygame.image.load(path + '/layouts/bird-settings-layout.png')
BARRIER_SETTINGS_LAYOUT = pygame.image.load(path + '/layouts/barrier-settings-layout.png')
GAME_OVER_LAYOUT = pygame.image.load(path + '/layouts/game-over-layout.png')
VERTICAL_FRAME = pygame.image.load(path + '/vertical-frame.png')
HORIZONTAL_FRAME = pygame.image.load(path + '/horizontal-frame.png')

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
