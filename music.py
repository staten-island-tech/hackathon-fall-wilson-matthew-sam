import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Note settings
NOTE_WIDTH = 50
NOTE_HEIGHT = 50
NOTE_SPEED = 5

# Key mappings
KEYS = {
    pygame.K_d: 'D',
    pygame.K_f: 'F',
    pygame.K_j: 'J',
    pygame.K_k: 'K'
}

# Note class
class Note:
    def __init__(self, x, y, key):
        self.rect = pygame.Rect(x, y, NOTE_WIDTH, NOTE_HEIGHT)
        self.key = key

    def update(self):
        self.rect.y += NOTE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

# Game loop
def game_loop():
    clock = pygame.time.Clock()
    notes = []
    running = True
    feedback = ""
    font = pygame.font.Font(None, 36)

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in KEYS:
                    for note in notes:
                        # Check if the note is within the hit range
                        if note.key == KEYS[event.key] and SCREEN_HEIGHT - NOTE_HEIGHT - 10 < note.rect.y < SCREEN_HEIGHT - NOTE_HEIGHT + 10:
                            notes.remove(note)
                            feedback = "Hit!"
                            break
                    else:
                        feedback = "Miss!"

        # Add new notes
        if random.randint(1, 20) == 1:
            x = random.choice([SCREEN_WIDTH // 4, SCREEN_WIDTH // 2, 3 * SCREEN_WIDTH // 4])
            key = random.choice(list(KEYS.values()))
            notes.append(Note(x, 0, key))

        # Update and draw notes
        for note in notes:
            note.update()
            note.draw(screen)

        # Draw feedback
        feedback_text = font.render(feedback, True, GREEN if feedback == "Hit!" else RED)
        screen.blit(feedback_text, (SCREEN_WIDTH // 2 - feedback_text.get_width() // 2, SCREEN_HEIGHT - 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Run the game
game_loop()
