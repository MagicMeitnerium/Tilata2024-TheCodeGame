import pygame
from settings import *

class Key(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.type = 'key'
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.image.load('graphics/Images/keys.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (16,16))
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(-10,0)


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, info):
        super().__init__(groups)
        self.player = player
        self.type = 'chest'
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.image.load('graphics/Images/chest.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(-10,-15)
        self.display_surface = pygame.display.get_surface()
        self.font = main_font
        self.display_info = False
        self.info = info
        self.isRead = False

    def display_text(self, text, x, y):
        text_list = text.split('\n')
        y_update = y
        for text in text_list:
            text_surf = self.font.render(text, False, TEXT_COLOR)
            text_rect = text_surf.get_rect(center = (x , y_update))
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,10))
            self.display_surface.blit(text_surf, text_rect)
            y_update += 30
        
        #pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20 ,y_update * len(text_list) // 2),3)

    def show_info(self, info):
        key = pygame.key.get_pressed()
        if self.player.IsChestInFront():
            if key[pygame.K_e]:
                self.display_info = True

        else:
            self.display_info = False
            self.player.viewing_chest = False

        if self.display_info:
                self.player.viewing_chest = True
                draw_text("Continue --> 'C' ", font_UI, WHITE, SCREEN_WIDTH/2 -100 , SCREEN_HEIGHT//2 + 100)

                self.display_text(self.info, SCREEN_WIDTH//2 ,SCREEN_HEIGHT//2 -200)
                if key[pygame.K_c]:
                    self.display_info = False
                    if not self.isRead:
                        self.player.score += 50 
                    self.isRead = True

    def update(self):
        self.show_info(self.info)