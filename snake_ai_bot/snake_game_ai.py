import numpy as np
import random

BLOCK_SIZE = 20
WIDTH = 640
HEIGHT = 480

class SnakeGameAI:
    def __init__(self):
        self.reset()

    def reset(self):
        self.direction = 'RIGHT'
        self.head = [WIDTH // 2, HEIGHT // 2]
        self.snake = [self.head[:], [self.head[0]-BLOCK_SIZE, self.head[1]], [self.head[0]-2*BLOCK_SIZE, self.head[1]]]
        self.spawn_food()
        self.frame_iteration = 0
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        import random
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = [x, y]
        if self.food in self.snake:
            self.spawn_food()

    def is_collision(self, point=None):
        if point is None:
            point = self.head
        # Check wall collision
        if point[0] >= WIDTH or point[0] < 0 or point[1] >= HEIGHT or point[1] < 0:
            return True
        # Check self collision
        if point in self.snake[1:]:
            return True
        return False

    def move(self, action):
        '''
        action: 0 = straight, 1 = right turn, 2 = left turn
        direction order: [RIGHT, DOWN, LEFT, UP]
        '''
        clock_wise = ['RIGHT', 'DOWN', 'LEFT', 'UP']
        idx = clock_wise.index(self.direction)

        if action == 0:  # straight
            new_dir = clock_wise[idx]
        elif action == 1:  # right turn
            new_dir = clock_wise[(idx + 1) % 4]
        else:  # left turn
            new_dir = clock_wise[(idx - 1) % 4]

        self.direction = new_dir

        x, y = self.head
        if self.direction == 'RIGHT':
            x += BLOCK_SIZE
        elif self.direction == 'LEFT':
            x -= BLOCK_SIZE
        elif self.direction == 'UP':
            y -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            y += BLOCK_SIZE

        self.head = [x, y]

    def play_step(self, action):
        self.frame_iteration += 1
        self.move(action)

        reward = 0
        if self.is_collision():
            self.game_over = True
            reward = -10
            return reward, True, self.score

        self.snake.insert(0, self.head[:])

        if self.head == self.food:
            self.score += 1
            reward = 10
            self.spawn_food()
            self.frame_iteration = 0
        else:
            self.snake.pop()
            reward = -0.1  # small penalty for each step without eating

        if self.frame_iteration > 100*len(self.snake):
            # snake is taking too long, end game
            self.game_over = True
            reward = -10
            return reward, True, self.score

        return reward, False, self.score

    def get_state(self):
        head = self.head
        point_l = [head[0] - BLOCK_SIZE, head[1]]
        point_r = [head[0] + BLOCK_SIZE, head[1]]
        point_u = [head[0], head[1] - BLOCK_SIZE]
        point_d = [head[0], head[1] + BLOCK_SIZE]

        dir_l = self.direction == 'LEFT'
        dir_r = self.direction == 'RIGHT'
        dir_u = self.direction == 'UP'
        dir_d = self.direction == 'DOWN'

        danger_straight = (
            (dir_r and self.is_collision(point_r)) or
            (dir_l and self.is_collision(point_l)) or
            (dir_u and self.is_collision(point_u)) or
            (dir_d and self.is_collision(point_d))
        )
        danger_right = (
            (dir_u and self.is_collision(point_r)) or
            (dir_d and self.is_collision(point_l)) or
            (dir_l and self.is_collision(point_u)) or
            (dir_r and self.is_collision(point_d))
        )
        danger_left = (
            (dir_d and self.is_collision(point_r)) or
            (dir_u and self.is_collision(point_l)) or
            (dir_r and self.is_collision(point_u)) or
            (dir_l and self.is_collision(point_d))
        )

        food_left = self.food[0] < head[0]
        food_right = self.food[0] > head[0]
        food_up = self.food[1] < head[1]
        food_down = self.food[1] > head[1]

        state = (
            danger_straight,
            danger_right,
            danger_left,
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            food_left,
            food_right,
            food_up,
            food_down
        )
        return state