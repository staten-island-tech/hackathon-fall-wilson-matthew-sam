import pygame
import math
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Dance of Fire and Ice - Alternating Balls")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Load sounds
background_music = pygame.mixer.music.load('background_music.mp3')  # Replace with your file path
hit_sound = pygame.mixer.Sound('hit_sound.wav')  # Replace with your file path
miss_sound = pygame.mixer.Sound('miss_sound.wav')  # Replace with your file path
miss_sound.set_volume(1.3)


# Start background music loop
pygame.mixer.music.play(-1, 0.0)  # Loop the background music indefinitely


# Path points
PATH = [
    (200, 300), (300, 300), (400, 300), (500, 300), (600, 300), (700, 300)
]

# Orbital movement settings
ORBIT_RADIUS = 50
BALL_RADIUS = 15

# Timing settings
BEATS_PER_SECOND = 1.5
BEAT_INTERVAL = 1 / BEATS_PER_SECOND

# State variables
last_beat_time = 0
current_angle = 0
current_path_index = 0
score = 0
missed = 0
game_over = False

# Ball alternation state
is_blue_orbiting = True  # If True, Blue ball is orbiting; else Red ball is orbiting


def reset_game():
    """Reset game state to the initial conditions."""
    global last_beat_time, current_angle, current_path_index, score, missed, game_over, is_blue_orbiting
    last_beat_time = 0
    current_angle = 0
    current_path_index = 0
    score = 0
    missed = 0
    game_over = False
    is_blue_orbiting = True


# Initialize the game
reset_game()

# Font for text
font = pygame.font.Font(None, 36)


def display_text(text, x, y, color=WHITE):
    """Display text on the screen."""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()  # Reset the game on R key press
            if event.key == pygame.K_SPACE and not game_over:
                elapsed_time = pygame.time.get_ticks() / 1000
                # Check if the orbiting ball is aligned with the path
                if abs(elapsed_time - last_beat_time) < 0.2:
                    score += 1
                    hit_sound.play()
                    # Move to the next point in the path
                    current_path_index += 1
                    if current_path_index >= len(PATH):
                        current_path_index = 0  # Loop back to the start of the path
                    is_blue_orbiting = not is_blue_orbiting  # Switch orbiting ball
                    last_beat_time = elapsed_time
                else:
                    miss_sound.play()
                    missed += 1
                    game_over = True

    # Beat generation
    elapsed_time = pygame.time.get_ticks() / 1000
    if elapsed_time - last_beat_time >= BEAT_INTERVAL:
        last_beat_time = elapsed_time

    # Update orbital angle
    current_angle += 2 * math.pi / (FPS * BEAT_INTERVAL)
    if current_angle >= 2 * math.pi:
        current_angle -= 2 * math.pi

    # Get the current stationary ball position
    stationary_x, stationary_y = PATH[current_path_index]

    # Calculate the orbiting ball position
    orbiting_x = stationary_x + ORBIT_RADIUS * math.cos(current_angle)
    orbiting_y = stationary_y + ORBIT_RADIUS * math.sin(current_angle)

    # Draw the path
    for i in range(len(PATH) - 1):
        pygame.draw.line(screen, WHITE, PATH[i], PATH[i + 1], 2)

    # Draw the stationary ball
    stationary_color = BLUE if is_blue_orbiting else RED
    pygame.draw.circle(screen, stationary_color, (stationary_x, stationary_y), BALL_RADIUS)

    # Draw the orbiting ball
    orbiting_color = RED if is_blue_orbiting else BLUE
    pygame.draw.circle(screen, orbiting_color, (int(orbiting_x), int(orbiting_y)), BALL_RADIUS)

    # Display score and missed beats
    display_text(f"Score: {score}", 10, 10)
    display_text(f"Missed: {missed}", 10, 50)
    if game_over:
        display_text("Game Over! Press R to Restart", 200, 500, RED)

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
