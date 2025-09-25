import pygame
from entity import Entity
import spritesheet

class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, get_damage_to_player, add_score):  
        super().__init__(groups)

        self.type = 'enemy'
        self.status = 0  # 0 = idle, 1 = move, 2 = attack
        self.speed = 2
        self.health = 100
        self.attack_damage = 18
        self.animation_list = self.create_animation_list()
        self.image = self.animation_list[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(-5,-10)
        #self.attack_retreat_distance = 20

        self.obstacle_sprites = obstacle_sprites

        self.can_attack = True
        self.attack_coooldown = 400
        self.attack_time = None

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 500

        self.damage_player = get_damage_to_player
        self.add_score = add_score
        #self.add_exp = add_exp

        self.attack_radius = 16
        self.notice_radius = 200

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return(distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 2:
                self.frame_index = 0
            self.status = 2
        elif distance <= self.notice_radius:
            self.status = 1
        else:
            self.status = 0

    def actions(self, player):
        if self.status == 2:
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage)
            
        if self.status == 1:
            self.direction = self.get_player_distance_direction(player)[1]
        else: 
            self.direction = pygame.math.Vector2()

    def create_animation_list(self):
        animsTypes = ['idle', 'move', 'attack']
        animation_list = []

        for anims in animsTypes:
            playerSpritesheetImage = pygame.image.load(f'graphics/enemy_anims/{anims}.png').convert_alpha()
            playerStatic = spritesheet.SpriteSheet(playerSpritesheetImage)
            tempList = []
            if anims == 'attack':
                length = 1
            else:
                length = 4
            for x in range(length):
                tempList.append(playerStatic.get_image(x, 16, 24, 1, (0,0,0)))
            animation_list.append(tempList)
        return animation_list   

    def animate(self):
        animation = self.animation_list[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 2:
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)

        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_coooldown:
                self.can_attack = True

        if not self.vulnerable:
             if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def die(self):
        if self.health <= 0:
            self.kill()
            self.add_score()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= - 1 #self.attack_retreat_distance

    def enemy_update(self, player):
        self.hit_reaction()
        self.die()
        self.get_status(player)
        self.animate()
        self.move(self.speed)
        self.cooldowns()
        self.actions(player)
        #self.energy_recovery()