import numpy as np
import random

class QLearningAgent:
    def __init__(self, game, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.game = game
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

    def get_state_key(self, state):
        return str(state['snake']) + str(state['food']) + state['direction']

    def get_action(self, state):
        state_key = self.get_state_key(state)
        if random.uniform(0, 1) < self.epsilon:
            return random.choice([0, 1, 2, 3])
        else:
            if state_key not in self.q_table:
                self.q_table[state_key] = np.zeros(4)
            return np.argmax(self.q_table[state_key])

    def update_q_table(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(4)

        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(4)

        best_next_action = np.max(self.q_table[next_state_key])
        self.q_table[state_key][action] += self.learning_rate * (
            reward + self.discount_factor * best_next_action - self.q_table[state_key][action]
        )
