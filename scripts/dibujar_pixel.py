import pygame
import sys
import numpy as np

class GridPaint:
    def __init__(self, N=40, cell=15):
        pygame.init()

        self.N = N
        self.CELL = cell
        self.WIDTH = self.HEIGHT = N * cell

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY  = (220, 220, 220)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Paint")

        # Lienzo 
        self.canvas = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.canvas.fill(self.WHITE)

        # Imagen / matriz
        self.img = np.zeros((N, N))

        self.clock = pygame.time.Clock()
        self.drawing = False

        self.draw_grid()

    def draw_grid(self):
        for i in range(self.N + 1):
            pygame.draw.line(
                self.canvas, self.GRAY,
                (i*self.CELL, 0), (i*self.CELL, self.HEIGHT)
            )
            pygame.draw.line(
                self.canvas, self.GRAY,
                (0, i*self.CELL), (self.WIDTH, i*self.CELL)
            )

    def handle_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.drawing = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.drawing = False

        if event.type == pygame.MOUSEMOTION and self.drawing:
            mx, my = event.pos
            x = mx // self.CELL
            y = my // self.CELL

            if 0 <= x < self.N and 0 <= y < self.N:
                self.draw_pixel(x, y)

    def draw_pixel(self, x, y):
        """Dibuja un pixel en la cuadrícula y en la matriz"""
        self.img.fill(0)
        self.canvas.fill(self.WHITE)
        self.draw_grid()
        self.img[y, x] = 1
        pygame.draw.rect(
            self.canvas,
            self.BLACK,
            (x*self.CELL, y*self.CELL, self.CELL, self.CELL)
        )
        self.draw_grid()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_mouse(event)

            self.screen.blit(self.canvas, (0, 0))
            pygame.display.update()
            self.clock.tick(120)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = GridPaint(N=50, cell=12)
    app.run()