import pygame 
from settings import *


class UI():
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = font_UI

        # bar setup
        self.healt_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.healt_bar_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT- 20)
        self.healt_energy_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH, BAR_HEIGHT)

    
    def showBar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def showScore(self, exp):
        text_surf = self.font.render('score: '+ str(int(exp)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright = (SCREEN_WIDTH-20, SCREEN_HEIGHT-20))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),3)
        self.display_surface.blit(text_surf, text_rect)

    def show_keys(self, player):
        text_surf = self.font.render('Llaves: '+str(player.key_count) + '/' + str(player.target_keys), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomleft = (20, SCREEN_HEIGHT-20))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),3)
        self.display_surface.blit(text_surf, text_rect)

    def interactions(self, player):
        if (player.doorCheck and player.interact_promt and not player.advanceDoor) or player.chestCheck and player.interact_promt and not player.viewing_chest:
            text_surf = self.font.render("Interactuar --> 'E' ", False, TEXT_COLOR)
            text_rect = text_surf.get_rect(center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT-200))
            self.display_surface.blit(text_surf, text_rect)
      
        if player.advanceDoor and player.doorCheck:
            text_surf = self.font.render("Abrir puerta --> 'Q' ", False, TEXT_COLOR)
            text_rect = text_surf.get_rect(center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT-200))
            self.display_surface.blit(text_surf, text_rect)
        
        if player.FinaldoorCheck and player.key_count < player.target_keys:
            text_surf = self.font.render("Recolecta todas las llaves", False, TEXT_COLOR)
            text_rect = text_surf.get_rect(center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT-200))
            self.display_surface.blit(text_surf, text_rect)

        if player.FinaldoorCheck and player.key_count == player.target_keys:
            text_surf = self.font.render("Abandona la prision --> 'e'", False, TEXT_COLOR)
            text_rect = text_surf.get_rect(center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT-200))
            self.display_surface.blit(text_surf, text_rect)
        

    def display(self, player):
        self.showBar(player.health, 100, self.healt_bar_rect, HEALTH_COLOR)
        self.showScore(player.score)
        self.interactions(player)
        self.show_keys(player)