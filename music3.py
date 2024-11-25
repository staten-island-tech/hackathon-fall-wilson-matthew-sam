import pygame
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
ORB_RADIUS = 30
TARGET_RADIUS = 50

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dance of Fire and Ice - Rhythm Game")

# Load music and set up Pygame mixer
pygame.mixer.music.load("your_song.mp3")  # Replace with your music file
pygame.mixer.music.set_volume(0.5)

# Main game variables
fire_x, fire_y = 100, SCREEN_HEIGHT // 2
ice_x, ice_y = 700, SCREEN_HEIGHT // 2
fire_moving = True
ice_moving = True

hit_time = 1.0  # Time to hit the target in seconds (you can make this dynamic based on music)
last_hit_time = time.time()

# Game loop
running = True
clock = pygame.time.Clock()

def draw_orbs():
    pygame.draw.circle(screen, RED, (fire_x, fire_y), ORB_RADIUS)
    pygame.draw.circle(screen, BLUE, (ice_x, ice_y), ORB_RADIUS)
    
def draw_targets():
    pygame.draw.circle(screen, GREEN, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2), TARGET_RADIUS)
    pygame.draw.circle(screen, GREEN, (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2), TARGET_RADIUS)

def check_hit():
    global last_hit_time
    current_time = time.time()
    if current_time - last_hit_time >= hit_time:
        last_hit_time = current_time
        return True
    return False

# Start playing music
pygame.mixer.music.play(loops=-1, start=0.0)

while running:
    screen.fill(BLACK)
    
    # Check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Sync orbs to the beat
    if check_hit():
        if fire_moving:
            fire_x += 5  # Fire orb moves towards target
            if fire_x > SCREEN_WIDTH // 4 + TARGET_RADIUS:  # Hit the target
                fire_moving = False
        if ice_moving:
            ice_x -= 5  # Ice orb moves towards target
            if ice_x < 3 * SCREEN_WIDTH // 4 - TARGET_RADIUS:  # Hit the target
                ice_moving = False
    
    # Draw elements
    draw_orbs()
    draw_targets()
    
    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()