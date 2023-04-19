import os
import pygame
import time

#local imports
import settings

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
        self.set_yellow_bird()
        self.current_image = 0
        self.image = self.current_bird[self.current_image]
        self.set_position()
        
    def set_position(self):
        self.rect = self.image.get_rect()
        self.rect[0] = 70
        self.rect[1] = 276

    def set_yellow_bird(self):
        self.current_bird = self.birds['yellow']
    
    def set_beige_bird(self):
        self.current_bird = self.birds['beige']

    def fly(self):
        self.current_image = (self.current_image + 1) % 2
        self.image = self.current_bird[self.current_image]

def welcome_screen():
    pass

def run_game():
    while True:
        pygame.time.Clock().tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.blit(background_image, (0, 0))
        
        bird.fly()

        bird_group.update()
        bird_group.draw(screen)
        
        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    background_image = pygame.image.load('assets/background-0.png')
    
    bird = Bird()
    bird_group = pygame.sprite.Group()
    bird_group.add(bird)
    
    pygame.display.set_caption('Flappy Bird')

    welcome_screen()
    run_game()

    
        
    