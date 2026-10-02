import sys

import pygame
from pygame.locals import *

pygame.init()

icono = pygame.image.load("pruebas/imagenes/icono.png")
fondo = pygame.image.load("pruebas/imagenes/fondo.jpeg")
pantalla = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Diyenguel")
pygame.display.set_icon(icono)


pantalla.fill("white")


# bucle de ventana
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
