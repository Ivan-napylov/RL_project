import pygame
import numpy as np
import random
from dqn import DQNAgent
from hexmap import HexMap
from reward import CoinSystem
from agent import Agent

random.seed(42)
np.random.seed(42)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Hex Game")
    clock = pygame.time.Clock()
    coin_system1 = CoinSystem(800, 600, initial_balance=100)
    coin_system2 = CoinSystem(800, 600, margin_bottom=50, initial_balance=100)
    hex_map = HexMap(map_size=5, cell_size=30)

    user_agent = Agent("user", hex_map, initial_cells=[(-4, 1), (-3, 0), (-3, 1), (-4, 2)], color=(0, 255, 0), coin_system=coin_system1)
    ai_agent = Agent("agent", hex_map, initial_cells=[(-1, -3), (0, -4), (1, -4)],color=(0, 255, 255), coin_system=coin_system2)

    hex_map.agents = [user_agent, ai_agent]

    action_size = 2  # 0 = move, 1 = add soldier
    user_state_dim = len(user_agent.get_state(ai_agent))
    ai_state_dim = len(ai_agent.get_state(user_agent))

    dqn_user_agent = DQNAgent(state_dim=user_state_dim, action_dim=action_size)
    dqn_ai_agent = DQNAgent(state_dim=ai_state_dim, action_dim=action_size)
    
    running = True
    iterations = 100000
    while running:
        screen.fill((0, 0, 0))
        hex_map.draw(screen)
        coin_system1.draw(screen)
        coin_system2.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    hex_map.start_drag()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    hex_map.stop_drag()

            elif event.type == pygame.MOUSEMOTION:
                if hex_map.dragging:
                    hex_map.handle_drag()

        # Get state
        user_state = user_agent.get_state(ai_agent)
        user_action = dqn_user_agent.select_action(user_state)

        ai_state = ai_agent.get_state(user_agent)
        ai_action = dqn_ai_agent.select_action(ai_state)
        
        user_result = user_agent.choose_action(user_action)
        ai_result = ai_agent.choose_action(ai_action)

        user_reward = user_agent.calculate_reward(user_action)
        ai_reward = ai_agent.calculate_reward(ai_action)
    

        user_next_state = user_agent.get_state(ai_agent)
        ai_next_state = ai_agent.get_state(user_agent)

        dqn_user_agent.store_experience(user_state, user_action, user_reward, user_next_state, done=False)
        dqn_ai_agent.store_experience(ai_state, ai_action, ai_reward, ai_next_state, done=False)

        # Train the agents
        dqn_user_agent.train()
        dqn_ai_agent.train()

        if iterations % 10 == 0:
            dqn_user_agent.save_weights("user_agent.pth")
            dqn_ai_agent.save_weights("ai_agent.pth")

        iterations += 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()