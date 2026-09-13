import pygame 
from random import randint, randint, uniform

WINDOW_HEIGHT = 600
DT = 0.01

# Alien Class
class Alien_Class(pygame.sprite.Sprite):
    
    def __init__(self, aliens_img, pos, groups):
        super().__init__(groups)
        self.image = aliens_img[randint(0,4)]
        self.rect = self.image.get_frect(center = pos)
        self.move_direction = 1
        self.move_counter = 0
    
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

# Alien Bullets Class
class Alien_Bullets(pygame.sprite.Sprite):
    
    def __init__(self, alien_bullet_img, pos, groups):
        super().__init__(groups)
        self.image = alien_bullet_img
        self.rect = self.image.get_frect(midbottom = pos)
        
    def update(self):
        self.rect.y += 2
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

# Meteor Class
class Meteor_Class(pygame.sprite.Sprite):
    def __init__(self, meteor_img, pos, groups):
        super().__init__(groups)
        self.original_surf = meteor_img
        self.image = meteor_img
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(400,500)
        self.rotation_speed = randint(40,80)
        self.rotation = 0
        
    def update(self):
        self.rect.center += self.direction * self.speed * DT
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * DT
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)
