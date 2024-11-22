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

# Define the dino class (with custom drawing)
class Dino:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 70
        self.width = 50
        self.height = 50
        self.velocity = 0
        self.gravity = 1
        self.jump_power = -20  # Higher jump power
        self.is_jumping = False
        self.alive = True  # Track whether the dino is alive or dead
        self.flip_over = False  # Track whether the dino is flipped over
        self.particles = []  # Red particles for death effect

    def move(self):
        if self.is_jumping:
            self.velocity += self.gravity
            self.y += self.velocity
            if self.y >= HEIGHT - 70:
                self.y = HEIGHT - 70
                self.is_jumping = False
                self.velocity = 0

    def jump(self):
        if not self.is_jumping and self.alive:
            self.is_jumping = True
            self.velocity = self.jump_power

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

# Define the lava class
class Lava:
    def __init__(self, volcano_x):
        self.x = volcano_x
        self.y = HEIGHT - 40  # Same ground level
        self.width = random.randint(20, 50)
        self.height = random.randint(10, 30)
        self.speed = 3

    def move(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, LAVA_COLOR, (self.x, self.y - self.height, self.width, self.height))

    def is_colliding(self, dino):
        # Check for collision with the dino
        if (self.x < dino.x + dino.width and
            self.x + self.width > dino.x and
            self.y - self.height < dino.y + dino.height and
            self.y > dino.y):
            return True
        return False

# Define the volcano class
class Volcano:
    def __init__(self):
        self.x = random.randint(WIDTH // 2, WIDTH - 100)
        self.y = HEIGHT - 100  # Volcanos are placed higher
        self.active = False

    def activate(self):
        self.active = True

    def draw(self, screen):
        if self.active:
            pygame.draw.polygon(screen, (139, 69, 19), [(self.x, self.y), (self.x + 50, self.y - 50), (self.x + 100, self.y)])  # Draw volcano

# Define the meteor class
class Meteor:
    def __init__(self, x, speed):
        self.x = x
        self.y = random.randint(0, HEIGHT // 2)  # Randomize the meteor's starting height
        self.size = random.randint(20, 40)  # Random meteor size
        self.speed = speed
        self.exploded = False

    def move(self):
        self.x -= self.speed  # Meteor moves left

    def draw(self, screen):
        pygame.draw.circle(screen, METEOR_COLOR, (self.x, self.y), self.size)  # Draw the meteor

    def is_colliding(self, dino):
        # Check if the meteor is colliding with the dino
        if (self.x - self.size < dino.x + dino.width and
            self.x + self.size > dino.x and
            self.y - self.size < dino.y + dino.height and
            self.y + self.size > dino.y):
            return True
        return False

    def explode(self):
        # Simulate an explosion when the meteor hits the ground
        self.exploded = True

# Function to display hearts
def draw_lives(screen, lives):
    for i in range(3):
        if i < lives:
            pygame.draw.circle(screen, HEART_COLOR, (WIDTH - 20 - i * 40, 20), 15)  # Red hearts
        else:
            pygame.draw.circle(screen, EMPTY_HEART_COLOR, (WIDTH - 20 - i * 40, 20), 15)  # Empty hearts

# Game loop
def game_loop():
    dino = Dino()
    obstacles = []
    meteors = []
    lava = []
    volcano = Volcano()
    lives = 3
    score = 0
    clock = pygame.time.Clock()
    run_game = True

    while run_game:
        screen.fill(DAY_COLOR if score % 2 == 0 else NIGHT_COLOR)  # Day/Night cycle

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and dino.alive:
                    dino.jump()
                if event.key == pygame.K_r and not dino.alive:
                    game_loop()  # Restart the game

        # Moving and drawing dino
        if dino.alive:
            dino.move()
        dino.draw(screen)

        # Spawn obstacles
        if len(obstacles) == 0 or obstacles[-1].x < WIDTH - random.randint(250, 350):
            obstacles.append(Obstacle(WIDTH, 5))

        # Draw obstacles
        for obstacle in obstacles:
            obstacle.move()
            obstacle.draw(screen)
            if obstacle.is_colliding(dino) and dino.alive:
                lives -= 1
                obstacles.remove(obstacle)  # Remove obstacle upon collision
                if lives == 0:
                    dino.die()  # Dino dies if no lives remain

        # Handle lava
        for lava_stream in lava:
            lava_stream.move()
            lava_stream.draw(screen)
            if lava_stream.is_colliding(dino):
                lives -= 1  # Lose a life if hit by lava
                lava.remove(lava_stream)
                if lives == 0:
                    dino.die()

        # Handle meteors (same logic)
        if random.randint(1, 100) == 1:
            meteors.append(Meteor(WIDTH, 5))

        for meteor in meteors:
            meteor.move()
            meteor.draw(screen)
            if meteor.is_colliding(dino):
                dino.die()  # Dino dies if hit by a meteor
                meteors.remove(meteor)

        # Handle volcano (random event)
        if random.randint(1, 500) == 1:
            volcano.activate()

        # Draw volcano and lava
        volcano.draw(screen)
        if volcano.active:
            if random.randint(1, 100) == 1:
                lava.append(Lava(volcano.x))

        # Update score and display it
        score = pygame.time.get_ticks() // 1000  # 1 point every second
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Draw hearts representing lives at the top right
        draw_lives(screen, lives)

        # Check for game over
        if lives == 0:
            font = pygame.font.SysFont(None, 50)
            game_over_text = font.render("GAME OVER", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))

            restart_text = font.render("Press 'R' to Restart", True, BLACK)
            screen.blit(restart_text, (WIDTH // 3, HEIGHT // 2))

            dino.flip_over = True  # Flip the dino over on game over

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Run the game
game_loop()