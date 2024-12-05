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
        self.invincible = False  # Track whether the dino is invincible
        self.invincibility_time = 0  # Time when invincibility starts
        self.invincibility_duration = 1000  # Invincibility lasts for 1000 ms (1 second)

    def move(self):
        if self.is_jumping:
            self.velocity += self.gravity  # Apply gravity
            self.y += self.velocity  # Move the dino vertically based on its velocity

            if self.y >= HEIGHT - 70:  # When the dino hits the ground
                self.y = HEIGHT - 70  # Reset the position to the ground level
                self.is_jumping = False  # Stop the jump
                self.velocity = 0  # Reset velocity when landing
                self.jump_cooldown = 0  # Reset cooldown after landing

        # Prevent the dino from moving above a certain barrier level
        if self.y < BARRIER_LEVEL:
            self.y = HEIGHT - 20  # Push the dino back down to the ground

    def jump(self):
        # Only allow jumping if the dino isn't already jumping and it's alive
        if not self.is_jumping and self.alive and self.jump_cooldown == 0:
            self.is_jumping = True
            self.velocity = self.jump_power  # Apply initial jump force
            self.jump_start_time = pygame.time.get_ticks()  # Track when the spacebar is pressed

    def take_damage(self):
        # Only allow the dino to take damage if it is not invincible
        if not self.invincible:
            self.invincible = True  # Activate invincibility
            self.invincibility_time = pygame.time.get_ticks()  # Start invincibility timer
            return True  # Damage is successfully taken
        return False  # No damage taken if invincible

    def update_invincibility(self):
        # Check if invincibility duration has expired
        if self.invincible and pygame.time.get_ticks() - self.invincibility_time > self.invincibility_duration:
            self.invincible = False  # Reset invincibility

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
            # If the dino is dead, flip over only after losing all lives
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

# Define the meteor class (for meteors falling from the sky)
class Meteor:
    def __init__(self, x, speed):
        self.x = x
        self.y = -30  # Start above the screen
        self.size = random.randint(10, 30)
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, METEOR_COLOR, (self.x, self.y), self.size)

    def is_colliding(self, dino):
        # Check for collision with the dino
        if (self.x - self.size < dino.x + dino.width and
            self.x + self.size > dino.x and
            self.y - self.size < dino.y + dino.height):
            return True
        return False

# Define the lava class (lava blocks falling from volcano)
class Lava:
    def __init__(self, volcano_x):
        self.x = volcano_x
        self.y = HEIGHT - 70  # Lava starts from the ground level
        self.width = 30
        self.height = 10
        self.speed = 5

    def move(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, LAVA_COLOR, (self.x, self.y - self.height, self.width, self.height))  # Lava rectangle

    def is_colliding(self, dino):
        # Check for collision with the dino
        if (self.x < dino.x + dino.width and
            self.x + self.width > dino.x and
            self.y - self.height < dino.y + dino.height):
            return True
        return False

# Define the volcano class (for lava generation)
class Volcano:
    def __init__(self):
        self.x = WIDTH - 100  # Position at the right edge of the screen
        self.y = HEIGHT - 100  # Position above the ground
        self.width = 50
        self.height = 30
        self.speed = 5  # Speed at which lava spawns

    def move(self):
        # The volcano stays stationary, but it can still move other objects (like lava)
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))  # Volcano rectangle

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
    game_over = False  # Track game over state

    while run_game:
        screen.fill(DAY_COLOR if score % 2 == 0 else NIGHT_COLOR)  # Day/Night cycle

        # Draw lives counter
        for i in range(lives):
            pygame.draw.circle(screen, HEART_COLOR, (WIDTH - 40 - (i * 30), 20), 10)
        for i in range(3 - lives):
            pygame.draw.circle(screen, EMPTY_HEART_COLOR, (WIDTH - 40 - (i * 30), 20), 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and dino.alive and not game_over:
                    dino.jump()  # Jump only when the spacebar is initially pressed
                if event.key == pygame.K_r and not dino.alive and lives > 0:  # Restart game when 'R' is pressed
                    game_loop()
                elif event.key == pygame.K_r and not dino.alive and lives == 0:  # Exit game after all lives are gone
                    run_game = False

        # If the dino is alive, update its movements
        if dino.alive:
            dino.move()
        dino.draw(screen)

        # Spawn obstacles with increased space between them
        if random.randint(1, 150) <= 3:  # 3% chance to spawn obstacle with greater gap
            obstacles.append(Obstacle(WIDTH, 5))

        # Move and draw obstacles
        for obstacle in obstacles:
            obstacle.move()
            obstacle.draw(screen)

            if obstacle.is_colliding(dino):  # If the dino collides with the obstacle
                if not dino.invincible:  # Only take damage if not invincible
                    if dino.take_damage():  # The dino takes damage
                        lives -= 1
                        if lives <= 0:  # If no lives are left, game over
                            dino.alive = False
                            game_over = True

        # Spawn meteors with decreased spawn rate
        if random.randint(1, 100) <= 2:  # 2% chance to spawn meteor
            meteors.append(Meteor(random.randint(0, WIDTH), 5))

        # Move and draw meteors
        for meteor in meteors:
            meteor.move()
            meteor.draw(screen)

            if meteor.is_colliding(dino):  # If the dino collides with the meteor
                if not dino.invincible:  # Only take damage if not invincible
                    if dino.take_damage():  # The dino takes damage
                        lives -= 1
                        if lives <= 0:  # If no lives are left, game over
                            dino.alive = False
                            game_over = True

        # Spawn lava
        if random.randint(1, 100) <= 4:  # 4% chance to spawn lava
            lava.append(Lava(volcano.x))

        # Move and draw lava
        for lava_block in lava:
            lava_block.move()
            lava_block.draw(screen)

            if lava_block.is_colliding(dino):  # If the dino collides with the lava
                if not dino.invincible:  # Only take damage if not invincible
                    if dino.take_damage():  # The dino takes damage
                        lives -= 1
                        if lives <= 0:  # If no lives are left, game over
                            dino.alive = False
                            game_over = True

        # Move and draw the volcano
        volcano.move()
        volcano.draw(screen)

        # Update invincibility state
        dino.update_invincibility()

        # Display game over screen
        if game_over:
            font = pygame.font.SysFont(None, 55)
            restart_text = font.render("Game Over! Press 'R' to Restart", True, BLACK)
            screen.blit(restart_text, (WIDTH // 3, HEIGHT // 2))

        pygame.display.update()
        clock.tick(60)

# Start the game loop
game_loop()

# Quit pygame
pygame.quit()
