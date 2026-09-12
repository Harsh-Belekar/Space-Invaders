import pygame

# Setup 
pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Invaders')

#  Imports Python Codes 
import button
import Help
from Assets import images, sounds  
import Mission


# Setup Buttons
start_button = button.Button(291, 370, images["start"], 1)
help_button = button.Button(50, 405, images["help"], 1)
exit_button = button.Button(560, 405, images["exit"], 1)


#  Main Menu Loop 
def main():
    clock = pygame.time.Clock()
    
    # Flag to control the main loop
    running = True
    
    # Play Game's Background music
    sounds["game_music"].play(loops= -1)

    while running:
        clock.tick(FPS)
        
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.blit(images["bg"], (0, 0)) 
        screen.blit(images["logo"], (126, 100))
        
        if start_button.draw(screen):
            sounds["click"].play() 
            mission_screen = Mission.Mission_Class() # Create battle instance
            mission_screen.run_game()  # Run the battle screen
        
        if help_button.draw(screen):
            sounds["click"].play()
            Help.help_screen()  # Show help screen 
        
        if exit_button.draw(screen):
            sounds["click"].play() 
            running = False # Exit the main menu loop 
        
        pygame.display.update()
    
    pygame.quit() # Close the Pygame window and clean up resources

# Start Game
if __name__ == "__main__":
    main()