import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Rhythm Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont("Arial", 40)

# Define the keys for the rhythm game
valid_keys = ['d', 'f', 'j', 'k']

# Define game parameters
note_speed = 3  # Slower speed for notes
line_position = screen_height - 60  # Position of the line where notes should align

# Define timing parameters
perfect_window = 0.1  # Ideal time window (in seconds) for perfect press
late_early_window = 0.3  # Window for late/early presses (in seconds)

# Define the Note class to represent the keys that need to be pressed
class Note:
    def __init__(self, key, y_position, spawn_time):
        self.key = key
        self.y = y_position
        self.x = 0  # Initially place it off-screen
        self.spawn_time = spawn_time  # Time when the note should ideally be pressed
        if key == 'd':
            self.x = 200
        elif key == 'f':
            self.x = 300
        elif key == 'j':
            self.x = 500
        elif key == 'k':
            self.x = 600
        self.height = 50
        self.width = 50

    def move(self):
        self.y += note_speed  # Move the note downwards

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

# Function to display text
def display_text(text, color, y_position):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, y_position))

# Game loop
def game_loop():
    running = True
    score = 0
    missed_notes = 0
    notes = []
    key_presses = []
    start_time = time.time()  # Time when the game starts
    rhythm_timing = [1.0, 1.5, 2.0, 2.5, 3.0]  # Rhythm interval times (in seconds)
    current_time = 0
    missing_note = False

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    key_presses.append(('d', time.time() - start_time))
                elif event.key == pygame.K_f:
                    key_presses.append(('f', time.time() - start_time))
                elif event.key == pygame.K_j:
                    key_presses.append(('j', time.time() - start_time))
                elif event.key == pygame.K_k:
                    key_presses.append(('k', time.time() - start_time))

        # Create new notes at predefined times based on rhythm_timing
        current_time = time.time() - start_time

        if rhythm_timing and current_time >= rhythm_timing[0]:
            key = random.choice(valid_keys)
            notes.append(Note(key, 0, rhythm_timing[0]))  # Create a new note at the top
            rhythm_timing.pop(0)  # Remove the last rhythm timing and generate a new one
            rhythm_timing.append(current_time + random.choice([1.0, 1.5, 2.0]))  # Add next note's time

        # Move and draw notes
        for note in notes:
            note.move()
            note.draw()

        # Check for notes that reach the bottom of the screen (missed notes)
        for note in notes[:]:
            if note.y >= line_position:  # If note reaches the line at the bottom
                notes.remove(note)  # Remove the note
                # Check the timing of the key press
                key_pressed = [x[0] for x in key_presses if abs(x[1] - note.spawn_time) < late_early_window]
                if note.key in key_pressed:
                    time_difference = abs(x[1] - note.spawn_time)  # Time difference from the ideal press time
                    if time_difference < perfect_window:
                        score += 50  # Full points for perfect timing
                    elif time_difference < late_early_window:
                        score += 20  # Fewer points for slightly early or late presses
                    key_presses = [x for x in key_presses if x[0] != note.key]  # Remove key press from queue
                else:
                    missed_notes += 1  # Count missed notes

        # Display missed note message
        if missed_notes > 0:
            display_text("You missed a note!", YELLOW, 100)

        # Draw the line at the bottom of the screen (UI Line)
        pygame.draw.line(screen, BLACK, (0, line_position), (screen_width, line_position), 5)

        # Draw score and missed notes count
        display_text(f'Score: {score}', BLACK, 20)
        display_text(f'Missed Notes: {missed_notes}', BLACK, 60)

        # Update the screen
        pygame.display.update()

        # Control the frame rate (limit the game to ~60 FPS)
        pygame.time.Clock().tick(60)

    pygame.quit()

# Start the game
game_loop()
