import pygame
import math
from noise import pnoise2  # Import Perlin noise function

class HexMap:
    def __init__(self, cols, rows, size, screen, camera, scale=0.1):
        self.cols = cols
        self.rows = rows
        self.size = size
        self.screen = screen
        self.camera = camera
        self.scale = scale  # Scale factor for noise generation
        self.map_grid = self.generate_map()

    def generate_map(self):
        # Create the map grid with noise-based terrain generation
        map_grid = []
        for q in range(self.cols):
            for r in range(self.rows):
                # Generate Perlin noise value for each tile
                noise_value = pnoise2(q * self.scale, r * self.scale)
                tile_type = "empty" if noise_value > 0 else "obstacle"
                map_grid.append({
                    "q": q, "r": r, "type": tile_type, "content": None
                })
        return map_grid

    def hex_to_pixel(self, q, r):
        x = self.size * (math.sqrt(3) * (q + r / 2))
        y = self.size * (3 / 2 * r)
        return x + self.camera.offset_x, y + self.camera.offset_y

    def draw_hexagon(self, center_x, center_y):
        corners = [self.hex_corner(center_x, center_y, self.size, i) for i in range(6)]
        pygame.draw.polygon(self.screen, (0, 255, 0), corners, 1)

    def hex_corner(self, center_x, center_y, size, i):
        angle_deg = 60 * i + 30
        angle_rad = math.pi / 180 * angle_deg
        return center_x + size * math.cos(angle_rad), center_y + size * math.sin(angle_rad)

    def draw_map(self):
        for tile in self.map_grid:
            x, y = self.hex_to_pixel(tile["q"], tile["r"])
            self.draw_hexagon(x, y)

    def set_tile_content(self, q, r, content):
        for tile in self.map_grid:
            if tile["q"] == q and tile["r"] == r:
                tile["content"] = content
                break

    def get_tile(self, q, r):
        for tile in self.map_grid:
            if tile["q"] == q and tile["r"] == r:
                return tile
        return None
