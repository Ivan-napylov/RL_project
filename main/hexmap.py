import pygame
import json
import math
from army import Soldier

class HexCell:
    def __init__(self, q, r, content=None, owner=None, owner_color=None, level=0, agents=[]):
        self.q = q
        self.r = r
        self.content = content
        self.owner = owner
        self.level = level
        self.owner_color = owner_color
        self.agents = agents

    def get_agent_by_color(self, color):
        for agent in self.agents:
            if agent.color == color:
                return agent
        return None

    def to_dict(self):
        return {
            "q": self.q,
            "r": self.r,
            "content": self.content,
            "owner": self.owner,
            "level": self.level,
        }

    @staticmethod
    def from_dict(data):
        return HexCell(
            q=data["q"],
            r=data["r"],
            content=data.get("content"),
            owner=data.get("owner"),
            level=data.get("level", 0),
        )
    
    def is_owned_by(self, agent):
        return self.owner == agent

class HexMap:
    DIRECTIONS = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]

    def __init__(self, map_size, cell_size):
        self.map_size = map_size
        self.cell_size = cell_size
        self.grid = self.generate_map()
        self.camera_offset = [0, 0]
        self.dragging = False
        self.last_mouse_pos = None

    def generate_map(self):
        grid = {}
        for q in range(-self.map_size, self.map_size + 1):
            for r in range(-self.map_size, self.map_size + 1):
                if -q - r in range(-self.map_size, self.map_size + 1):
                    grid[(q, r)] = HexCell(q, r)
        return grid
    
    def generate_user_land(self, initial_cells, owner, owner_color):
        for q, r in initial_cells:
            if (q, r) in self.grid and not self.grid[(q, r)].owner:
                self.grid[(q, r)].owner = owner
                self.grid[(q, r)].owner_color = owner_color

    def axial_to_pixel(self, q, r):
        x = self.cell_size * 3/2 * q
        y = self.cell_size * math.sqrt(3) * (r + q / 2)
        return x + self.camera_offset[0], y + self.camera_offset[1]

    def draw(self, screen):
        font = pygame.font.Font(None, 20)
        for cell in self.grid.values():
            x, y = self.axial_to_pixel(cell.q, cell.r)
            corners = self.get_hex_corners(x, y)

            color = (255, 0, 0)
            if cell.owner_color:
                color = cell.owner_color

            pygame.draw.polygon(screen, color, corners, width=1)
            # just text for visualization
            text_surface = font.render(f"({str(cell.q)}, {str(cell.r)})", True, (255, 10, 0))
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)

            if cell.content:
                if isinstance(cell.content, Soldier):
                    pygame.draw.circle(screen, cell.content.color, (int(x), int(y)), 10)

    def get_hex_corners(self, x, y):
        angles = [math.radians(60 * i) for i in range(6)]
        return [
            (x + self.cell_size * math.cos(angle), y + self.cell_size * math.sin(angle))
            for angle in angles
        ]
    
    def start_drag(self):
        self.dragging = True
        self.last_mouse_pos = pygame.mouse.get_pos()
    
    def handle_drag(self):
        if self.dragging:
            current_mouse_pos = pygame.mouse.get_pos()
            dx = current_mouse_pos[0] - self.last_mouse_pos[0]
            dy = current_mouse_pos[1] - self.last_mouse_pos[1]
            self.camera_offset[0] += dx
            self.camera_offset[1] += dy
            self.last_mouse_pos = current_mouse_pos
    
    def stop_drag(self):
        self.dragging = False
    
    def is_clicked(self, mouse_pos, selected_content, owner=None):
        # return pos if in that cell already user
        for cell in self.grid.values():
            x, y = self.axial_to_pixel(cell.q, cell.r)
            if self.is_point_inside_hex(x, y, mouse_pos):
                # print(f"Clicked: ({str(cell.q)}, {str(cell.r)})")
                if owner and isinstance(cell.content, Soldier) and cell.owner == owner:
                    # move soldier
                    return True, (cell.q, cell.r)
                elif selected_content and selected_content.get('type') == 'soldier':
                    # Place soldier in the clicked cell
                    self.place_soldier(cell.q, cell.r, selected_content['level'], owner)
                    return True, None
                elif not isinstance(cell.content, Soldier):
                    return False, (cell.q, cell.r)
        return False, None

    def handle_movement_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.dragging = True
                self.last_mouse_pos = pygame.mouse.get_pos()
            elif event.button == 3:
                self.is_clicked(event.pos, "")
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            current_mouse_pos = pygame.mouse.get_pos()
            dx = current_mouse_pos[0] - self.last_mouse_pos[0]
            dy = current_mouse_pos[1] - self.last_mouse_pos[1]
            self.camera_offset[0] += dx
            self.camera_offset[1] += dy
            self.last_mouse_pos = current_mouse_pos
    
    def place_soldier(self, q, r, soldier_level, agent):
        soldier = Soldier(level=soldier_level)
        # Place a soldier in the given cell if it's empty
        if self.is_user_land(q, r, agent.name) or self.is_adjacent_to_user_land(q, r, agent.name):
            if self.grid.get((q, r)) and not self.grid[(q, r)].content:
                self.grid[(q, r)].content = soldier
                self.grid[(q, r)].owner = agent.name
                self.grid[[q, r]].owner_color = agent.color
    
    def is_user_land(self, q, r, owner):
        return self.grid.get((q, r)) and self.grid[(q, r)].owner == owner
    
    def is_adjacent_to_user_land(self, q, r, owner):
        neighbors = self.get_neighbors(q, r)
        return any(self.grid.get((nq, nr)) and self.grid[(nq, nr)].owner == owner for nq, nr in neighbors)

    def get_neighbors(self, q, r):
        neighbors = []
        for dq, dr in self.DIRECTIONS:
            neighbor = (q + dq, r + dr)
            if neighbor in self.grid:
                neighbors.append(neighbor)
        return neighbors
    
    def move_or_place_soldier(self, from_, to_, owner):
        from_q, from_r = from_
        to_q, to_r = to_
        from_cell = self.grid.get((from_q, from_r))
        to_cell = self.grid.get((to_q, to_r))

        # Ensure both cells exist
        if not from_cell or not to_cell:
            return False

        # Ensure the 'from' cell has a soldier and belongs to the user
        if from_cell.owner != owner or not isinstance(from_cell.content, Soldier):
            return False

        # Check if the 'to' cell is a valid target
        if (
            (to_q, to_r) in self.get_neighbors(from_q, from_r) and
            (to_cell.owner == owner or to_cell.owner is None or to_cell.owner != owner)
        ):
            # Place the soldier in the target cell
            self.grid[(to_q, to_r)].content = from_cell.content
            self.grid[(to_q, to_r)].owner = owner
            self.grid[(from_q, from_r)].content = None  # Clear the soldier from the original cell
            return True
        return False
    
    def is_point_inside_hex(self, x, y, mouse_pos):
        # Check if the mouse position is inside the hexagon
        px, py = mouse_pos
        return px > x - self.cell_size and px < x + self.cell_size and py > y - self.cell_size and py < y + self.cell_size
    
    def pixel_to_axial(self, x, y):
        # Convert pixel coordinates to axial coordinates
        q = (2/3 * x) / self.cell_size
        r = (-1 / 3 * x + math.sqrt(3) / 3 * y) / self.cell_size
        return round(q), round(r)

    def is_valid_location(self, q, r):
        """Check if a location is valid within the map grid."""
        return (q, r) in self.grid


    def save_map(self, file_path):
        with open(file_path, 'w') as file:
            json.dump({key: cell.to_dict() for key, cell in self.grid.items()}, file)

    def load_map(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.grid = {tuple(map(int, k.split(','))): HexCell.from_dict(v) for k, v in data.items()}

# Game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    hex_map = HexMap(map_size=10, cell_size=20)

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            hex_map.handle_events(event)

        hex_map.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
