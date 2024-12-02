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
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    
    def update(self):
        self.level += 1
        if self.level == 3:
            self.level = 0
        # return self.soldiers_level[self.level]
        self.text = self.levels[self.level]
        return {'type': 'soldier', 'level': self.level}

    def button_active(self):
        if self.level == -1:
            self.color = (255, 0, 0)
        else:
            self.color = (0, 255, 0)
    
    def draw(self, screen):
        # Draw button
        self.button_active()
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))
    
    def define_type(self, level):
        color = (100, 0, 255)
        if  level == 1: #text[-1] == '1':
            color = (100, 0, 255)
        elif level == 2: #text[-1] == '2':
            color = (0, 200, 255)
        elif level == 3: #text[-1] == '3':
            color = (150, 255, 255)
        return color

class Soldier:
    def __init__(self, level=1):
        self.level = level
        self.health = 50 + (level * 10)  # Example: Each level increases health
        self.attack = 10 + (level * 2)  # Example: Each level increases attack power
        self.cost = 10 * level  # Cost increases with soldier level

    def upgrade(self):
        self.level += 1
        self.health += 10  # Upgrade health
        self.attack += 2   # Upgrade attack
        self.cost = 10 * self.level  # Upgrade cost


class Army(Button):
    def __init__(self, x, y, width, height, color, text):
        super().__init__(x, y, width, height, color, text)

        self.soldiers = []
        self.coin_system = CoinSystem(initial_balance=0)

    def draw_entities(self, screen, entities):
        for pos, level in entities:
            soldier = pygame.draw.circle(screen, self.define_type(level), pos, 5, 5)
            self.soldiers.append(soldier)

    def change_pos(self, pos):
        for soldier in self.soldiers:
            if soldier.collidepoint(pos):
                pass
    
    def buy_soldier(self, level):
        soldier = Soldier(level)
        if self.coin_system.spend(soldier.cost):
            self.soldiers.append(soldier)
            return True
        return False

    def upgrade_soldier(self, index):
        if 0 <= index < len(self.soldiers):
            self.soldiers[index].upgrade()
    
    def get_balance(self):
        return self.coin_system.get_balance()
    
    def draw(self, screen):
        for soldier in self.soldiers:
            pygame.draw.circle(screen, self.define_type(soldier.level), (100, 100), 10) 


        

    
