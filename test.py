import pygame
import sys
from rhythm_game import game_loop  # Import the game loop from rhythm_game.py

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu - Choose a Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, 50)

# Game state
current_game = None  # Variable to hold the selected game (None means menu)

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
                    return  # Start Rhythm Game
                elif event.key == pygame.K_2:  # Select Alternating Balls
                    current_game = "alternating_balls"
                    return  # Start Alternating Balls
                elif event.key == pygame.K_q:  # Quit the game
                    running = False

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Limit to ~60 FPS

# Function to display text on screen
def display_text(text, x, y, font, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Main Loop
def main():
    while True:
        main_menu()  # Show main menu
        
        if current_game == "rhythm_game":
            rhythm_game()  # Start the Rhythm Game (calls game_loop from rhythm_game.py)
        elif current_game == "alternating_balls":
            alternating_balls_game()  # Start the Alternating Balls Game (implement similar logic)
        else:
            pygame.quit()
            sys.exit()

# Run the main function to start the game
main()
