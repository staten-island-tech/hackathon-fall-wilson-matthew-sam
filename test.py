import pygame
import random
import math
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  
RED = (255, 0, 0)    
YELLOW = (255, 255, 0)  

TILE_SIZE = 40

PLAYER_SPEED = 5

PROXIMITY_RANGE = 80 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

clock = pygame.time.Clock()

class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.generate_maze()
        self.original_grid = [row[:] for row in self.grid]  

    def generate_maze(self):
        grid = [[1 for _ in range(self.width)] for _ in range(self.height)]

        def dfs(x, y):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                if 0 < nx < self.width and 0 < ny < self.height and grid[ny][nx] == 1:
                    grid[ny][nx] = 0  
                    grid[y + dy][x + dx] = 0  
                    dfs(nx, ny)

        start_x, start_y = 1, 1
        grid[start_y][start_x] = 0  
        dfs(start_x, start_y)

        return grid

    def clear_walls(self):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = 0  

    def restore_walls(self):
        self.grid = [row[:] for row in self.original_grid]

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                color = WHITE if self.grid[y][x] == 0 else BLACK
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

TILE_SIZE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREEN = (0, 255, 0)

class Player:
    def __init__(self, x, y, name, attack, rate, hp, speed, inventory=None, money=0):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = GREEN
        
        self.name = name
        self.attack = attack  
        self.hp = hp  
        self.rate = rate  
        self.speed = speed  
        
        self.inventory = inventory if inventory else []
        self.money = money

        self.pistol = None  
        self.bullets = []  
        self.last_shot_time = time.time()  
        self.last_attack_time = time.time() 

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        for bullet in self.bullets:
            bullet.draw()

    def move(self, dx, dy, dungeon, monsters):
        new_x = self.x + dx
        new_y = self.y + dy
        
        if new_x < 0 or new_x + self.width > SCREEN_WIDTH or new_y < 0 or new_y + self.height > SCREEN_HEIGHT:
            return
        
        if self.can_move(new_x, new_y, dungeon, monsters):
            self.x = new_x
            self.y = new_y

    def can_move(self, new_x, new_y, dungeon, monsters):
        top_left_x = new_x // TILE_SIZE
        top_left_y = new_y // TILE_SIZE
        bottom_right_x = (new_x + self.width - 1) // TILE_SIZE
        bottom_right_y = (new_y + self.height - 1) // TILE_SIZE

        if not (0 <= top_left_x < dungeon.width and 0 <= top_left_y < dungeon.height and
                0 <= bottom_right_x < dungeon.width and 0 <= bottom_right_y < dungeon.height):
            return False

        if dungeon.grid[top_left_y][top_left_x] == 1 or \
           dungeon.grid[top_left_y][bottom_right_x] == 1 or \
           dungeon.grid[bottom_right_y][top_left_x] == 1 or \
           dungeon.grid[bottom_right_y][bottom_right_x] == 1:
            return False

        for monster in monsters:
            monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
            player_rect = pygame.Rect(new_x, new_y, self.width, self.height)
            if player_rect.colliderect(monster_rect):
                return False 

        return True

    def shoot(self):
        current_time = time.time()
        if self.pistol and current_time - self.last_shot_time >= (1 / self.rate):  
            mouse_x, mouse_y = pygame.mouse.get_pos()  
            direction_x = mouse_x - (self.x + self.width // 2)  
            direction_y = mouse_y - (self.y + self.height // 2)

            distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
            if distance != 0:
                direction_x /= distance
                direction_y /= distance

            bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, direction_x, direction_y, self.attack, self.speed)
            self.bullets.append(bullet)

            self.last_shot_time = current_time

    def update_bullets(self, monsters):
        for bullet in self.bullets[:]:
            bullet.update()
            for monster in monsters:
                if bullet.collides_with(monster):
                    monster.hp -= bullet.damage  
                    self.bullets.remove(bullet)  

    def buy(self, item, money):
        if self.money >= money:
            self.inventory.append(item)
            self.money -= money
            print(f"Purchased {item}. Current inventory: {self.inventory}")
        else:
            print("Not enough money.")

class Bullet:
    def __init__(self, x, y, direction_x, direction_y, attack, speed):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = GREEN  
        self.speed = speed  
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.damage = attack  

    def update(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collides_with(self, monster):
        monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
        bullet_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return bullet_rect.colliderect(monster_rect)

player = Player(100, 100, "Player1", 20, 2, 100, 15) 
player.shoot() 

class Projectile:
    def __init__(self, x, y, direction_x, direction_y, speed):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = (0, 255, 0)  #
        self.speed = speed 
        self.direction_x = direction_x
        self.direction_y = direction_y

    def update(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Enemy:
    def __init__(self, ename, x, y, ehp, eattack, espeed, erate):
        self.name = ename
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = RED
        self.ehp = ehp
        self.eattack = eattack
        self.speed = espeed 
        self.erate = erate  
        self.is_alive = True
        self.projectiles = []
        self.last_shot_time = time.time()

    def attack(self, player):
        if self.is_alive:
            damage = self.eattack
            print(f"{self.name} attacks {player.name} for {damage} damage!")
            player.take_damage(damage)

    def shoot(self, player):
        current_time = time.time()
        if current_time - self.last_shot_time > (1 / self.erate):  
            direction_x = player.x - self.x
            direction_y = player.y - self.y
            distance = math.sqrt(direction_x**2 + direction_y**2)
            direction_x /= distance
            direction_y /= distance
            projectile = Projectile(self.x + self.width // 2, self.y + self.height // 2, direction_x, direction_y, self.speed)
            self.projectiles.append(projectile)
            self.last_shot_time = current_time

    def update_projectiles(self):
        for projectile in self.projectiles:
            projectile.update()  

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        for projectile in self.projectiles:
            projectile.draw()

    # New method to calculate distance to player
    def distance_to_player(self, player):
        return math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)

    def spawn(self, dungeon):
        while True:
            x = random.randint(1, dungeon.width - 1) * TILE_SIZE
            y = random.randint(1, dungeon.height - 1) * TILE_SIZE
            grid_x = x // TILE_SIZE
            grid_y = y // TILE_SIZE
            if dungeon.grid[grid_y][grid_x] == 0: 
                self.x = x
                self.y = y
                break

    def remove_from_game(self, dungeon):
        self.x = -TILE_SIZE  
        self.y = -TILE_SIZE
        self.projectiles.clear()
        self.ehp = 0  
        dungeon.grid[self.y // TILE_SIZE][self.x // TILE_SIZE] = 0 

Monster = Enemy(ename="Monster", x=100, y=100, ehp=100, eattack=5, espeed=8, erate=2) 

def remove_from_game(self, dungeon):
        self.x = -TILE_SIZE  
        self.y = -TILE_SIZE
        self.projectiles.clear()
        self.hp = 0  
        dungeon.grid[self.y // TILE_SIZE][self.x // TILE_SIZE] = 0 
class Merchant:
    def __init__(self):
        self.x = -TILE_SIZE 
        self.y = -TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = (0, 0, 255)  

    def spawn(self, dungeon):
        if random.random() < 0.2: 
            while True:
                x = random.randint(1, dungeon.width - 1) * TILE_SIZE
                y = random.randint(1, dungeon.height - 1) * TILE_SIZE
                grid_x = x // TILE_SIZE
                grid_y = y // TILE_SIZE
                if dungeon.grid[grid_y][grid_x] == 0:  
                    self.x = x
                    self.y = y
                    break

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def distance_to_player(self, player):
        return math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
class Projectile:
    def __init__(self, x, y, direction_x, direction_y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = RED  
        self.speed = 3
        self.direction_x = direction_x
        self.direction_y = direction_y

    def update(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collides_with(self, player):
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        projectile_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(projectile_rect)
    
class Game:
    def __init__(self):
        self.initial_spawn_position = (1 * TILE_SIZE, 1 * TILE_SIZE)  
        
        self.dungeon = Dungeon(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)
        
        self.player = Player(self.initial_spawn_position[0], self.initial_spawn_position[1], 
                             "Player1", 20, 2, 100, 15)  

        self.monster = Enemy(ename="Monster", x=100, y=100, ehp=100, eattack=5, espeed=8, erate=2)
        
        while True:
            x = random.randint(1, self.dungeon.width - 1) * TILE_SIZE
            y = random.randint(1, self.dungeon.height - 1) * TILE_SIZE
            grid_x = x // TILE_SIZE
            grid_y = y // TILE_SIZE
            if self.dungeon.grid[grid_y][grid_x] == 0:
                self.monster.x = x
                self.monster.y = y
                break

        self.merchant = Merchant()
        self.merchant.spawn(self.dungeon)
        
        self.fight_started = False
        self.proximity_message = ""  
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.score = 0 
        self.merchant_menu_active = False  
        self.previous_player_position = None


    def reset_game(self):
        self.dungeon = Dungeon(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)
        self.player = Player(self.initial_spawn_position[0], self.initial_spawn_position[1]) 
        self.monster = Monster(0, 0)
        self.monster.spawn(self.dungeon) 
        self.merchant = Merchant()
        self.merchant.spawn(self.dungeon)  
        self.fight_started = False
        self.proximity_message = ""  
        self.score = 0  


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.proximity_message == "Press Space to Open Merchant Menu":
                        self.toggle_merchant_menu()

                    elif self.proximity_message == "Press Space to Fight":
                        self.start_boss_fight()

    def toggle_merchant_menu(self):
        if self.merchant_menu_active:
            self.teleport_player_back()
            self.dungeon.restore_walls()  
            self.merchant_menu_active = False  
        else:
            self.clear_walls_for_merchant_interaction()
            self.merchant_menu_active = True  

    def clear_walls_for_merchant_interaction(self):
        self.dungeon.clear_walls()
        self.previous_player_position = (self.player.x, self.player.y)  
        self.player.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2  
        self.player.y = SCREEN_HEIGHT - TILE_SIZE - 10  
        self.merchant.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2  
        self.merchant.y = SCREEN_HEIGHT // 4 - TILE_SIZE // 2  
        self.proximity_message = ""  

    def teleport_player_back(self):
        self.player.x, self.player.y = self.previous_player_position
        self.previous_player_position = None  

    def start_boss_fight(self):
        self.starting_position = (self.player.x, self.player.y)
    
        self.dungeon.clear_walls()
        self.player.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2  
        self.player.y = SCREEN_HEIGHT - TILE_SIZE - 10
        self.monster.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2  
        self.monster.y = SCREEN_HEIGHT // 2 - TILE_SIZE // 2  
        self.fight_started = True
        self.player.pistol = True  

    def end_boss_fight(self):
        self.dungeon.restore_walls()
        self.merchant = Merchant()
        self.merchant.spawn(self.dungeon)  
        self.monster = Monster(0, 0)
        self.monster.spawn(self.dungeon) 

        self.player.x, self.player.y = self.starting_position

        self.fight_started = False
        self.proximity_message = ""  

def update(self):
    if self.player.hp <= 0:  
        self.reset_game()  
        return  

    if self.monster.ehp <= 0:
        self.monster.remove_from_game(self.dungeon)
        self.dungeon.restore_walls() 
        self.end_boss_fight() 
        self.score += 10  
        return  

    keys = pygame.key.get_pressed()
    
    dx = 0  # Horizontal movement
    dy = 0  # Vertical movement
    
    if keys[pygame.K_a]:  # Move left
        dx = -PLAYER_SPEED
    if keys[pygame.K_d]:  # Move right
        dx = PLAYER_SPEED
    if keys[pygame.K_w]:  # Move up
        dy = -PLAYER_SPEED
    if keys[pygame.K_s]:  # Move down
        dy = PLAYER_SPEED
    
    # Apply movement if valid
    self.player.move(dx, dy, self.dungeon, [self.monster])

    if self.fight_started and pygame.mouse.get_pressed()[0]: 
        self.player.shoot()

    self.proximity_message = ""
    if not self.fight_started:
        dist = self.monster.distance_to_player(self.player)
        if dist <= PROXIMITY_RANGE:
            self.proximity_message = "Press Space to Fight"

        dist_merchant = self.merchant.distance_to_player(self.player)
        if dist_merchant <= PROXIMITY_RANGE:
            self.proximity_message = "Press Space to Open Merchant Menu"

    if self.fight_started:
        self.monster.shoot(self.player)
        self.monster.update_projectiles(self.player)
        self.player.update_bullets(self.monster)

def run(self):
    while self.running:
        self.handle_events()
        self.update()
        self.draw()
        clock.tick(FPS)

    def draw(self):
        screen.fill(BLACK)

        self.dungeon.draw()
        self.player.draw()

        self.monster.draw()

        self.merchant.draw()

        if self.proximity_message:
            text = self.font.render(self.proximity_message, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - 50))

        hp_text = self.font.render(f"HP: {self.player.hp}", True, GREEN)
        screen.blit(hp_text, (10, 10))

        if self.fight_started:
            monster_hp_text = self.font.render(f"HP: {self.monster.hp}", True, RED)
            screen.blit(monster_hp_text, (SCREEN_WIDTH - 100, 10)) 

        score_text = self.font.render(f"Score: {self.score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

        if self.merchant_menu_active:
            self.draw_merchant_menu()

        pygame.display.flip()

    def draw_merchant_menu(self):
        menu_text = self.font.render("Welcome to the Merchant! (Press Space to Exit)", True, WHITE)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 3))

        item_text = self.font.render("1. Buy Health Potion - 10 Gold", True, WHITE)
        screen.blit(item_text, (SCREEN_WIDTH // 2 - item_text.get_width() // 2, SCREEN_HEIGHT // 3 + 50))

game = Game()

game.run()

pygame.quit()

if __name__ == "__main__":
    game = Game()  
    game.run()  
