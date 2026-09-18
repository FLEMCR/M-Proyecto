import sys

import pygame
from pygame.locals import *

pygame.init()

pantalla = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Mi primer juego")

verde = (130, 200, 0)

pantalla.fill("green")
fondo = pygame.draw.rect(pantalla, verde, (50, 50, 400, 300))
serpiente = pygame.draw.line(pantalla, "blue", (100, 104), (199, 104), 20)
print(serpiente)


# bucle de ventana
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
