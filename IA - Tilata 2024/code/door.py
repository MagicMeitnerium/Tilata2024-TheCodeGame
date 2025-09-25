import pygame

class Door():
    def __init__ (self, question, player):
        self.question = question
        self.player = player
        self.displayQuestion = False

    def display_question(self):
        key = pygame.key.get_pressed()
        if self.player.IsDoorInFront():
            if key[pygame.K_e]:
                self.displayQuestion = True
        else:
            self.displayQuestion = False

        if self.displayQuestion:
            self.player.interact_promt = False
            if self.question.draw():
                self.displayQuestion = False
                self.player.advanceDoor = True
                self.player.score += 100
                pygame.mixer.Sound.play(pygame.mixer.Sound("SFX/score.wav"), 0).set_volume(0.1)


class unlock_door(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        
        # Graphic
        full_path = f'graphics/images/transparent.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(80, 150))

        #placement
        self.rect = self.image.get_rect(center = player.rect.center + pygame.math.Vector2(0,16))
