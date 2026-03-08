import pygame
import sys
import numpy as np

class Raster:
    
    @staticmethod
    def linea_dummy(x1, y1, x2, y2, img):
        a = y2-y1
        b = x1-x2
        c = x2*y1-x1*y2
        inicio_x = min(x1, x2)
        fin_x = max(x1, x2)
        inicio_y = min(y1, y2)
        fin_y = max(y1, y2)
        
        for x in range(inicio_x, fin_x+1):
            for y in range(inicio_y, fin_y+1):
                f = a*x + b*y + c
                if abs(f)<=1e-2:
                    img[y,x] = 1
        return img
    
    @staticmethod
    def linea_DDA(x1, y1, x2, y2, img):
        dx = x2-x1
        dy = y2-y1
        pasos = max(abs(dx), abs(dy))
        incr_x = dx/pasos
        incr_y = dy/pasos
        x = x1
        y = y1
        for i in range(pasos):
            x+=incr_x
            y+=incr_y
            img[round(y), round(x)]=1
        return img
    
    @staticmethod
    def linea_bresenham(x1, y1, x2, y2, img):
        dx = abs(x2-x1)
        dy = abs(y2-y1)
        x, y = x1, y1
        incr_x = 1 if x2>x1 else -1
        incr_y = 1 if y2>y1 else -1
        
        if dx>dy:
            p = 2*dy - dx
            for i in range(dx):
                img[y, x]=1
                x+=incr_x
                p+= 2*dy
                if p>=0:
                    p-=2*dx
                    y+=incr_y
        else:
            p = 2*dx-dy
            for i in range(dy):
                img[y, x] = 1
                y+=incr_y
                p+=2*dx
                if p>=0:
                    p-=2*dy
                    x+=incr_x
        return img

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
        
        self.x1 = 3
        self.y1 = 4
        

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
                self.dibujar_linea(x, y)

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
        
    def dibujar_linea(self, x2, y2):
        self.img.fill(0)
        self.canvas.fill(self.WHITE)
        self.draw_grid()
        pygame.draw.rect(
            self.canvas,
            self.BLACK,
            (self.x1*self.CELL, self.y1*self.CELL, self.CELL, self.CELL)
        )
        self.img = Raster.linea_bresenham(self.x1, self.y1, 
                                    x2, 
                                    y2, 
                                    self.img)
        coords_y, coords_x = np.where(self.img==1)
        for y, x in zip(coords_y, coords_x):
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