import pygame
import random
import sys

pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 400, 400
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Relógio do jogo
clock = pygame.time.Clock()
FPS = 10

def draw_snake(snake_blocks):
    for block in snake_blocks:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_food(food_pos):
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

def main():
    snake_pos = [[100, 100]]
    direction = 'RIGHT'
    change_to = direction

    food_pos = [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]

    score = 0
    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_s and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_a and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_d and direction != 'LEFT':
                    change_to = 'RIGHT'

        direction = change_to

        # Atualiza posição da cabeça
        x, y = snake_pos[0]
        if direction == 'UP':
            y -= BLOCK_SIZE
        elif direction == 'DOWN':
            y += BLOCK_SIZE
        elif direction == 'LEFT':
            x -= BLOCK_SIZE
        elif direction == 'RIGHT':
            x += BLOCK_SIZE

        new_head = [x, y]

        # Verifica colisão
        if (
            x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or
            new_head in snake_pos
        ):
            print(f'Game over! Score: {score}')
            font = pygame.font.SysFont(None, 36)
            text = font.render(f'Game Over! Score: {score}', True, WHITE)
            screen.blit(text, (WIDTH // 4, HEIGHT // 2))
            pygame.display.update()

            # Espera até o jogador fechar a janela
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                        waiting = False

            pygame.quit()
            sys.exit()

        snake_pos.insert(0, new_head)

        # Comer comida
        if new_head == food_pos:
            score += 1
            food_pos = [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]
        else:
            snake_pos.pop()

        draw_snake(snake_pos)
        draw_food(food_pos)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
