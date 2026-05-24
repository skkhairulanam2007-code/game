# snake_game.py
# Simple Snake game using pygame
# Controls: Arrow keys or WASD
# Install: pip install pygame

import pygame # type: ignore
import random
import sys

pygame.init()
# Window size
WIDTH, HEIGHT = 640, 480
CELL = 20  # size of each grid cell
COLUMNS = WIDTH // CELL
ROWS = HEIGHT // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 20)

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)

def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def rand_food_position(snake):
    while True:
        pos = (random.randint(0, COLUMNS-1), random.randint(0, ROWS-1))
        if pos not in snake:
            return pos

def draw_rect_from_grid(pos, color):
    x, y = pos
    rect = pygame.Rect(x*CELL, y*CELL, CELL, CELL)
    pygame.draw.rect(screen, color, rect)

def show_text(text, size=20, color=WHITE, center=None):
    font = pygame.font.SysFont("consolas", size)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = center
    else:
        rect.topleft = (10, 10)
    screen.blit(surf, rect)

def main():
    # initial snake in middle, 3 blocks long
    init_x = COLUMNS // 2
    init_y = ROWS // 2
    snake = [(init_x, init_y), (init_x-1, init_y), (init_x-2, init_y)]
    direction = (1, 0)  # moving right
    next_direction = direction

    food = rand_food_position(snake)
    score = 0
    speed = 10  # starting FPS

    game_over = False

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    next_direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    next_direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    next_direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    next_direction = (1, 0)
                elif event.key == pygame.K_r and game_over:
                    # restart
                    return main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # prevent reversing directly
        if (next_direction[0] * -1, next_direction[1] * -1) != direction:
            direction = next_direction

        if not game_over:
            # move snake
            head = snake[0]
            new_head = (head[0] + direction[0], head[1] + direction[1])

            # check wall collisions
            if not (0 <= new_head[0] < COLUMNS and 0 <= new_head[1] < ROWS):
                game_over = True

            # check self collision
            if new_head in snake:
                game_over = True

            if not game_over:
                snake.insert(0, new_head)  # add new head

                # check food
                if new_head == food:
                    score += 1
                    # increase speed a little every 3 points
                    if score % 3 == 0:
                        speed = min(speed + 1, 25)
                    food = rand_food_position(snake)
                else:
                    snake.pop()  # remove tail

        # draw
        screen.fill(BLACK)
        draw_grid()

        # draw food
        draw_rect_from_grid(food, RED)

        # draw snake (head brighter)
        if snake:
            draw_rect_from_grid(snake[0], (0, 220, 0))
            for segment in snake[1:]:
                draw_rect_from_grid(segment, GREEN)

        # HUD
        show_text(f"Score: {score}", size=20, color=WHITE, center=(70, 15))

        if game_over:
            show_text("GAME OVER", size=48, color=RED, center=(WIDTH//2, HEIGHT//2 - 20))
            show_text("Press R to restart or ESC to quit", size=20, color=WHITE, center=(WIDTH//2, HEIGHT//2 + 30))

        pygame.display.flip()
        clock.tick(speed)

if __name__ == "__main__":
    main()
