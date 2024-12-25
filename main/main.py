# Import libraries
import pygame
from hexmap import HexMap
from army import Army
from reward import CoinSystem

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Antiyoy")

        # Screen dimensions and refresh rate
        self.height = 600
        self.width = 800
        self.fps = 30

        # Initialize game components
        self.coin_system = CoinSystem(initial_balance=100, width = self.width, height=self.height)
        self.hex_map = HexMap(map_size=5, cell_size=30, coin_system=self.coin_system)  # Using the provided HexMap class
        self.hex_map.generate_user_land(initial_cells=[(0, 0), (0, 1), (1, 0)], owner='user', owner_color=(0, 255, 0))
        self.army = Army(x=20, y=20, width=120, height=40, color=(255, 0, 0), label="Army 1", coin_system=self.coin_system)

        # Create game window
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        selected_content = None  # Tracks current action (e.g., selected soldier level)
        temp_pos = None
        owner = 'user'
        while running:
            self.screen.fill((0, 0, 0))  # Clear the screen

            # Draw game map and entities
            self.hex_map.draw(self.screen)  # Draw the hex map
            self.army.draw(self.screen)  # Draw the army button
            self.coin_system.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # Check if army button is clicked
                        if self.army.is_clicked(event.pos):
                            selected_content = self.army.update()

                        # Check if hex map handles a click (e.g., placing a soldier)
                        check, pos = self.hex_map.is_clicked(event.pos, selected_content, owner)
                        if check and not pos:
                            if selected_content:
                                self.army.level = -1  # Reset army button level
                                selected_content = None
                                self.army.text = self.army.init_text
                        if check and pos:
                            temp_pos = pos
                        
                        if temp_pos and not check and pos:
                            self.hex_map.move_or_place_soldier(temp_pos, pos, owner)
                            temp_pos = None
                        
                        self.hex_map.start_drag()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Stop dragging on mouse release
                        self.hex_map.stop_drag()

                elif event.type == pygame.MOUSEMOTION:
                    # Handle dragging of the map
                    if self.hex_map.dragging:
                        self.hex_map.handle_drag()  

                self.hex_map.handle_movement_events(event) 

            pygame.display.flip()  # Update the display
            self.clock.tick(self.fps)  # Cap the frame rate

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
