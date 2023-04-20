import os
import pygame
import time

from enum import Enum

#local imports
import settings
from states import ScreenState

screen_state = ScreenState.MENU

MENU_IMAGE = pygame.image.load('assets/menu.png')
SETTINGS_IMAGE = pygame.image.load('assets/settings.png')
BACKGROUND_FRAME = pygame.image.load('assets/background-frame.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.birds = {
            'beige' : [
                pygame.image.load('assets/bird-beige-1.png').convert_alpha(),
                pygame.image.load('assets/bird-beige-2.png').convert_alpha()
            ],
            'yellow' : [
                pygame.image.load('assets/bird-yellow-1.png').convert_alpha(),
                pygame.image.load('assets/bird-yellow-2.png').convert_alpha()
            ]
        }
        self.fall = 0
        self.set_yellow_bird()
        self.current_image = 0
        self.image = self.current_bird[self.current_image]
        self.set_position()
        
    def set_position(self):
        self.rect = self.image.get_rect()
        self.rect[0] = settings.BIRD_INIT_X
        self.rect[1] = settings.BIRD_INIT_Y

    def set_yellow_bird(self):
        self.current_bird = self.birds['yellow']
    
    def set_beige_bird(self):
        self.current_bird = self.birds['beige']

    def fly(self):
        self.current_image = (self.current_image + 1) % 2
        self.image = self.current_bird[self.current_image]
    
    def jump(self):
        self.fall -= 20

    def update(self):
        self.fly()
        self.fall += 2
        self.rect[1] += self.fall

class Background():
    def __init__(self):
        self.backgrounds = [
            pygame.image.load('assets/background-0.png'),
            pygame.image.load('assets/background-1.png'),
            pygame.image.load('assets/background-2.png')
        ]
        self.current_background = 0
        
    def change_background(self):
        self.current_background = (self.current_background + 1) % 3

    def get_image(self):
        return self.backgrounds[self.current_background]
    
class Screen():
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.state = ScreenState.MENU
    
    def blit(self, image, offset):
        self.screen.blit(image, offset)

def welcome_screen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screen.state = ScreenState.PLAY
            if event.key == pygame.K_s:
                screen.state = ScreenState.SETTINGS
    screen.blit(MENU_IMAGE, (0, 0))
    pygame.time.Clock().tick(10)
    bird.fly()
    bird_group.draw(screen.screen)

def settings_screen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                screen.state = ScreenState.MENU
            if event.key == pygame.K_f:
                background.change_background()
    screen.blit(SETTINGS_IMAGE, (0, 0))
    screen.blit(
        BACKGROUND_FRAME, 
        (
            settings.BACKGROUND_SETTING_X + settings.BACKGROUND_SETTING_WIDTH * background.current_background, 
            settings.BACKGROUND_SETTING_Y
        )
    )

def run_game():
    while True:
        pygame.time.Clock().tick(20)
        screen.blit(background.get_image(), (0, 0))

        if screen.state == ScreenState.MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        screen.state = ScreenState.PLAY
                    if event.key == pygame.K_s:
                        screen.state = ScreenState.SETTINGS
            screen.blit(MENU_IMAGE, (0, 0))

        elif screen.state == ScreenState.SETTINGS:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        screen.state = ScreenState.MENU
                    if event.key == pygame.K_f:
                        background_state = (background_state + 1) % 3

            screen.blit(SETTINGS_IMAGE, (0, 0))
            screen.blit(
                BACKGROUND_FRAME, 
                (
                    settings.BACKGROUND_SETTING_X + settings.BACKGROUND_SETTING_WIDTH * background_state, 
                    settings.BACKGROUND_SETTING_Y
                )
            )
        
        elif screen.state == ScreenState.PLAY:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()

        bird_group.update()
        bird_group.draw(screen.screen)
        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    screen = Screen()
    
    bird = Bird()
    bird_group = pygame.sprite.Group()
    bird_group.add(bird)

    background = Background()
    
    pygame.display.set_caption('Flappy Bird')

    while True:
        screen.blit(background.get_image(), (0, 0))

        if screen.state == ScreenState.MENU:
            welcome_screen()
        elif screen.state == ScreenState.SETTINGS:
            settings_screen()
        elif screen.state == ScreenState.PLAY:
            run_game()

        pygame.display.update()

    
        
    