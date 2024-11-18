# Импорт библиотек
import pygame
import random
from HexMap import HexMap
from config.config import *
from variable import army

# Сама игра
class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Antiyoy")

        # Установим расширение экрана и частоту обновления
        self.visota = HEIGHT
        self.shirina = WIDTH
        self.FPS = FPS

        self.HexMap = HexMap(cols=10, rows=10, size=20, screen_width=800, screen_height=300)
        self.army = army.Army(20, 20, 120, 40, (255,0,0), " Army 1")
        self.barrier = army.Barrier(20, 20 + 41 , 120, 40, (255,0,0), "Barrier Level 1")

        # создание игры и окна
        self.screen = pygame.display.set_mode((self.shirina, self.visota))
        self.clock = pygame.time.Clock()

        # self.HexMap.run()
    
    def run(self):
        running = True
        clock = pygame.time.Clock()
        content = None
        while running:

            self.screen.fill((0, 0, 0))
            soldiers = self.HexMap.draw_map()
            self.army.draw(self.screen)
            self.barrier.draw(self.screen)
            
            self.army.draw_entities(self.screen, soldiers)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.army.is_clicked(event.pos):
                            content = self.army.update()
                            # print(content)
                        if self.HexMap.is_clicked(event, content):
                            content = None
                            self.army.level = -1

                    # if event.button == 3:  
                    #     self.camera.start_drag(event.pos) 

                self.HexMap.handle_events(event)
            pygame.display.flip()
            clock.tick(30)  # Обновление 30 раз в секунду
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()