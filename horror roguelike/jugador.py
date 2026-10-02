# Modulo: jugador.py

"""Datos del torso y desplazamiento sujeto a colisiones."""

from dataclasses import dataclass, field

import pygame
from configuracion import RADIO_TORSO
from mapa import MapaPrueba


@dataclass
class Jugador:
    posicion: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(170, 320))
    radio: float = RADIO_TORSO

    def mover_hacia(
        self, destino: pygame.Vector2, distancia: float, mapa: MapaPrueba
    ) -> float:
        """Acerca el cuerpo al destino; devuelve la distancia recorrida realmente."""
        desplazamiento = destino - self.posicion
        if distancia <= 0 or desplazamiento.length_squared() == 0:
            return 0.0
        direccion = desplazamiento.normalize()
        restante = min(distancia, desplazamiento.length())
        anterior = self.posicion.copy()

        # Subpasos para impedir que un tirón rápido atraviese paredes estrechas.
        while restante > 1e-6:
            paso = min(restante, 2.0)
            propuesta_x = self.posicion + pygame.Vector2(direccion.x * paso, 0)
            if mapa.cuerpo_valido(propuesta_x, self.radio):
                self.posicion.x = propuesta_x.x
            propuesta_y = self.posicion + pygame.Vector2(0, direccion.y * paso)
            if mapa.cuerpo_valido(propuesta_y, self.radio):
                self.posicion.y = propuesta_y.y
            restante -= paso

        return self.posicion.distance_to(anterior)
