# main.py
import sys
import pygame
from config import ANCHO, ALTO, FPS, NEGRO
from src.entidades.jugador import Jugador


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Endoparasite - Prototype Tracción")
    reloj = pygame.time.Clock()

    # Instanciar al jugador en el centro de la pantalla
    jugador = Jugador(ANCHO // 2, ALTO // 2)

    ejecutando = True
    while ejecutando:
        pos_mouse = pygame.mouse.get_pos()

        # 1. Manejo de Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            jugador.procesar_eventos(evento, pos_mouse)

        # 2. Actualización de Lógica
        jugador.actualizar(pos_mouse)

        # 3. Renderizado
        pantalla.fill(NEGRO)
        jugador.dibujar(pantalla)

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
