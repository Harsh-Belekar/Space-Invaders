import pygame
from os.path import join

# Asset Base Path 
SOUND_PATH = join("Assets", "Sounds")
SCORE_PATH = join("Assets",  "Scores-Files")
FONTS_PATH = join("Assets","Fonts")
PLAYER_PATH = join("Assets", "Images", "Player")
ENEMY_PATH = join("Assets", "Images", "Enemy")
EXPLOSION_PATH = join("Assets","Images", "Explosion")
BACKGROUND_PATH = join("Assets","Images","UI","Background")
MENU_PATH = join("Assets","Images","UI","Main-Menu")
BANNERS_PATH = join("Assets","Images","UI","Banners")

# Colors
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)


# Image Loader 
def load_image(path: str, img_name: str, convert_alpha=True):
    try:
        img_path = join(path, img_name)
        img = pygame.image.load(img_path)
        return img.convert_alpha() if convert_alpha else img.convert()
    except Exception as e:
        print(f"[ERROR] Failed to load image: {img_path}\n{e}")
        return None

# Loading Series Images
def load_image_series(path:str, img_cat: str, frame_count: int):
        return [
        load_image(path, f"{img_cat}{i}.png")
        for i in range(1, frame_count + 1)
    ]

# Sound Loader
def load_sound(path: str, file: str):
    try:
        sound = join(path, file)
        return pygame.mixer.Sound(sound)
    
    except Exception as e:
        print(f"[ERROR] Failed to load Sound: {path}\n{e}")
        return None

# Font Loader
def load_font(path: str, file: str, size: int):
    try:
        font = join(path, file)
        return pygame.font.Font(font,size)
    
    except Exception as e:
        print(f"[ERROR] Failed to load Font: {path}\n{e}")
        return None


# Image Assets
images = {
    "spaceship_img" : load_image(PLAYER_PATH, "spaceship.png"),
    "laser_img" : load_image(PLAYER_PATH, "laser.png"),
    "bullet_img" : load_image(PLAYER_PATH, "bullet.png"),
    "alien_bullet_img" : load_image(ENEMY_PATH, "alien_bullet.png"),
    "meteor_img" : load_image(ENEMY_PATH, "meteor.png"),

    "explosion_frames" : load_image_series(EXPLOSION_PATH,"exp",5),
    "alien_explosion_frames" : load_image_series(EXPLOSION_PATH,"A_exp",5),
    "aliens_img" : load_image_series(ENEMY_PATH,"alien",5),
    
    "bg" : load_image(BACKGROUND_PATH, "bg.png", False,),
    "logo": load_image(MENU_PATH, "game_logo.png"),
    "start": load_image(MENU_PATH, "start_button.png"),
    "help": load_image(MENU_PATH, "help_button.png"),
    "exit": load_image(MENU_PATH, "exit_button.png"),
    "back": load_image(MENU_PATH, "back_button.png"),
    "restart": load_image(MENU_PATH, "restart_button.png"),
    
    "win": load_image(BANNERS_PATH, "win_banner.png"),
    "lose": load_image(BANNERS_PATH, "lose_banner.png")
}

images["spaceship_damage_frames"] = [pygame.transform.scale(img,(20,20)) for img in images["explosion_frames"]]

# Sound Effects
sounds = {
    "click" : load_sound(SOUND_PATH, "click.wav"),
    "bullet" : load_sound(SOUND_PATH, "bullet.wav"),
    "laser" : load_sound(SOUND_PATH, "laser.wav"),
    "explosion_sound" : load_sound(SOUND_PATH, "explosion.wav"),
    "meteor_explosion_sound" : load_sound(SOUND_PATH, "explosion_1.wav"),
    "damage_sound" : load_sound(SOUND_PATH, "damage.ogg"),
    "game_music" : load_sound(SOUND_PATH, "game_music.wav")
}

# Load Font
font18 = load_font(FONTS_PATH, "Oxanium-Bold.ttf", 18)
font30 = load_font(FONTS_PATH, "Oxanium-Bold.ttf", 30)
font40 = load_font(FONTS_PATH, "Oxanium-Bold.ttf", 40)