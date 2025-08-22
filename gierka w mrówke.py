import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Langton's Ant")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ant properties
ant_pos = [width // 2, height // 2]
ant_direction = 0  # 0: right, 1: down, 2: left, 3: up
grid = [[0 for _ in range(width)] for _ in range(height)]

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ant position
    current_cell = grid[ant_pos[1]][ant_pos[0]]
    
    if current_cell == 0:
        # On white cell, turn left
        ant_direction = (ant_direction + 1) % 4
        grid[ant_pos[1]][ant_pos[0]] = 1
    else:
        # On black cell, turn right
        ant_direction = (ant_direction - 1) % 4
        grid[ant_pos[1]][ant_pos[0]] = 0

    # Move ant forward
    if ant_direction == 0:
        ant_pos[0] = (ant_pos[0] + 1) % width
    elif ant_direction == 1:
        ant_pos[1] = (ant_pos[1] + 1) % height
    elif ant_direction == 2:
        ant_pos[0] = (ant_pos[0] - 1) % width
    else:
        ant_pos[1] = (ant_pos[1] - 1) % height

    # Draw
    screen.fill(WHITE)
    
    # Draw grid
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1:
                screen.set_at((x, y), BLACK)
    
    # Draw ant
    screen.set_at((ant_pos[0], ant_pos[1]), RED)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()