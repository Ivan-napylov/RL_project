import pygame
class Army:
    def __init__(self, hex_map, money):
        self.hex_map = hex_map
        self.money = money
        self.armies = []

    def add_army(self, q, r):
        if self.money >= 10:
            tile = self.hex_map.get_tile(q, r)
            if tile and tile["type"] == "empty" and tile["content"] is None:
                tile["content"] = "army"
                self.armies.append((q, r))
                self.money -= 10
                print(f"Army added at ({q}, {r})")
            else:
                print("Cannot place army here.")
        else:
            print("Not enough money to add an army.")

    def draw_armies(self, screen):
        for q, r in self.armies:
            x, y = self.hex_map.hex_to_pixel(q, r)
            pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), 5)
