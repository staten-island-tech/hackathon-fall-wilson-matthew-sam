import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up display with larger dimensions
screen_width = 1200  # Increased width
screen_height = 800  # Increased height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hollow Purple Effect - Dodge the Particles")

# Define colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
GLOW_COLOR = (128, 0, 128)  # Glow around the purple ball
GLOW_INTENSITY = 150  # Light intensity for the glow effect
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 255, 0)

# Ball settings
ball_radius = 200  # Larger radius for the red and blue balls
purple_ball_radius = 400  # Larger radius for the combined purple ball
ball_speed = 4  # Slower speed for smoother movement

# Player settings
player_radius = 20
player_speed = 5
player_pos = [screen_width // 2, screen_height // 2]
player_alive = True

# Particle settings
particle_count = 50
particles = []

# Score settings
score = 0
font = pygame.font.SysFont("Arial", 30)

# Ball positions
red_ball_pos = [screen_width // 4, screen_height // 2]
blue_ball_pos = [screen_width * 3 // 4, screen_height // 2]

# Time settings
clock = pygame.time.Clock()

def draw_ball(color, position, radius):
    pygame.draw.circle(screen, color, position, radius)

def move_ball_towards(ball_pos, target_pos, speed):
    dx = target_pos[0] - ball_pos[0]
    dy = target_pos[1] - ball_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance > speed:
        dx /= distance
        dy /= distance
        ball_pos[0] += dx * speed
        ball_pos[1] += dy * speed
    else:
        ball_pos[0] = target_pos[0]
        ball_pos[1] = target_pos[1]

def create_particles(position):
    for _ in range(particle_count):
        particle = {
            "pos": position,
            "speed": [random.uniform(-2, 2), random.uniform(-2, 2)],
            "color": (random.randint(128, 255), random.randint(0, 128), random.randint(128, 255)),
            "size": random.randint(2, 6),
            "lifetime": random.randint(60, 120),  # Increased lifetime range
            "alpha": random.randint(50, 255)
        }
        particles.append(particle)

def draw_particles():
    global particles
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for particle in particles[:]:
        # Move the particle
        particle["pos"][0] += particle["speed"][0]
        particle["pos"][1] += particle["speed"][1]
        particle["lifetime"] -= 1
        particle["alpha"] = max(0, particle["alpha"] - 3)

        # Check collision with mouse
        dist_to_mouse = math.sqrt((particle["pos"][0] - mouse_x) ** 2 + (particle["pos"][1] - mouse_y) ** 2)
        if dist_to_mouse < particle["size"] * 2:
            # "Bounce" off the mouse: reverse the direction
            angle = math.atan2(mouse_y - particle["pos"][1], mouse_x - particle["pos"][0])
            particle["speed"][0] = -math.cos(angle) * random.uniform(3, 6)
            particle["speed"][1] = -math.sin(angle) * random.uniform(3, 6)
            particle["alpha"] = max(0, particle["alpha"] - 50)  # Make the particle fade out faster upon collision

        # Draw the particle with alpha blending
        pygame.draw.circle(screen, (particle["color"][0], particle["color"][1], particle["color"][2], particle["alpha"]),
                           (int(particle["pos"][0]), int(particle["pos"][1])), particle["size"])
        
        # Remove particle if lifetime is over
        if particle["lifetime"] <= 0 or particle["alpha"] <= 0:
            particles.remove(particle)

def draw_glow(position, radius):
    # Create a glowing aura around the purple ball
    for i in range(6, 0, -1):
        pygame.draw.circle(screen, (GLOW_COLOR[0], GLOW_COLOR[1], GLOW_COLOR[2], GLOW_INTENSITY // i),
                           position, radius + i)

def draw_ripple(position, max_radius):
    # Draw an expanding ripple effect when the purple ball forms
    for i in range(0, max_radius, 10):
        pygame.draw.circle(screen, (PURPLE[0], PURPLE[1], PURPLE[2], 100 - (i // 4)),
                           position, i, 2)

def mix_colors(color1, color2, factor):
    """ Mix two colors together based on a given factor (0 = color1, 1 = color2) """
    r = color1[0] * (1 - factor) + color2[0] * factor
    g = color1[1] * (1 - factor) + color2[1] * factor
    b = color1[2] * (1 - factor) + color2[2] * factor
    return (int(r), int(g), int(b))

def check_collision(player_pos, particle):
    """ Check if the player collides with a particle """
    dist_to_player = math.sqrt((player_pos[0] - particle["pos"][0]) ** 2 + (player_pos[1] - particle["pos"][1]) ** 2)
    return dist_to_player < player_radius + particle["size"]

def reset_game():
    global player_pos, player_alive, particles, score
    player_pos = [screen_width // 2, screen_height // 2]
    player_alive = True
    particles.clear()
    score = 0

# Main loop
running = True
while running:
    screen.fill(BLACK)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Check for player movement input (WASD)
    keys = pygame.key.get_pressed()
    if player_alive:
        if keys[pygame.K_w]:
            player_pos[1] -= player_speed
        if keys[pygame.K_s]:
            player_pos[1] += player_speed
        if keys[pygame.K_a]:
            player_pos[0] -= player_speed
        if keys[pygame.K_d]:
            player_pos[0] += player_speed
    
    # Check if the player collides with any particle
    if player_alive:
        for particle in particles[:]:
            if check_collision(player_pos, particle):
                player_alive = False
                break
    
    # Move balls toward the center
    move_ball_towards(red_ball_pos, [screen_width // 2, screen_height // 2], ball_speed)
    move_ball_towards(blue_ball_pos, [screen_width // 2, screen_height // 2], ball_speed)
    
    # Calculate color transition effect between red and blue
    factor = min(1, max(0, math.sqrt((red_ball_pos[0] - blue_ball_pos[0]) ** 2 + (red_ball_pos[1] - blue_ball_pos[1]) ** 2) / 500))
    current_color = mix_colors(RED, BLUE, factor)
    
    # Draw the red and blue balls with color transition
    draw_ball(current_color, red_ball_pos, ball_radius)
    draw_ball(current_color, blue_ball_pos, ball_radius)
    
    # Check if balls have reached the center
    if red_ball_pos == blue_ball_pos == [screen_width // 2, screen_height // 2]:
        # Create particles to simulate energy explosion when balls meet
        create_particles([screen_width // 2, screen_height // 2])
        
        # Draw ripple effect around the purple ball
        draw_ripple([screen_width // 2, screen_height // 2], purple_ball_radius)
        
        # Draw the glowing purple ball
        draw_glow([screen_width // 2, screen_height // 2], purple_ball_radius)
        
        # Draw the purple ball itself
        draw_ball(PURPLE, [screen_width // 2, screen_height // 2], purple_ball_radius)
    
    # Draw particles (now with mouse interaction)
    draw_particles()
    
    # Draw the player
    if player_alive:
        pygame.draw.circle(screen, PLAYER_COLOR, (int(player_pos[0]), int(player_pos[1])), player_radius)
    
    # Update score
    if player_alive:
        score += 1

    # Draw the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Check for restart input (R key)
    if not player_alive and keys[pygame.K_r]:
        reset_game()
    
    # Update the screen
    pygame.display.flip()
    
    # Set FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
