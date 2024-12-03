import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set up display
WIDTH = 800
HEIGHT = 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Google Dino Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
DINO_BODY = (34, 139, 34)  # Dark green for the dinosaur
DINO_HEAD = (50, 205, 50)  # Lighter green for the head
DAY_COLOR = (135, 206, 235)  # Day sky blue
NIGHT_COLOR = (25, 25, 112)  # Night sky dark blue
LAVA_COLOR = (255, 69, 0)  # Lava color (bright red-orange)
METEOR_COLOR = (255, 69, 0)  # Meteor fiery color
EXPLOSION_COLOR = (255, 165, 0)  # Explosion particles (bright orange)
GIANT_EXPLOSION_COLOR = (255, 0, 0)  # Bright red explosion color
HEART_COLOR = (255, 0, 0)  # Heart color (Red)
EMPTY_HEART_COLOR = (0, 0, 0)  # Empty heart color (Black)
PARTICLE_COLOR = (255, 0, 0)  # Red particles for the dinosaur death effect

# Set the barrier level at the top of the screen
BARRIER_LEVEL = 0  # Barrier at the top

# Define the dino class (with custom drawing)
class Dino:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 70
        self.width = 50
        self.height = 50
        self.velocity = 0
        self.gravity = 1
        self.is_jumping = False
        self.alive = True  # Track whether the dino is alive or dead
        self.flip_over = False  # Track whether the dino is flipped over
        self.particles = []  # Red particles for death effect
        self.jump_power = -20  # Short jump power
        self.max_jump_power = -60  # High jump power (double the short jump)
        self.short_jump_height = 80  # Short jump height
        self.high_jump_height = 160  # High jump height
        self.jump_start_time = None  # To track how long spacebar is held
        self.jump_time_threshold = 1000  # Threshold for high jump (1 second)
        self.is_high_jump = False  # Track whether it's a high jump or short jump
        self.jump_cooldown = 0  # Cooldown timer for jump (in milliseconds)
        self.max_cooldown = 500  # Max cooldown time (500ms = 0.5 seconds)

    def move(self):
        if self.is_jumping:
            self.velocity += self.gravity
            self.y += self.velocity
            if self.y >= HEIGHT - 70:
                self.y = HEIGHT - 70
                self.is_jumping = False
                self.velocity = 0
                self.jump_cooldown = 0  # Reset cooldown when touching the ground

        # Check for collision with the invisible barrier at the top
        if self.y < BARRIER_LEVEL:
            self.y = HEIGHT - 70  # Push the dino back down to the ground

    def jump(self):
        if not self.is_jumping and self.alive and self.jump_cooldown == 0:
            self.is_jumping = True
            self.velocity = self.jump_power
            self.jump_start_time = pygame.time.get_ticks()  # Start tracking time when spacebar is pressed

    def release_jump(self):
        if self.is_jumping and self.jump_start_time is not None:
            hold_time = pygame.time.get_ticks() - self.jump_start_time  # Calculate how long the spacebar was held
            if hold_time >= self.jump_time_threshold:  # If held for more than 1 second, perform a high jump
                self.velocity = self.max_jump_power
                self.is_high_jump = True
            else:  # Perform a short jump otherwise
                self.velocity = self.jump_power
                self.is_high_jump = False
            self.jump_cooldown = self.max_cooldown  # Set the cooldown after the jump

    def die(self):
        self.alive = False
        self.flip_over = True
        self.generate_death_particles()

    def generate_death_particles(self):
        # Generate red particles for the death effect
        for _ in range(100):
            angle = random.uniform(0, 2 * math.pi)
            velocity = random.uniform(1, 3)
            particle = {
                "x": self.x + self.width // 2,
                "y": self.y + self.height // 2,
                "dx": velocity * math.cos(angle),
                "dy": velocity * math.sin(angle),
                "size": random.randint(3, 7),
                "color": PARTICLE_COLOR
            }
            self.particles.append(particle)

    def draw(self, screen):
        if self.alive:
            # Draw body (a simple rectangle)
            pygame.draw.rect(screen, DINO_BODY, (self.x, self.y, self.width, self.height))

            # Draw head (a simple circle)
            pygame.draw.circle(screen, DINO_HEAD, (self.x + 35, self.y - 10), 15)

            # Draw eyes (white circles for eyes)
            pygame.draw.circle(screen, WHITE, (self.x + 40, self.y - 20), 5)
            pygame.draw.circle(screen, WHITE, (self.x + 30, self.y - 20), 5)

            # Draw arms (small rectangles)
            pygame.draw.rect(screen, DINO_BODY, (self.x - 10, self.y + 10, 20, 10))
            pygame.draw.rect(screen, DINO_BODY, (self.x + 50, self.y + 10, 20, 10))

            # Draw legs (simple rectangles)
            pygame.draw.rect(screen, DINO_BODY, (self.x + 10, self.y + 40, 15, 20))
            pygame.draw.rect(screen, DINO_BODY, (self.x + 25, self.y + 40, 15, 20))
        else:
            # If the dino is dead, flip over and draw particles
            if self.flip_over:
                pygame.draw.rect(screen, DINO_BODY, (self.x, self.y, self.width, self.height))
                self.y += 10  # Move the dino down as it flips over

            # Draw the death particles
            for particle in self.particles:
                particle["x"] += particle["dx"]
                particle["y"] += particle["dy"]
                particle["size"] = max(0, particle["size"] - 0.1)  # Shrink particles over time
                pygame.draw.circle(screen, particle["color"], (particle["x"], particle["y"]), particle["size"])

# Define the obstacle class (for ground and other obstacles)
class Obstacle:
    def __init__(self, x, speed):
        self.x = x
        self.y = HEIGHT - 40  # Ground level
        self.width = random.randint(20, 40)
        self.height = random.randint(20, 40)
        self.speed = speed

    def move(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (self.x, self.y - self.height, self.width, self.height))  # Simulating obstacle

    def is_colliding(self, dino):
        # Check for collision with the dino
        if (self.x < dino.x + dino.width and
            self.x + self.width > dino.x and
            self.y - self.height < dino.y + dino.height):
            return True
        return False

# Game loop
def game_loop():
    dino = Dino()
    obstacles = []
    clock = pygame.time.Clock()
    lives = 3
    font = pygame.font.SysFont(None, 30)
    running = True
    while running:
        screen.fill(DAY_COLOR)  # Set background color
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()
                elif event.key == pygame.K_r and not dino.alive:  # Restart the game
                    if lives == 0:
                        lives = 3  # Reset lives if it's game over
                    dino = Dino()  # Reset the dinosaur
                    obstacles.clear()  # Clear obstacles
        if dino.alive:
            # Generate obstacles randomly
            if random.randint(1, 100) == 1:
                obstacles.append(Obstacle(WIDTH, random.randint(3, 6)))

            # Move and draw obstacles
            for obstacle in obstacles[:]:
                obstacle.move()
                obstacle.draw(screen)
                if obstacle.is_colliding(dino):
                    dino.die()
                    lives -= 1
                    if lives == 0:
                        dino.alive = False
                    obstacles.remove(obstacle)

            dino.move()
            dino.draw(screen)
        else:
            # Display the game over text and restart prompt
            game_over_text = font.render(f"Game Over! Press 'R' to Restart", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 2))

        # Display the lives
        lives_text = font.render(f"Lives: {lives}", True, BLACK)
        screen.blit(lives_text, (10, 10))

        pygame.display.update()  # Update display
        clock.tick(60)  # Set frame rate

# Start the game
game_loop()
pygame.quit()
