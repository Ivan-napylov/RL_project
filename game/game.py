import pygame
from hex_map import HexMap
from army import Army

class Game:
    def __init__(self, screen_width, screen_height):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.camera = Camera(screen_width, screen_height)
        self.hex_map = HexMap(10, 10, 30, self.screen, self.camera)
        self.army = Army(self.hex_map, money=100)

    def draw_ui(self):
        font = pygame.font.SysFont(None, 24)
        money_text = font.render(f"Money: {self.army.money}", True, (255, 255, 0))
        self.screen.blit(money_text, (10, 10))

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            self.screen.fill((0, 0, 0))
            self.hex_map.draw_map()
            self.army.draw_armies(self.screen)
            self.draw_ui()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    q, r = self.get_hex_under_mouse()
                    self.army.add_army(q, r)

            pygame.display.flip()
            clock.tick(30)
        pygame.quit()

    def get_hex_under_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for tile in self.hex_map.map_grid:
            x, y = self.hex_map.hex_to_pixel(tile["q"], tile["r"])
            if (x - mouse_x) ** 2 + (y - mouse_y) ** 2 < self.hex_map.size ** 2:
                return tile["q"], tile["r"]
        return None, None
