import pygame
import random
import time
import sys


# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu - Choose a Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, 50)

# Game state
current_game = None  # Variable to hold the selected game (None means menu)

# Load sounds
background_music = pygame.mixer.music.load('background_music.mp3')  # Replace with your file path
hit_sound = pygame.mixer.Sound('hit_sound.wav')  # Replace with your file path
miss_sound = pygame.mixer.Sound('miss_sound.wav')  # Replace with your file path

# Function to display text on screen
def display_text(text, x, y, font, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Main Menu Function
def main_menu():
    global current_game
    running = True

    while running:
        screen.fill(BLACK)

        # Display main menu title
        display_text("Main Menu", WIDTH // 2 - 100, 100, menu_font)

        # Display menu options
        display_text("1. Rhythm Game", WIDTH // 2 - 100, 200, font)
        display_text("2. Alternating Balls", WIDTH // 2 - 150, 250, font)
        display_text("Press 1 or 2 to select a game", WIDTH // 2 - 200, 350, font)
        display_text("Press Q to quit", WIDTH // 2 - 100, 400, font)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Select Rhythm Game
                    current_game = "rhythm_game"
                    from rhythm_game import game_loop
                    return  # Start Rhythm Game
                elif event.key == pygame.K_2:  # Select Alternating Balls
                    current_game = "alternating_balls"
                    return  # Start Alternating Balls

                elif event.key == pygame.K_q:  # Quit the game
                    running = False

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Limit to ~60 FPS

# Rhythm Game Function (Existing rhythm game code, simplified here)
def rhythm_game():

    screen.fill(BLACK)
    pygame.display.update()
    print("Starting Rhythm Game...")
    # Place rhythm game logic here, for example:
    # Implement rhythm game logic where notes fall, and player presses corresponding keys

# Alternating Balls Game (Placeholder)
def alternating_balls_game():
    import FIREGAME
    screen.fill(BLACK)
    pygame.display.update()
    print("Starting Alternating Balls Game...")
    # Implement logic for another game here (e.g., balls bouncing)

# Main Loop
def main():
    while True:
        main_menu()  # Show main menu
        
        if current_game == "rhythm_game":
            rhythm_game()  # Start the Rhythm Game
        elif current_game == "alternating_balls":
            alternating_balls_game()  # Start the Alternating Balls Game
        else:
            pygame.quit()
            sys.exit()

# Run the main function to start the game
main()
