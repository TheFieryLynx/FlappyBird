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
        self.fall -= 15

    def update(self):
        self.fly()
        self.fall += 2
        self.rect[1] += self.fall

def welcome_screen():
    pass

def run_game():
    while True:
        pygame.time.Clock().tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        screen.blit(background_image, (0, 0))
        
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

    
        
    