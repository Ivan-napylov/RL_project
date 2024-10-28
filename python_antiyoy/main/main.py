# Импорт библиотек
import pygame
import random
from HexMap import HexMap


# Сама игра
class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Antiyoy")

        # Установим расширение экрана и частоту обновления
        self.visota = 720
        self.shirina = 1280
        self.FPS = 60

        self.HexMap = HexMap(cols=10, rows=10, size=40, screen_width=800, screen_height=600)

        # создание игры и окна
        self.screen = pygame.display.set_mode((self.shirina, self.visota))
        self.clock = pygame.time.Clock()

        self.HexMap.run()

if __name__ == '__main__':
    game = Game()