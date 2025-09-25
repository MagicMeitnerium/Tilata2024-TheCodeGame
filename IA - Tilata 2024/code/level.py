import pygame, os, csv
from settings import *
from tiles import Tile
from player import Player
from door import *
from questions import *
from random import choice
from user_interface import UI
from enemy import Enemy
from objects import *
from playerattack import *


class Level():
    def __init__(self, main_map, deco_map, entity_map, spritesheet):
        self.tile_size = 16
        self.visible_sprites = ySortCameragroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.door_unlock_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()
        self.attacks = pygame.sprite.Group()

        self.spritesheet = spritesheet
        self.map_surface = pygame.display.get_surface()
        self.map_surface.set_colorkey((0,0,0))
        self.load_tiles(main_map, deco_map, entity_map)
        self.door_num = 0
        self.door = Door(question_list[self.door_num], self.player)
        self.ui = UI()
        self.game_end = False

    def load_tiles(self, main_map, deco_map, entity_map):
        full_map = [ (self.read_csv(entity_map)),(self.read_csv(main_map)), (self.read_csv(deco_map))]
        for map in full_map:
            for row_index, row in enumerate(map):
                for tile_index, tile in enumerate(row):
                    if tile != '-1':
                        x = tile_index * self.tile_size
                        y = row_index * self.tile_size
                        if map == full_map[0]:
                            if tile == "0":
                                Enemy((x,y), [self.visible_sprites, self.obstacle_sprites], self.obstacle_sprites, self.get_damage_to_player, self.add_exp)
                            if tile == "2":
                                Key((x,y), [self.visible_sprites, self.obstacle_sprites, self.chests])
                        else:
                            for a in range(32,50):
                                if tile == f"{a}":
                                    Tile(a, self.spritesheet, x , y , 'wall', [self.visible_sprites, self.obstacle_sprites])
                            for b in range(50,56):
                                if tile == f"{b}":
                                    Tile(b, self.spritesheet, x , y, 'door', [self.visible_sprites, self.obstacle_sprites, self.door_sprites])
                            for c in range(56,59):
                                if tile == f"{c}":
                                    Tile(c, self.spritesheet, x , y, 'final_door', [self.visible_sprites, self.obstacle_sprites, self.door_sprites])
                            for d in range(59,69):
                                if tile == f"{d}":
                                    Tile(d, self.spritesheet, x , y , 'deco', [self.visible_sprites, self.obstacle_sprites])

        self.player = Player((1990,2520), #1795,550  
                             self.obstacle_sprites,
                             self.door_sprites, self.chests,
                             [self.visible_sprites, self.obstacle_sprites],
                             self.open_door,
                             self.next_question,
                             self.create_attack)

        self.chest = Chest((1990,2480),
                               [self.visible_sprites,
                                self.obstacle_sprites,
                                self.chests],
                                self.player,
                                information[0])

    def load_map(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player.update()
        self.collision_logic()
        if not self.player.advanceDoor:
            self.door.display_question()

        self.ui.display(self.player)

        if self.player.dead:
            self.restart_menu()

        if self.player.end_door():
            self.game_end = True
        if self.game_end:
            key = pygame.key.get_pressed()
            self.map_surface.fill((0,0,0))
            draw_text('¡¡¡FELICIDADES, HAS ESCAPADO!!!', font_UI, (254, 249 ,129), 170, 250)
            draw_text("Juego terminado", main_font, (214, 74 ,64), 315, 400)
            draw_text("Presiona 'q' para salir", main_font, (214, 74 ,64), 300, 440)
            draw_text(f"Tu puntaje:  {self.player.score}", main_font, (254, 249 ,129), 300, 300)
            self.visible_sprites.empty()
            self.obstacle_sprites.empty()
            self.door_unlock_sprites.empty()
            self.door_sprites.empty()
            self.keys.empty()
            self.chests.empty()
            self.attacks.empty()
            if key[pygame.K_q]:
                pygame.quit()

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def open_door(self):
        self.opendoor = unlock_door(self.player, [self.visible_sprites, self.door_unlock_sprites])

    def collision_logic(self):
        for unlock_sprite in self.door_unlock_sprites:
            collision_sprites = pygame.sprite.spritecollide(unlock_sprite, self.door_sprites, False)
            if collision_sprites:
                for sprite in collision_sprites:
                    if sprite.type == 'door':
                        sprite.kill()
        for unlock_sprite in self.attacks:
            collision_sprites = pygame.sprite.spritecollide(unlock_sprite, self.obstacle_sprites, False)
            if collision_sprites:
                for sprite in collision_sprites:
                    if sprite.type == 'enemy':
                        if sprite.vulnerable:
                            sprite.health -= 50
                            sprite.vulnerable = False
                            sprite.hit_time = pygame.time.get_ticks()

    def next_question(self):
        if self.door_num < 9:
            self.door_num += 1
        self.door = Door(question_list[self.door_num], self.player)

    def create_attack(self):
        playerAttack(self.player, [self.visible_sprites, self.attacks])
        self.player.direction = pygame.math.Vector2(0,0)

    def add_exp(self):
        self.player.score += 50
        pygame.mixer.Sound.play(pygame.mixer.Sound("SFX/score.wav"), 0).set_volume(0.1)

    def get_damage_to_player(self, amount):
        if self.player.vulnerable:
            pygame.mixer.Sound.play(pygame.mixer.Sound("SFX/hit.wav"), 0).set_volume(0.05)
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def restart_menu(self):
        pause = True
        clock = pygame.time.Clock()
        display_surface = pygame.display.get_surface()
        pygame.mixer.music.pause()
        
        while pause:
            clock.tick(30)
            key = pygame.key.get_pressed()
            pygame.draw.rect(display_surface, UI_BG_COLOR, (20,20, SCREEN_WIDTH-40, SCREEN_HEIGHT-40))
            pygame.draw.rect(display_surface, UI_BORDER_COLOR, (20,20, SCREEN_WIDTH-40, SCREEN_HEIGHT-40),3)
            draw_text("HAS SIDO CAPTURADO", font1, HEALTH_COLOR, (SCREEN_WIDTH/2)-120,( SCREEN_HEIGHT/2)-100)
            draw_text("Press 'r' to restart", font_UI, WHITE, (SCREEN_WIDTH/2)-100,( SCREEN_HEIGHT/2))
            draw_text("Press 'q' to quit", font_UI, WHITE, (SCREEN_WIDTH/2)-100,( SCREEN_HEIGHT/2)+100)
            #Continue game
            if key[pygame.K_r]:
                pause = False
                self.visible_sprites.empty()
                self.obstacle_sprites.empty()
                self.door_unlock_sprites.empty()
                self.door_sprites.empty()
                self.keys.empty()
                self.chests.empty()
                self.attacks.empty()
                self.load_tiles('map/map1_ main.csv', 'map/map1_decoration.csv', 'map/map1_entities.csv')
                self.door_num = 0
                self.door = Door(question_list[self.door_num], self.player)
                pygame.mixer.music.unpause()

            if key[pygame.K_q]:
                quit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            pygame.display.update()

class ySortCameragroup(pygame.sprite.Group):
    def __init__(self):
        # General Setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('map/maps_ia.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        # getting offset
        self.offset.x = player.rect.x - self.half_width
        self.offset.y = player.rect.y - self.half_height

        self.display_surface.blit(self.floor_surf, (self.floor_rect.topleft - self.offset))

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'type') and sprite.type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
