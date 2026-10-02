# src/entidades/jugador.py
import pygame
from config import (
    RADIO_CUERPO,
    LARGO_BRAZO,
    LARGO_ANTEBRAZO,
    FUERZA_JALON,
    FRICCION,
    ROJO_TORSO,
    PIEL_BRAZO,
    BLANCO_MANO,
    VERDE_ANCLA,
)
from src.fisicas.traccion import calcular_posicion_codo, calcular_fuerza_traccion


class Jugador:
    def __init__(self, x: float, y: float):
        # Posición y física del cuerpo
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)

        # Extremidad (Hombro, Codo, Mano)
        self.pos_mano = pygame.Vector2(x, y)
        self.pos_codo = pygame.Vector2(x, y)
        self.pos_ancla = None  # Coordenada fija cuando la mano se clava en el suelo

        # Estados
        self.mano_clavada = False

    def procesar_eventos(self, evento: pygame.event.Event, pos_mouse: tuple):
        """Maneja el clic del mouse para clavar o soltar la mano."""
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            # Clavar la mano en la posición actual donde está la mano
            self.mano_clavada = True
            self.pos_ancla = pygame.Vector2(self.pos_mano)

        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            # Soltar la mano del suelo
            self.mano_clavada = False
            self.pos_ancla = None

    def actualizar(self, pos_mouse: tuple):
        """Actualiza el movimiento, la posición del brazo y las fuerzas."""
        mouse_vec = pygame.Vector2(pos_mouse)

        if not self.mano_clavada:
            # ESTADO LIBRE: La mano sigue al mouse (respetando el alcance)
            self.pos_codo, self.pos_mano = calcular_posicion_codo(
                self.pos, mouse_vec, LARGO_BRAZO, LARGO_ANTEBRAZO
            )
        else:
            # ESTADO CLAVADO: La mano se queda fija en el suelo
            self.pos_mano = pygame.Vector2(self.pos_ancla)
            self.pos_codo, self.pos_mano = calcular_posicion_codo(
                self.pos, self.pos_mano, LARGO_BRAZO, LARGO_ANTEBRAZO
            )

            # Calcular tracción: Si mueves el mouse lejos del ancla o jalas
            fuerza = calcular_fuerza_traccion(self.pos, self.pos_ancla, FUERZA_JALON)
            self.vel += fuerza

        # Aplicar físicas al cuerpo
        self.pos += self.vel
        self.vel *= FRICCION  # Desaceleración por rozamiento con el suelo

    def dibujar(self, superficie: pygame.Surface):
        """Dibuja el torso, la articulación del brazo (hombro-codo-mano) y el indicador de ancla."""
        # 1. Dibujar el Brazo (Hombro -> Codo -> Mano)
        pygame.draw.line(
            superficie, PIEL_BRAZO, self.pos, self.pos_codo, 6
        )  # Hombro a Codo
        pygame.draw.line(
            superficie, PIEL_BRAZO, self.pos_codo, self.pos_mano, 5
        )  # Codo a Mano

        # Articulación del codo
        pygame.draw.circle(
            superficie, PIEL_BRAZO, (int(self.pos_codo.x), int(self.pos_codo.y)), 4
        )

        # 2. Dibujar la Mano
        color_mano = VERDE_ANCLA if self.mano_clavada else BLANCO_MANO
        pygame.draw.circle(
            superficie, color_mano, (int(self.pos_mano.x), int(self.pos_mano.y)), 6
        )

        # 3. Dibujar el Cuerpo (Torso)
        pygame.draw.circle(
            superficie, ROJO_TORSO, (int(self.pos.x), int(self.pos.y)), RADIO_CUERPO
        )
