import pygame
import sys
import time

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Zmiana koloru ekranu")

colors = [(0, 0, 255), (255, 0, 0)]  # niebieski, czerwony
color_index = 0
last_switch = time.time()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = time.time()
    if current_time - last_switch >= 2:
        color_index = 1 - color_index
        last_switch = current_time

    screen.fill(colors[color_index])
    pygame.display.flip()

pygame.quit()
sys.exit()