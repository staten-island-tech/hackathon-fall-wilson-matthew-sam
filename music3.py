import pygame
import random

# Initialize pygame
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rhythm Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Hit area Y position (where the player hits notes)
hit_area_y = 500
tolerance = 30  # Tolerance for timing precision in Y-axis for hits

# Game variables
score = 0
combo = 0
max_combo = 0
accuracy = 'None'

# Note Class
class Note:
    def __init__(self, x, y, key, speed=5, color=RED):
        self.x = x
        self.y = y
        self.key = key
        self.speed = speed
        self.color = color
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        # Draw the note as a colored rectangle
        pygame.draw.rect(screen, self.color, (self.x, self.y, 50, 50))
        
        # Draw the corresponding key label on the note
        font = pygame.font.SysFont("Arial", 24)
        key_label = font.render(self.key.upper(), True, WHITE)
        screen.blit(key_label, (self.x + 15, self.y + 15))  # Position the label inside the note

# Generate notes at random intervals
def generate_notes(note_list, key_mapping, speed_multiplier):
    if random.random() < 0.02:  # Random chance to generate a note
        key = random.choice(list(key_mapping.keys()))
        note_x = key_mapping[key]
        note_color = random.choice([RED, BLUE])  # Randomly choose note color
        note_speed = random.randint(5, 10) * speed_multiplier  # Random speed for note
        note = Note(note_x, -50, key, note_speed, note_color)
        note_list.append(note)

# Check input for notes
def check_input(key_press, notes, score, combo):
    global hit_area_y, tolerance, max_combo, accuracy
    for note in notes:
        if note.key == key_press:
            # Calculate the accuracy
            distance = abs(note.y - hit_area_y)
            if distance < tolerance:
                # Perfect hit
                score += 100
                combo += 1
                accuracy = 'Perfect'
            elif distance < tolerance + 20:
                # Good hit
                score += 50
                combo += 1
                accuracy = 'Good'
            else:
                # Missed hit
                score -= 25
                combo = 0
                accuracy = 'Miss'
            if combo > max_combo:
                max_combo = combo

            notes.remove(note)  # Remove the note after hit
            break
    return score, combo

# Display Game Over screen
def game_over_screen(score):
    font = pygame.font.SysFont("Arial", 36)
    text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 50))
    
    # Retry or quit prompt
    retry_text = font.render("Press R to Restart or Q to Quit", True, YELLOW)
    screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2 + 50))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_game_loop()  # Restart the game
                    waiting_for_input = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Main game loop
def main_game_loop():
    global score, combo, max_combo, accuracy
    running = True
    notes = []
    speed_multiplier = 1.0  # Control speed over time
    
    # Key mappings to X positions on the screen (using D, F, J, K keys)
    key_mapping = {'D': 200, 'F': 300, 'J': 400, 'K': 500}
    
    # The position of the "hit line" at the bottom of the screen
    hit_line_y = 480  # Just above the hit area

    while running:
        screen.fill(BLACK)

        # Draw the hit line at the bottom of the screen
        pygame.draw.line(screen, WHITE, (0, hit_line_y), (screen_width, hit_line_y), 5)

        # Generate new notes at random intervals
        generate_notes(notes, key_mapping, speed_multiplier)
        
        # Move and draw notes
        for note in notes:
            note.move()
            note.draw(screen)
        
        # Detect player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key in key_mapping:
                    score, combo = check_input(key, notes, score, combo)
        
        # Display the score
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Display combo
        combo_text = font.render(f"Combo: {combo} (Max: {max_combo})", True, YELLOW)
        screen.blit(combo_text, (10, 40))
        
        # Display accuracy (Perfect, Good, Miss)
        accuracy_text = font.render(f"Accuracy: {accuracy}", True, GREEN)
        screen.blit(accuracy_text, (10, 70))
        
        # Remove notes that have gone past the screen
        notes = [note for note in notes if note.y < screen_height]
        
        # Game over condition if there are too many notes on the screen
        if len(notes) > 50:
            running = False
            game_over_screen(score)
        
        # Increase difficulty by speeding up notes over time
        if score > 500:
            speed_multiplier = 1.5
        if score > 1000:
            speed_multiplier = 2.0
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

# Start the game
if __name__ == "__main__":
    main_game_loop()
