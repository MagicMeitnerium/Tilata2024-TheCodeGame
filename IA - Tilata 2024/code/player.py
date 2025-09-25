import pygame
import spritesheet
from questions import *
from entity import Entity

class Player(Entity):
    def __init__(self, pos0, obstacle_sprites, door_group, chest_group ,groups, open_door, next_question, create_attack):
        super().__init__(groups)
        self.type = 'player'
        self.speed = 2
        self.health = 100
        self.score = 0
        self.key_count = 0
        self.target_keys = 8
        self.master_key = False
        self.interact_promt = False
        self.dead = False

        self.obstacle_sprites = obstacle_sprites
        self.action = 0
        self.animationList = self.create_animation_list()
        self.image = self.animationList[self.action][self.frame_index]
        self.rect = self.image.get_rect(center = pos0)
        self.hitbox = self.rect.inflate(0, -20)

        # Animations
        self.update_time = pygame.time.get_ticks()
        self.vulnerable = True
        self.hurt_time = None
        self.invincibility_duration = 300

        self.attacking = False
        self.attack_coooldown = 400
        self.attack_time = None

        self.lastKeyPressed = 4
        self.next = False
        self.doorCheck = False 
        self.advanceDoor = False

        self.chestCheck = False
        self.viewing_chest = False

        self.open_door = open_door
        self.next_question = next_question
        self.door_group = door_group
        self.create_attack = create_attack
        self.chest_group = chest_group

        # import sound
        #self.death_sound = pygame.mixer.Sound("SFX/gameOverpiririri.mp3")

    def input(self):
        key = pygame.key.get_pressed()
        # direction input
        if not self.attacking:
            # vertical input
            if key[pygame.K_UP]:
                self.direction.y = -1
                self.action = 2
                self.lastKeyPressed = 2

            elif key[pygame.K_DOWN]:
                self.direction.y = 1
                self.action = 4
                self.lastKeyPressed = 4 
            else:
                self.direction.y = 0

            # horizontal input
            if key[pygame.K_RIGHT]:
                self.direction.x = 1
                self.action = 1
                self.lastKeyPressed = 1
            elif key[pygame.K_LEFT]:
                self.direction.x = -1
                self.action = 3
                self.lastKeyPressed = 3
            else:
                self.direction.x = 0
        
            if self.direction.x == 0 and self.direction.y == 0:
                self.action = 0
                self.frame_index = self.lastKeyPressed - 1

            if key[pygame.K_q] and self.advanceDoor and self.IsDoorInFront():
                self.advanceDoor = False
                self.open_door()
                self.next_question()

            if key[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.action = 0
                self.frame_index = self.lastKeyPressed - 1
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                pygame.mixer.Sound.play(pygame.mixer.Sound("SFX/sword.wav")).set_volume(0.05)
                          
    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
        #pygame.draw.rect(display, (255,255,255), self.rect, 1)

    def update(self):
        #self.door_interaction()
        self.health_recovery()
        self.input()
        self.move(self.speed)
        self.updateAnimation()
        self.IsDoorInFront()
        self.IsChestInFront()
        self.cooldowns()
        self.key_update()
        self.end_door()
        self.death()
        
    def create_animation_list(self):
        animsTypes = ['static', 'run_right', 'run_up', 'run_left', 'run_down']
        animation_list = []
        for anims in animsTypes:
            playerSpritesheetImage = pygame.image.load(f'graphics/player_anims/{anims}.png').convert_alpha()
            playerStatic = spritesheet.SpriteSheet(playerSpritesheetImage)
            tempList = []
            for x in range(6):
                tempList.append(playerStatic.get_image(x, 16, 24, 1, (0,0,0)))
            animation_list.append(tempList)
        return animation_list

    def updateAnimation(self):
        animationCooldown = 100
        currentTime = pygame.time.get_ticks()
        self.image = self.animationList[self.action][self.frame_index]


        if currentTime - self.update_time >= animationCooldown:
            if not self.action == 0:
                self.frame_index += 1

            self.update_time = currentTime

            
        if self.frame_index >= len(self.animationList):
              self.frame_index = 0

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)

        else:
            self.image.set_alpha(255)
    
    def IsDoorInFront(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.door_group, False)
        if collision_sprites:
            for target_sprite in collision_sprites:
                
                if target_sprite.type == 'door':
                    self.doorCheck = True
                    self.interact_promt = True
                else:
                    self.doorCheck = False
        else:
            self.doorCheck = False

        return self.doorCheck
    
    def IsChestInFront(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.chest_group, False)
        if collision_sprites:
            for target_sprite in collision_sprites:
                if target_sprite.type == 'chest':
                    self.chestCheck = True
                    self.interact_promt = True
                else:
                    self.chestCheck = False
        else:
            self.chestCheck = False

        return self.chestCheck
    
    def key_update(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.obstacle_sprites, False)
        if collision_sprites:
            for target_sprite in collision_sprites:
                if target_sprite.type == 'key':
                    pygame.mixer.Sound.play(pygame.mixer.Sound("SFX/score.wav"), 0).set_volume(0.1)
                    target_sprite.kill()
                    self.key_count += 1
                    if self.health < 100:
                        self.health += 20
                    self.score += 20

        if self.key_count >= 8:
            self.master_key = True

    def end_door(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.door_group, False)
        key = pygame.key.get_pressed()
        if collision_sprites:
            for target_sprite in collision_sprites:
                if target_sprite.type == 'final_door':
                    self.FinaldoorCheck = True
                else:
                    self.FinaldoorCheck = False
        else:
            self.FinaldoorCheck = False

        if self.FinaldoorCheck and self.key_count == self.target_keys:
            if key[pygame.K_e]:
                return True
             
    def health_recovery(self):
        if self.health < 100:
            self.health += 0.01 
        else:
            self.health = 100

        if self.score <= 0:
            self.score = 0 

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_coooldown:
                self.attacking = False
                
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.vulnerable = True

    def death(self):
        if self.health <= 0:
            self.dead = True
            pygame.mixer.Sound.play(pygame.mixer.Sound("SFX/audio_game_over.mp3"), 0).set_volume(0.05)
