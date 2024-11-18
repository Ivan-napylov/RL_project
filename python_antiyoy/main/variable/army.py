import pygame

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
        return {'type': 'soldier', 'level': self.text}

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
    
    def define_type(self, text: str):
        color = (100, 0, 255)
        if text[-1] == '1':
            color = (100, 0, 255)
        elif text[-1] == '2':
            color = (0, 200, 255)
        elif text[-1] == '3':
            color = (150, 255, 255)
        return color

class Army(Button):
    def __init__(self, x, y, width, height, color, text):
        super().__init__(x, y, width, height, color, text)

        self.soldiers = []

    def draw_entities(self, screen, entities):
        for pos, level in entities:
            soldier = pygame.draw.circle(screen, self.define_type(level), pos, 5, 5)
            self.soldiers.append(soldier)

    def change_pos(self, pos):
        for soldier in self.soldiers:
            if soldier.collidepoint(pos):
                pass

class Barrier(Button):
    def __init__(self, x, y, width, height, color, text):
        super().__init__(x, y, width, height, color, text)
        

    
