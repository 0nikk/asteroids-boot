import pygame
from constants import *

class BackgroundLayer:
    def __init__(self, image_path, scale=1.0, speed=0.0):
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, 
                (int(SCREEN_WIDTH * scale), int(SCREEN_HEIGHT * scale)))
        except:
            print(f"Could not load background image: {image_path}")
            self.image = None
        
        self.speed = speed
        self.offset = 0
        self.width = SCREEN_WIDTH * scale

    def update(self, dt):
        if self.image:
            self.offset = (self.offset + self.speed * dt) % self.width

    def draw(self, screen):
        if self.image:
            # Draw the background twice to create seamless scrolling
            screen.blit(self.image, (-self.offset, 0))
            screen.blit(self.image, (self.width - self.offset, 0)) 