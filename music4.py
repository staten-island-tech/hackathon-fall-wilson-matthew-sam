import pygame
import random
import time
import requests

# Initialize pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Master Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font
font = pygame.font.SysFont("Arial", 40)
small_font = pygame.font.SysFont("Arial", 30)

# Fetch a list of words from a public API
def get_random_words():
    try:
        response = requests.get("https://random-word-api.herokuapp.com/word?number=10")
        words = response.json()
        return words
    except:
        return ["example", "keyboard", "pygame", "performance", "typing"]

# Game class
class TypingGame:
    def __init__(self):
        self.words = get_random_words()
        self.current_word = self.words[0]
        self.user_input = ""
        self.score = 0
        self.start_time = time.time()
        self.time_limit = 30
        self.game_over = False

    def restart(self):
        self.words = get_random_words()
        self.current_word = self.words[0]
        self.user_input = ""
        self.score = 0
        self.start_time = time.time()
        self.game_over = False

    def check_input(self):
        if self.user_input == self.current_word:
            self.score += 1
            self.user_input = ""
            self.words = get_random_words()
            self.current_word = self.words[0]

    def draw(self):
        screen.fill(WHITE)

        # Time remaining
        elapsed_time = time.time() - self.start_time
        time_remaining = self.time_limit - elapsed_time
        time_text = small_font.render(f"Time left: {max(0, int(time_remaining))}", True, BLACK)
        screen.blit(time_text, (10, 10))

        # Score
        score_text = small_font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (WIDTH - 150, 10))

        # Current word
        current_word_text = font.render(self.current_word, True, BLACK)
        screen.blit(current_word_text, (WIDTH // 2 - current_word_text.get_width() // 2, HEIGHT // 3))

        # User input
        user_input_text = font.render(self.user_input, True, GREEN)
        screen.blit(user_input_text, (WIDTH // 2 - user_input_text.get_width() // 2, HEIGHT // 2))

        # Game over screen
        if self.game_over:
            game_over_text = font.render("Game Over!", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if not self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.check_input()
                    else:
                        self.user_input += event.unicode

    def update(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.time_limit:
            self.game_over = True

# Main loop
def main():
    game = TypingGame()

    while True:
        game.handle_events()
        game.update()
        game.draw()

        if game.game_over:
            time.sleep(2)
            game.restart()

        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
