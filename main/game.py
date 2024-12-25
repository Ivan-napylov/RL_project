import pygame
from hexmap import HexMap
from agent import Agent
from reward import CoinSystem

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Hex Game")
    clock = pygame.time.Clock()
    coin_system1 = CoinSystem(800, 600, initial_balance=100)
    coin_system2 = CoinSystem(800, 600, margin_bottom=50, initial_balance=100)
    hex_map = HexMap(map_size=5, cell_size=30)

    # Create agents
    user_agent = Agent("user", hex_map, initial_cells=[(-4, 1), (-3, 0), (-3, 1), (-4, 2)], color=(0, 255, 0), coin_system=coin_system1)
    ai_agent = Agent("agent", hex_map, initial_cells=[(-1, -3), (0, -4), (1, -4)],color=(0, 255, 255), coin_system=coin_system2)

    running = True

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

        # User agent action
        user_agent.choose_action()

        # AI agent action
        ai_agent.choose_action()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()