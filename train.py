from snake_ai_bot.snake_game_ai import SnakeGameAI
from snake_ai_bot.q_learning_agent import QLearningAgent

import time

def train():
    game = SnakeGameAI()
    agent = QLearningAgent(game)

    n_episodes = 1000

    for episode in range(n_episodes):
        game.reset()
        state = game.get_state()
        total_reward = 0
        while True:
            action = agent.get_action(state)
            reward, done, score = game.play_step(action)
            next_state = game.get_state()
            agent.update_q_table(state, action, reward, next_state)
            state = next_state
            total_reward += reward
            if done:
                break
        agent.decay_epsilon()
        print(f"Episode {episode+1} - Score: {score} - Total Reward: {total_reward:.2f} - Epsilon: {agent.epsilon:.4f}")

if __name__ == "__main__":
    train()

