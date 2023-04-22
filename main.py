import os
import pygame
import time

from enum import Enum

#local imports
import settings
from states import ScreenState

MENU_LAYOUT = pygame.image.load('assets/layouts/menu-layout.png')
BACKGROUND_SETTINGS_LAYOUT = pygame.image.load('assets/layouts/background-settings-layout.png')
BIRD_SETTINGS_LAYOUT = pygame.image.load('assets/layouts/bird-settings-layout.png')
COLUMN_SETTINGS_LAYOUT = pygame.image.load('assets/layouts/barrier-settings-layout.png')
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
        self.fall = -25

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
        self.rect = self.image.get_rect()
        self.set_position(settings.WINDOW_WIDTH + 100, -254)

    def change_barrier_right(self):
        self.current_background = (self.current_background + 1) % len(self.barriers)

    def change_barrier_left(self):
        self.current_background = (self.current_background - 1) % len(self.barriers)

    def set_position(self, x, y):
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y

    def update(self):
        self.rect[0] -= 20

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
                screen.state = ScreenState.COLUMN_SETTINGS
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
    frame_group.draw(screen.screen)

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

def run_game():
    while True:
        pygame.time.Clock().tick(20)
        screen.blit(background.get_image(), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        if barrier_group.sprites()[0].rect[0] < -300:
            # barrier_group.remove(barrier_group.sprites()[0])
            # barrier_group.add(barrier)
            barrier.set_position(settings.WINDOW_WIDTH + 100, -254)

        bird_group.update()
        barrier_group.update()

        bird_group.draw(screen.screen)
        frame_group.draw(screen.screen)
        barrier_group.draw(screen.screen)
        pygame.display.update()

        if pygame.sprite.groupcollide(bird_group, frame_group, False, False, pygame.sprite.collide_mask):
            screen.state = ScreenState.GAME_OVER
            bird.reset()
            time.sleep(1)
            break

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
                screen.state = ScreenState.COLUMN_SETTINGS
    screen.blit(GAME_OVER_LAYOUT, (0, 0))
    pygame.time.Clock().tick(10)
    frame_group.draw(screen.screen)

if __name__ == "__main__":
    pygame.init()
    screen = Screen()
    
    bird = Bird()
    bird_group = pygame.sprite.Group()
    bird_group.add(bird)

    frame = Frame()
    frame_group = pygame.sprite.Group()
    frame_group.add(frame)

    barrier = Barrier()
    barrier_group = pygame.sprite.Group()
    barrier_group.add(barrier)

    background = Background()
    
    pygame.display.set_caption('Flappy Bird')

    while True:
        screen.blit(background.get_image(), (0, 0))
        if screen.state == ScreenState.MENU:
            welcome_screen()
        elif screen.state == ScreenState.BACKGROUND_SETTINGS:
            background_settings_screen()
        elif screen.state == ScreenState.BIRD_SETTINGS:
            bird_settings_screen()
        elif screen.state == ScreenState.PLAY:
            run_game()
        elif screen.state == ScreenState.GAME_OVER:
            game_over()
          

        pygame.display.update()

    
        
    