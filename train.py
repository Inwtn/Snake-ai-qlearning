import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from snake_game_ai import SnakeGameAI
from q_learning_agent import QLearningAgent

import time


# Inicializar o ambiente e o agente
game = SnakeGameAI()
agent = QLearningAgent(game)

# Parâmetros de treino
EPISODES = 500

for episode in range(EPISODES):
    game.reset()
    total_reward = 0
    done = False

    while not done:
        state = game.get_state()
        action = agent.get_action(state)
        next_state, reward, done = game.step(action)
        agent.update_q_table(state, action, reward, next_state)
        total_reward += reward

    print(f"Episode {episode + 1} - Score: {game.score} - Total Reward: {total_reward}")

    # Exibir visualmente o jogo de vez em quando
    if episode % 50 == 0:
        game.reset()
        done = False
        while not done:
            state = game.get_state()
            action = agent.get_action(state)
            _, _, done = game.step(action)
            game.render()
            time.sleep(0.1)
