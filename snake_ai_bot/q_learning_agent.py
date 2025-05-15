import numpy as np
import random


class QLearningAgent:
    def __init__(self, game, learning_rate=0.1, discount_factor=0.9, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        self.game = game
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

    def get_state_key(self, state):
        return str(state)

    def get_action(self, state):
        state_key = self.get_state_key(state)
        if random.uniform(0, 1) < self.epsilon:
            return random.choice([0, 1, 2])  # 3 ações: frente, direita, esquerda
        else:
            if state_key not in self.q_table:
                self.q_table[state_key] = np.zeros(3)
            return int(np.argmax(self.q_table[state_key]))

    def update_q_table(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(3)

        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(3)

        best_next_action = np.max(self.q_table[next_state_key])
        td_target = reward + self.discount_factor * best_next_action
        td_delta = td_target - self.q_table[state_key][action]
        self.q_table[state_key][action] += self.learning_rate * td_delta

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay