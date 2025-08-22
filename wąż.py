import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
SNAKE_SPEED = 15

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 56, 184)   # Israeli flag blue
YELLOW = (255, 215, 0) # Ukrainian flag yellow
GERMAN_RED = (221, 0, 0)

# Initialize window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.length = 8  # większy wąż na start
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        # Tworzymy początkowe pozycje węża w wybranym kierunku
        x, y = WINDOW_WIDTH//2, WINDOW_HEIGHT//2
        self.positions = [(x - i*BLOCK_SIZE*self.direction[0], y - i*BLOCK_SIZE*self.direction[1]) for i in range(self.length)]
        self.color = WHITE

    def draw(self):
        for pos in self.positions:
            rect_top = pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE // 2)
            rect_bottom = pygame.Rect(pos[0], pos[1] + BLOCK_SIZE // 2, BLOCK_SIZE, BLOCK_SIZE // 2)
            pygame.draw.rect(screen, WHITE, rect_top)   # górna połowa biała
            pygame.draw.rect(screen, RED, rect_bottom)  # dolna połowa czerwona

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = ((cur[0] + (x*BLOCK_SIZE)) % WINDOW_WIDTH, (cur[1] + (y*BLOCK_SIZE)) % WINDOW_HEIGHT)
        if new in self.positions[2:]:
            return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def grow(self):
        self.length += 1

class Food:
    def __init__(self):
        self.position = self.randomize_position()
        self.type = random.choice(['israel', 'germany', 'ukraine'])
        self.active = True
        self.moving = random.random() < 0.5  # 50% szans na ruchomą kropkę
        if self.moving:
            self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        else:
            self.direction = (0, 0)
    def move(self):
        if self.moving:
            x, y = self.position
            dx, dy = self.direction
            new_x = (x + dx * BLOCK_SIZE) % WINDOW_WIDTH
            new_y = (y + dy * BLOCK_SIZE) % WINDOW_HEIGHT
            self.position = (new_x, new_y)

    def randomize_position(self):
        return (random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE),
                random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE))

    def draw(self):
        rect = pygame.Rect(self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE)
        if self.type == 'israel':
            # Tło białe
            pygame.draw.rect(screen, WHITE, rect)
            # Górny niebieski pasek
            pygame.draw.rect(screen, BLUE, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE // 6))
            # Dolny niebieski pasek
            pygame.draw.rect(screen, BLUE, (self.position[0], self.position[1] + BLOCK_SIZE - BLOCK_SIZE // 6, BLOCK_SIZE, BLOCK_SIZE // 6))
            # Gwiazda Dawida (dwie nakładające się trójkąty)
            cx = self.position[0] + BLOCK_SIZE // 2
            cy = self.position[1] + BLOCK_SIZE // 2
            r = BLOCK_SIZE // 3
            # Górny trójkąt
            points_up = [
                (cx, cy - r),
                (cx - r, cy + r//2),
                (cx + r, cy + r//2)
            ]
            # Dolny trójkąt
            points_down = [
                (cx, cy + r),
                (cx - r, cy - r//2),
                (cx + r, cy - r//2)
            ]
            pygame.draw.polygon(screen, BLUE, points_up, 2)
            pygame.draw.polygon(screen, BLUE, points_down, 2)
        elif self.type == 'germany':
            pygame.draw.rect(screen, BLACK, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE/3))
            pygame.draw.rect(screen, GERMAN_RED, (self.position[0], self.position[1] + BLOCK_SIZE/3, BLOCK_SIZE, BLOCK_SIZE/3))
            pygame.draw.rect(screen, YELLOW, (self.position[0], self.position[1] + 2*BLOCK_SIZE/3, BLOCK_SIZE, BLOCK_SIZE/3))
        else:  # ukraine
            pygame.draw.rect(screen, BLUE, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE/2))
            pygame.draw.rect(screen, YELLOW, (self.position[0], self.position[1] + BLOCK_SIZE/2, BLOCK_SIZE, BLOCK_SIZE/2))

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    import time
    snake = Snake()
    foods = []
    next_food_time = pygame.time.get_ticks() + random.randint(200, 800)  # szybciej pojawiają się kropki

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        # Move snake
        if not snake.move():
            break

        # Dodawanie nowego jedzenia w losowym czasie
        current_time = pygame.time.get_ticks()
        if current_time >= next_food_time:
            foods.append(Food())
            next_food_time = current_time + random.randint(200, 800)

        # Poruszanie ruchomych kropek
        for food in foods:
            if food.active:
                food.move()

        # Sprawdź kolizję flagi z ogonem węża (nie z głową)
        for food in foods:
            if food.active:
                for pos in snake.positions[1:]:
                    if food.position == pos:
                        # Eksplozja: animacja
                        for i in range(8):
                            pygame.draw.circle(screen, (255, 255, 0), food.position, BLOCK_SIZE//2 + i*3)
                            pygame.display.update()
                            pygame.time.delay(20)
                        food.active = False
                        break

        # Sprawdź kolizję z dowolnym jedzeniem (śmierć przy zderzeniu)
        for food in foods:
            if food.active and snake.positions[0] == food.position:
                # Wąż ginie przy zderzeniu z kropką
                pygame.quit()
                sys.exit()

        # Draw
        LIGHT_GREEN = (144, 238, 144)
        screen.fill(LIGHT_GREEN)
        snake.draw()
        for food in foods:
            if food.active:
                food.draw()
        pygame.display.update()
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    main()