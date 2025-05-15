import pygame
import random
import sys

WIDTH, HEIGHT = 400, 400
BLOCK_SIZE = 20

class SnakeGameAI:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake AI Manual')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.snake = [[100, 100]]
        self.direction = 'RIGHT'
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        pos = [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]
        while pos in self.snake:
            pos = [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]
        return pos

    def get_state(self):
        return {
            'snake': self.snake,
            'food': self.food,
            'direction': self.direction
        }

    def step(self, action):
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.direction = directions[action]

        x, y = self.snake[0]
        if self.direction == 'UP':
            y -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            y += BLOCK_SIZE
        elif self.direction == 'LEFT':
            x -= BLOCK_SIZE
        elif self.direction == 'RIGHT':
            x += BLOCK_SIZE

        new_head = [x, y]

        # Verifica colisão
        if (
            x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or
            new_head in self.snake
        ):
            self.game_over = True
            reward = -10
            return self.get_state(), reward, True

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            reward = 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()
            reward = 0

        return self.get_state(), reward, False

    def render(self):
        self.display.fill((0, 0, 0))
        for block in self.snake:
            pygame.draw.rect(self.display, (0, 255, 0), pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.update()
        self.clock.tick(10)

    def play_manual(self):
        direction = self.direction
        running = True

        while running:
            self.display.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and direction != 'DOWN':
                        direction = 'UP'
                    elif event.key == pygame.K_s and direction != 'UP':
                        direction = 'DOWN'
                    elif event.key == pygame.K_a and direction != 'RIGHT':
                        direction = 'LEFT'
                    elif event.key == pygame.K_d and direction != 'LEFT':
                        direction = 'RIGHT'

            # Atualiza posição da cabeça
            x, y = self.snake[0]
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
                new_head in self.snake
            ):
                print(f'Game Over! Score: {self.score}')
                font = pygame.font.SysFont(None, 36)
                text = font.render(f'Game Over! Score: {self.score}', True, (255, 255, 255))
                self.display.blit(text, (WIDTH // 4, HEIGHT // 2))
                pygame.display.update()

                # Espera até o jogador fechar a janela ou apertar uma tecla
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                            waiting = False
                running = False
                pygame.quit()
                sys.exit()

            self.snake.insert(0, new_head)

            if new_head == self.food:
                self.score += 1
                self.food = self.spawn_food()
            else:
                self.snake.pop()

            self.render()
            self.clock.tick(10)

if __name__ == '__main__':
    game = SnakeGameAI()
    game.play_manual()
