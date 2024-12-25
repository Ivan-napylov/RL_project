import pygame
from reward import CoinSystem

class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont(None, 30)
        self.active = False
        self.level = -1
        self.levels = ["Level 1", "Level 2", "Level 3"]
        self.init_text = text

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update(self):
        # Cycle through soldier levels
        self.level = (self.level + 1) % len(self.levels)
        self.text = self.levels[self.level]
        return {'type': 'soldier', 'level': self.level + 1}

    def update_color(self):
        # Update button color based on state
        self.color = (0, 255, 0) if self.level != -1 else (255, 0, 0)

    def draw(self, screen):
        # Draw the button
        self.update_color()
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    @staticmethod
    def get_color_for_level(level):
        # Return color based on level
        level_colors = {
            1: (100, 0, 255),
            2: (0, 200, 255),
            3: (150, 255, 255)
        }
        return level_colors.get(level, (100, 0, 255))  # Default to Level 1 color

class Soldier:
    def __init__(self, level=1, owner=None):
        self.level = level
        self.health = 50 + (level * 10)
        self.attack = 10 + (level * 2)
        self.cost = 10 * level  # Cost increases with soldier level
        self.owner = owner
        self.color = self.get_color_for_level(level)

    def upgrade(self):
        # Upgrade soldier stats
        self.level += 1
        self.health += 10
        self.attack += 2
        self.cost = 10 * self.level
    
    def get_color_for_level(self, level):
        # Return color based on level
        level_colors = {
            1: (100, 0, 255),
            2: (0, 200, 255),
            3: (150, 255, 255)
        }
        return level_colors.get(level, (100, 0, 255))  # Default to Level 1 color

class Army(Button):
    def __init__(self, x, y, width, height, color, label, coin_system):
        super().__init__(x, y, width, height, color, text=label)  # Pass label as text
        self.soldiers = []
        self.coin_system = coin_system

    def draw_soldiers(self, screen):
        # Draw soldiers as circles
        for soldier in self.soldiers:
            position = (100 + soldier.level * 20, 100)  # Example position calculation
            color = self.get_color_for_level(soldier.level)
            pygame.draw.circle(screen, color, position, 10)

    def add_soldier(self, level):
        # Buy and add a soldier to the army
        soldier = Soldier(level)
        if self.coin_system.spend(soldier.cost):
            self.soldiers.append(soldier)

    def upgrade_soldier(self, index):
        # Upgrade a specific soldier
        if 0 <= index < len(self.soldiers):
            if self.coin_system.spend(self.soldiers[index].cost):
                self.soldiers[index].upgrade()
                return True
        return False

    def get_balance(self):
        return self.coin_system.get_balance()

    def draw(self, screen):
        # Draw both button and soldiers
        super().draw(screen)
        # self.draw_soldiers(screen)
