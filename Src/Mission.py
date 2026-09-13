import pygame 
import button
import sys
from os.path import join
from random import randint, choice

from Assets import images, sounds , font18, WHITE
from Spaceship import Spaceship_Class, AnimatedExplosion
import Alien


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

SCORE_PATH = join("Assets","Scores-Files")

class Mission_Class:
    
    def __init__(self):
        # Initialize Pygame and set up display
        pygame.init()
        self.mission_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space Invaders - Mission Start")
        self.clock = pygame.time.Clock()
        
        self.rows = 3
        self.cols = 6
        self.alien_cooldown = 1000 
        self.last_alien_shoot = pygame.time.get_ticks()
        self.is_over = 0 # 0 is no gameover, 1 is Player Win, -1 is Player Lost
        self.current_time = 0
        self.meteor_count = 0
        self.lowest_time = 0
        self.highest_meteor_count = 0
        
        # Load Assets
        self.bg = images["bg"]
        self.restart_img = images["restart"]
        self.exit_img = images["exit"]
        self.win_banner = images["win"]
        self.lose_banner = images["lose"]
        
        # Load Images
        self.meteor_img = images["meteor_img"]
        self.aliens_img = images["aliens_img"]
        self.alien_bullet_img = images["alien_bullet_img"]
        self.explosion_frames = images["explosion_frames"]
        self.alien_explosion_frames = images["alien_explosion_frames"]
        self.spaceship_damage_frames = images['spaceship_damage_frames']
        
        # Load Sound 
        self.click = sounds["click"]
        self.meteor_explosion_sound = sounds["meteor_explosion_sound"]
        self.explosion_sound = sounds["explosion_sound"]
        self.damage_sound = sounds["damage_sound"]
        
        # Buttons
        self.restart_button=button.Button(295,265,self.restart_img,1)
        self.exit_button=button.Button(305,355,self.exit_img,1)
        
        self.spaceship_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self.meteor_sprites = pygame.sprite.Group()
        self.alien_sprites = pygame.sprite.Group()
        self.alien_bullets_sprites = pygame.sprite.Group()
        self.explosion_sprites = pygame.sprite.Group()
        
        
        # custom events -> meteor event
        self.meteor_event = pygame.event.custom_type()
        pygame.time.set_timer(self.meteor_event, 1000)
    
    def run_game(self):
        # Game State Flags
        self.running = True
        self.restart = False
        
        # Create Player
        self.spaceship = Spaceship_Class(self.mission_screen, self.spaceship_sprites,
                                                    self.laser_sprites, self.bullet_sprites,
                                                    self.explosion_sprites)
        
        # Create Alien
        self.create_alien()
        
        # Read Score
        self.read_score()
        
        self.start_ticks = pygame.time.get_ticks()
        
        # -------- Game Loop --------
        while self.running:
            self.clock.tick(FPS)
            
            # Draw Background
            self.mission_screen.blit(self.bg, (0, 0))
            
            self.score_board()
            
            # -------- Handle Quit Event --------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == self.meteor_event and self.is_over == 0:
                    if randint(1,10) > 5 :
                        x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
                        Alien.Meteor_Class(self.meteor_img, (x, y), self.meteor_sprites)
            
            self.time_now = pygame.time.get_ticks()
            if (self.time_now - self.last_alien_shoot > self.alien_cooldown) and len(self.alien_bullets_sprites) < 5 and len(self.alien_sprites) > 0 and self.spaceship.health_remaining > 0:
                attacking_alien = choice(self.alien_sprites.sprites())
                Alien.Alien_Bullets(self.alien_bullet_img,(attacking_alien.rect.centerx,
                                            attacking_alien.rect.bottom),self.alien_bullets_sprites)
                self.last_alien_shoot = self.time_now
                
            if len(self.alien_sprites) == 0:
                self.is_over = 1
                self.game_over("win")
                if self.current_time < self.lowest_time or self.lowest_time == 0: 
                    self.lowest_time = self.current_time
                    self.update_score("lowest_time.txt",self.lowest_time)
            
            if self.spaceship.health_remaining <= 0:
                self.is_over = -1
                self.game_over("lose")
            
            if self.meteor_count > self.highest_meteor_count: 
                self.highest_meteor_count = self.meteor_count
                self.update_score("highest_meteor.txt",self.highest_meteor_count)
            
            if self.is_over == 0:
                self.elapsed_milliseconds = pygame.time.get_ticks() - self.start_ticks
                self.current_time = self.elapsed_milliseconds // 1000
                
                self.alien_sprites.update()
                self.alien_sprites.draw(self.mission_screen)
                self.meteor_count = self.collisions(self.meteor_count)
            
            # Update Sprite Group
            self.spaceship_sprites.update(self.is_over)
            self.bullet_sprites.update()
            self.laser_sprites.update()
            self.meteor_sprites.update()
            self.alien_bullets_sprites.update()
            self.explosion_sprites.update()
            
            # Draw Sprite Group
            self.spaceship_sprites.draw(self.mission_screen)
            self.bullet_sprites.draw(self.mission_screen)
            self.laser_sprites.draw(self.mission_screen)
            self.meteor_sprites.draw(self.mission_screen)
            self.alien_bullets_sprites.draw(self.mission_screen)
            self.explosion_sprites.draw(self.mission_screen)

            # Update display
            pygame.display.update()

        if self.restart:
            self.run_game()

    def create_alien(self):
        for row in range(self.rows):
            for item in range(self.cols):
                Alien.Alien_Class(self.aliens_img,((150 + item * 100), (80 + row * 70)),self.alien_sprites)

    def collisions(self, meteor_count):
    
        for laser in self.laser_sprites:
            laser_collided_sprites = pygame.sprite.spritecollide(laser, self.meteor_sprites, True, pygame.sprite.collide_mask)
            if laser_collided_sprites:
                laser.kill()
                meteor_count += 1
                AnimatedExplosion(self.explosion_frames, laser.rect.midtop, self.meteor_explosion_sound,15, self.explosion_sprites)
                
        for bullet in self.bullet_sprites:
            bullet_collided_sprites = pygame.sprite.spritecollide(bullet, self.alien_sprites, True, pygame.sprite.collide_mask)
            if bullet_collided_sprites:
                bullet.kill()
                AnimatedExplosion(self.alien_explosion_frames, bullet.rect.midtop,self.explosion_sound,15, self.explosion_sprites)
        
        for alien_bullet in self.alien_bullets_sprites:
            alien_bullet_collided_sprites = pygame.sprite.spritecollide(alien_bullet, self.spaceship_sprites, False, pygame.sprite.collide_mask)
            if alien_bullet_collided_sprites:
                self.damage_sound.play()
                AnimatedExplosion(self.spaceship_damage_frames, alien_bullet.rect.midbottom, self.meteor_explosion_sound,20, self.explosion_sprites)
                alien_bullet.kill()
                self.spaceship.health_remaining -= 1

        for meteor in self.meteor_sprites:
            meteor_collided_sprites = pygame.sprite.spritecollide(meteor, self.spaceship_sprites, False, pygame.sprite.collide_mask)
            if meteor_collided_sprites:
                self.damage_sound.play()
                meteor.kill()
                AnimatedExplosion(self.explosion_frames, meteor.rect.midbottom, self.meteor_explosion_sound,15, self.explosion_sprites)
                self.spaceship.health_remaining -= 2
        
        return meteor_count
    
    def draw_text(self, text, font, text_col, pos):
        img = font.render(text, True, text_col)
        self.mission_screen.blit(img, pos)

    def read_score(self):
        try :
            with open(join(SCORE_PATH,'lowest_time.txt'),"r") as file: #Open File in Read Mode
                self.lowest_time = int(file.read()) 
        except:
            with open(join(SCORE_PATH,'lowest_time.txt'),"w") as file: #Open File in Wirte Mode
                file.write(f"{0}") 
        
        try :
            with open(join(SCORE_PATH, 'highest_meteor.txt'),"r") as file: #Open File in Read Mode
                self.highest_meteor_count = int(file.read()) 
        except:
            with open(join(SCORE_PATH,'highest_meteor.txt'),"w") as file: #Open File in Wirte Mode
                file.write(f"{0}")

    def update_score(self, file: str , update):
        with open(join(SCORE_PATH, file),"w") as file:
            file.write(f"{update}") 

    def score_board(self):
        self.draw_text(f"Current Time: {self.current_time}",font18,WHITE,(10, 10))
        self.draw_text(f"Meteor: {self.meteor_count}",font18,WHITE,(10, 30))
        
        self.draw_text(f"Lowest Time: {self.lowest_time}",font18,WHITE,(WINDOW_WIDTH - 180, 10))
        self.draw_text(f"Hightest Meteor:  {self.highest_meteor_count}",font18,WHITE,(WINDOW_WIDTH - 180, 30))

    def game_over(self, res):
        self.result = self.win_banner if res == "win" else self.lose_banner
        
        self.mission_screen.blit(self.result,(233,100)) # Show the banner on screen
        
        # Show buttons for restart, exit, etc.
        if self.restart_button.draw(self.mission_screen):
            self.restart_game()
        
        if self.exit_button.draw(self.mission_screen) :
            self.running=False
            pygame.quit()
            sys.exit()
    
    def restart_game(self):
        
        # Reset counters
        self.is_over = 0
        self.start_ticks = pygame.time.get_ticks()
        self.meteor_count = 0
        
        # Reset Sprites 
        self.spaceship_sprites.empty()
        self.bullet_sprites.empty()
        self.laser_sprites.empty()
        self.meteor_sprites.empty()
        self.alien_sprites.empty()
        self.alien_bullets_sprites.empty()
        # self.explosion_sprites.empty()
        
        
        # Set restart and unpause
        self.restart = True
        self.running = False # Exit current loop to trigger game restart

