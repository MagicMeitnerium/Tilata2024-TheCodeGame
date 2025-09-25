import pygame
from settings import *
import spritesheet

class playerAttack(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.type = 'attack'
        self.direction = player.action
        self.lastKeyPressed = player.lastKeyPressed

        self.screen = pygame.display.get_surface()

        self.frame_index = 0
        self.animation_speed = 1


        # sprites
        self.spritesheet_image = pygame.image.load(f'graphics/slash/slash_spritesheet.png').convert_alpha()
        self.spritesheet = spritesheet.SpriteSheet(self.spritesheet_image)
        self.anim_list = []
        for x in range(6):
            self.anim_list.append(self.spritesheet.get_image(x, 16, 24, 1, (0,0,0)))

        self.image = self.anim_list[self.frame_index]

        #placement
        if self.direction == 0:
            if self.lastKeyPressed == 1:
                self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-5, 0))
            if self.lastKeyPressed == 3:
                self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(5, 10))
            if self.lastKeyPressed == 4:
                self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0,-10))
            if self.lastKeyPressed == 2:
                self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,15))


        if self.direction == 1:
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-5, 0))
        if self.direction == 3:
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(5, 10))
        if self.direction == 4:
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0,-10))
        if self.direction == 2:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,15))

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.anim_list):
            self.kill()
        else:
            self.image = self.anim_list[int(self.frame_index)]

    def update(self):        
        self.animate()

         