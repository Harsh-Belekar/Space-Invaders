import pygame
import button
from Assets import images, sounds, font40, font30, RED, WHITE  # Import centralized assets

def draw_text(text, font, text_col, pos):
    img = font.render(text, True, text_col)
    pygame.display.get_surface().blit(img, pos)

# ----------------- Help Screen Function -----------------
def help_screen():
    help_running = True
    clock = pygame.time.Clock()
    FPS = 60
    
    # Create Button
    back_button = button.Button(5, 5, images["back"], 0.5)

    # Instruction Lines
    instructions = [
        "1. Use LEFT Arrow Key to Move Left",
        "2. Use RIGHT Arrow Key to Move Right",
        "3. Use UP Arrow Key to Move Up",
        "4. Use DOWN Arrow Key to Move Down",
        "5. Press SPACE Key to Fire Bullet to kill Alien",
        "6. Press Shift + SPACE to Fire Liser to Destroy Meteor"
    ]

    # Help Screen Loop
    while help_running:
        clock.tick(FPS)  # Maintain frame rate
        pygame.display.get_surface().fill("black")  # Clear screen

        # Render Title
        draw_text("Controls", font40, RED, (319, 30))

        # Render Instructions 
        for i, line in enumerate(instructions):
            draw_text(line, font30, WHITE, (20, 90 + i * 60))

        # Draw Back Button
        if back_button.draw(pygame.display.get_surface()):
            sounds["click"].play()
            help_running = False  # Exit Help Screen

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                help_running = False

        # Update Screen
        pygame.display.update()