# Modulo: mapa.py

"""Superficies y obstáculos para ensayar agarres y colisiones."""

from dataclasses import dataclass, field

import pygame
from configuracion import ALTO, ANCHO, RADIO_TORSO


@dataclass
class MapaPrueba:
    ancho: int = ANCHO
    alto: int = ALTO
    muros: list[pygame.Rect] = field(
        default_factory=lambda: [
            pygame.Rect(430, 145, 42, 350),
            pygame.Rect(665, 300, 110, 42),
        ]
    )

    def cuerpo_valido(self, punto: pygame.Vector2, radio: float = RADIO_TORSO) -> bool:
        if not (radio <= punto.x <= self.ancho - radio):
            return False
        if not (radio <= punto.y <= self.alto - radio):
            return False
        # Distancia desde el centro hasta el punto más próximo de cada muro.
        for muro in self.muros:
            x_cercana = max(muro.left, min(punto.x, muro.right))
            y_cercana = max(muro.top, min(punto.y, muro.bottom))
            if (punto.x - x_cercana) ** 2 + (punto.y - y_cercana) ** 2 < radio**2:
                return False
        return True

    def puede_agarrar(self, torso: pygame.Vector2, mano: pygame.Vector2) -> bool:
        if not (0 <= mano.x < self.ancho and 0 <= mano.y < self.alto):
            return False
        for muro in self.muros:
            if muro.collidepoint(mano.x, mano.y):
                return False
            # No permitir sujetarse a suelo detrás de una pared.
            if muro.clipline(torso.x, torso.y, mano.x, mano.y):
                return False
        return True
