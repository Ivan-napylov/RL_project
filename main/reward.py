import pygame

class CoinSystem:
    def __init__(self, width, height, margin_bottom = 100, initial_balance=0):
        self.balance = initial_balance
        self.radius = 30
        self.x = width - self.radius - 10
        self.y = self.radius + margin_bottom

    def spend(self, amount):
        # Deduct coins if balance is sufficient
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def update_score(self, action, cell_owner):
        if action == 'capture' and cell_owner is None:
            self.score += 10  # Neutral land
        elif action == 'capture' and cell_owner != 'user':
            self.score += 20  # Enemy land
        elif action == 'loss':
            self.score -= 5  # Lost a soldier

    def get_balance(self):
        return self.balance
    
    def draw(self, screen):
        font = pygame.font.Font(None, 20)
        # need to draw circle to represent coin and amount of coins inside of it
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.radius)
        text_surface = font.render(str(self.balance), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)
