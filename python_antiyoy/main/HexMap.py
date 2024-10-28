import pygame
import math
import json
from perlin_noise import PerlinNoise
from p_noise import PerlinNoiseGenerator

class HexMap:
    def __init__(self, cols, rows, size, screen_width, screen_height, scale=0.1):
        self.cols = cols  
        self.rows = rows  
        self.size = size  

        self.screen_width = screen_width  
        self.screen_height = screen_height  
        self.map_grid = [[0 for _ in range(rows)] for _ in range(cols)]  
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  

        #Инициализация камеры
        self.camera = Camera(screen_width, screen_height)
        self.noise_generator = PerlinNoiseGenerator(scale)

        # Создаём структуру для хранения всех вершин с информацией о каждой ячейке
        self.map_grid = []
        for q in range(cols):
            for r in range(rows):
                noise_value = self.noise_generator.get_noise(q, r)
                if noise_value > 0:
                    self.map_grid.append({
                        "q": q,
                        "r": r,
                        "type": "empty",  
                        "content": None   
                    })

    # Функция для генерации координат вершин гексагона
    def hex_corner(self, center_x, center_y, size, i):
        angle_deg = 60 * i + 30
        angle_rad = math.pi / 180 * angle_deg
        return center_x + size * math.cos(angle_rad), center_y + size * math.sin(angle_rad)

    # Функция для отрисовки гексагона
    def draw_hexagon(self, center_x, center_y):
        corners = [self.hex_corner(center_x, center_y, self.size, i) for i in range(6)]
        pygame.draw.polygon(self.screen, (0, 255, 0), corners, 1)

    # Преобразование из осевых координат в пиксельные для odd-q горизонтальной системы
    def hex_to_pixel(self, q, r):
        x = self.size * (math.sqrt(3) * (q + r / 2))
        y = self.size * (3/2 * r)
        return x, y

    # Отрисовка всей карты
    def draw_map(self):
        self.screen.fill((0, 0, 0))  
        for q in range(self.cols):
            for r in range(self.rows):
                x, y = self.hex_to_pixel(q, r)
                x += self.camera.offset_x
                y += self.camera.offset_y
                self.draw_hexagon(x + self.screen_width // 4, y + self.screen_height // 4)  #

        
        pygame.display.flip()  

    # Получение состояния карты 
    def get_map_state(self):
        return self.map_grid
    
    # Установка типа и содержимого для вершины
    def set_tile(self, q, r, tile_type="empty", content=None):
        for tile in self.map_grid:
            if tile["q"] == q and tile["r"] == r:
                tile["type"] = tile_type
                tile["content"] = content
                break

    # Получение данных о ячейке
    def get_tile(self, q, r):
        for tile in self.map_grid:
            if tile["q"] == q and tile["r"] == r:
                return tile
        return None

    # Сохранение состояния карты в JSON файл
    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.map_grid, f, indent=4)

    # Загрузка состояния карты из JSON файла
    def load_from_json(self, filename):
        with open(filename, 'r') as f:
            self.map_grid = json.load(f)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:

            self.draw_map()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:  # Сохранение карты при нажатии 'S'
                        self.save_to_json('hex_map.json')
                    elif event.key == pygame.K_l:  # Загрузка карты при нажатии 'L'
                        self.load_from_json('hex_map.json')
                    elif event.key == pygame.K_1:  # Пример изменения тайла
                        self.set_tile(2, 3, tile_type="obstacle", content="rock")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  
                        self.camera.start_drag(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    if self.camera.dragging:
                        self.camera.drag(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3: 
                        self.camera.stop_drag()

            clock.tick(30)  # Обновление 30 раз в секунду
        pygame.quit()



class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height
        self.dragging = False  # Флаг для отслеживания перетаскивания камеры
        self.last_mouse_pos = None  # Последняя позиция мыши

    # Начало перетаскивания камеры
    def start_drag(self, mouse_pos):
        self.dragging = True
        self.last_mouse_pos = mouse_pos

    # Перетаскивание камеры
    def drag(self, mouse_pos):
        if self.dragging and self.last_mouse_pos:
            dx = mouse_pos[0] - self.last_mouse_pos[0]
            dy = mouse_pos[1] - self.last_mouse_pos[1]
            self.offset_x += dx
            self.offset_y += dy
            self.last_mouse_pos = mouse_pos

    # Остановка перетаскивания камеры
    def stop_drag(self):
        self.dragging = False
        self.last_mouse_pos = None
