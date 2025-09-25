import pygame, csv, os
from settings import *

pygame.init()

class Tile(pygame.sprite.Sprite):
    def __init__(self, frame, spritesheet, x, y, type, groups):
        super().__init__(groups)
        self.type = type
        self.image = spritesheet.get_image(frame, 16, 16,1,(0,0,0)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.rect = self.image.get_rect(topleft= (x,y))
        self.hitbox = self.rect.inflate(0,0) 