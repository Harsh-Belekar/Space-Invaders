import pygame

from Assets import images, sounds, RED, GREEN

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DT = 0.01

# Spaceship Class
class Spaceship_Class(pygame.sprite.Sprite):
    
    def __init__(self, screen, groups, laser_sprites, bullet_sprites, explosion_sprites):
        super().__init__(groups)
        self.screen = screen
        self.image = images["spaceship_img"]
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100))
        self.direction = pygame.Vector2()
        self.speed = 6
        self.health_start = 10
        self.health_remaining = 10
        
        # cooldown 
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        
        # Images
        self.laser_img = images["laser_img"]
        self.bullet_img = images["bullet_img"]
        self.explosion_frames = images["explosion_frames"]
        
        # Sound
        self.laser_sound = sounds["laser"]
        self.bullet_sound = sounds["bullet"]
        self.meteor_explosion_sound = sounds["meteor_explosion_sound"]
        
        # Sprites
        self.laser_sprites = laser_sprites
        self.bullet_sprites = bullet_sprites
        self.explosion_sprites = explosion_sprites
    
    def health_bar(self):
        pygame.draw.rect(self.screen, RED, (self.rect.x + 5,(self.rect.y + 85),
                                        self.rect.width - 5, 15))
        
        if self.health_remaining > 0: 
            pygame.draw.rect(self.screen, GREEN, (self.rect.x + 5,(self.rect.y + 85), 
                            int((self.rect.width - 5) * (self.health_remaining / self.health_start)), 15))
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    
    def update(self, is_over):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])  
        self.direction = (self.direction.normalize() if self.direction else self.direction)
        
        # Move Spaceship
        if is_over == 0:
            self.rect.center += self.direction * self.speed
        else:
            self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100))
        
        # Screen boundaries
        if self.rect.left < 5:
            self.rect.left = 5
        if self.rect.right > WINDOW_WIDTH - 5:
            self.rect.right = WINDOW_WIDTH - 5
        if self.rect.top < 5:
            self.rect.top = 5
        if self.rect.bottom > WINDOW_HEIGHT - 30:
            self.rect.bottom = WINDOW_HEIGHT - 30
        
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot and is_over == 0: 
            if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) :
                img = self.laser_img
                sprite = self.laser_sprites
                shoot_sound = self.laser_sound
            else:
                img = self.bullet_img
                sprite = self.bullet_sprites
                shoot_sound = self.bullet_sound
            
            Laser_Class(img, self.rect.midtop, sprite) 
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            shoot_sound.play()
        
        if self.health_remaining <= 0:
            AnimatedExplosion(self.explosion_frames, self.rect.center, self.meteor_explosion_sound,15, self.explosion_sprites)
            self.kill()
        
        self.laser_timer()
        
        self.health_bar()


# Laser Class
class Laser_Class(pygame.sprite.Sprite):
    
    def __init__(self, laser_img, pos, groups):
        super().__init__(groups)
        self.image = laser_img
        self.rect = self.image.get_frect(midbottom = pos)
        
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()


# Explosion Class
class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, sound, time, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        self.explosion_time = time
        sound.play()
    
    def update(self):
        self.frame_index += self.explosion_time * DT
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

