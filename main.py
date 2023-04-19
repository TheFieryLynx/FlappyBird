import os
import pygame
import time

#local imports
import settings


if __name__ == "__main__":
    pygame.init()
    background_image = pygame.image.load('assets/background.png')
    background_group = pygame.sprite.Group()


    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption('Flappy Bird')


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        

        screen.blit(background_image, (0, 0))
        background_group.update()
        background_group.draw(screen)
        pygame.display.update()
        
    