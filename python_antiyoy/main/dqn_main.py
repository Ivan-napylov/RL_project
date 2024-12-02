import pygame
import random
from HexMap import HexMap
from config.config import *
from variable import army
import numpy as np
from dqn import DQN


class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Antiyoy")

        # Initialize map and agent
        self.HexMap = HexMap(cols=10, rows=10, size=20, screen_width=800, screen_height=300)
        self.army = army.Army(20, 20, 120, 40, (255,0,0), "Army 1")
        self.agent = DQN(state_dim=100, action_dim=100)  # 100 possible actions (10x10 grid)
        
        # Initialize the game screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def action_to_coordinates(self, action):
        # Map action to (x, y) coordinates on the hex map
        x = action // self.HexMap.cols  # Row
        y = action % self.HexMap.cols   # Column
        return x, y


    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))

            # Get current state
            state = np.array(self.HexMap.get_state()).flatten()

            print("############### STATE: ", state)

            # Agent chooses action (i.e., selects a hex cell)
            action = self.agent.choose_action(state)
            x, y = self.action_to_coordinates(action)

            # Perform the action and get the reward
            reward, done = self.HexMap.perform_action(x, y, content=self.army.update())

            # Get the next state after the action
            next_state = np.array(self.HexMap.get_state()).flatten()

            # Store the transition in the agent's memory
            self.agent.store_transition(state, action, reward, next_state, done)

            # Train the agent 
            self.agent.learn()

            # If the game is over, update the target network
            if done:
                self.agent.update_target_network()

            # Draw game elements
            self.HexMap.draw_map()
            self.army.draw(self.screen)
            # self.army.draw_entities(self.screen, soldiers)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            pygame.display.flip()
            self.clock.tick(30)  # Update 30 times per second
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()

