import pygame
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Dance of Fire and Ice")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Circle properties
radius = 20
orbit_radius = 100
angle = 0
speed = 0.05

# Path properties
path = [(WIDTH // 2, HEIGHT // 2)]
for i in range(1, 20):
    path.append((WIDTH // 2 + i * 40, HEIGHT // 2 + (i % 2) * 80 - 40))

# Scoring
score = 0
font = pygame.font.Font(None, 36)

# Music
music_file = r"C:\Users\weichen.fang24\Documents\GitHub\hackathon-fall-wilson-matthew-sam\your_music_file.mp3"
pygame.mixer.init()
pygame.mixer.music.load(music_file)
pygame.mixer.music.play(-1)

# Clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Check if the circles are in sync with the path
                if math.isclose(angle % (2 * math.pi), 0, abs_tol=0.1):
                    score += 1
                else:
                    score -= 1

    # Clear screen
    screen.fill(WHITE)

    # Draw path
    for point in path:
        pygame.draw.circle(screen, BLACK, point, 5)

    # Calculate positions
    x1 = WIDTH // 2 + orbit_radius * math.cos(angle)
    y1 = HEIGHT // 2 + orbit_radius * math.sin(angle)
    x2 = WIDTH // 2 + orbit_radius * math.cos(angle + math.pi)
    y2 = HEIGHT // 2 + orbit_radius * math.sin(angle + math.pi)

    # Draw circles
    pygame.draw.circle(screen, RED, (int(x1), int(y1)), radius)
    pygame.draw.circle(screen, BLUE, (int(x2), int(y2)), radius)

    # Update angle
    angle += speed

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
