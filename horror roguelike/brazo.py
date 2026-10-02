# Modulo: brazo.py

"""Brazo libre o anclado: el arrastre del ratón tira del torso."""

from dataclasses import dataclass
from enum import Enum, auto

import pygame
from configuracion import (
    ALCANCE_BRAZO,
    DISTANCIA_MINIMA_ANCLA,
    SENSIBILIDAD_ARRASTRE,
    VELOCIDAD_MAXIMA_ARRASTRE,
)
from jugador import Jugador
from mapa import MapaPrueba


class EstadoMano(Enum):
    LIBRE = auto()
    AGARRADO_SUELO = auto()


@dataclass
class Brazo:
    alcance: float = ALCANCE_BRAZO
    sensibilidad: float = SENSIBILIDAD_ARRASTRE
    velocidad_maxima: float = VELOCIDAD_MAXIMA_ARRASTRE
    distancia_minima: float = DISTANCIA_MINIMA_ANCLA
    estado: EstadoMano = EstadoMano.LIBRE
    ancla: pygame.Vector2 | None = None
    tiron_pendiente: float = 0.0

    def posicion_mano(
        self, torso: pygame.Vector2, cursor: pygame.Vector2
    ) -> pygame.Vector2:
        if self.ancla is not None:
            return self.ancla.copy()
        desplazamiento = cursor - torso
        if desplazamiento.length_squared() > self.alcance**2:
            desplazamiento.scale_to_length(self.alcance)
        return torso + desplazamiento

    def intentar_agarrar(
        self, jugador: Jugador, cursor: pygame.Vector2, mapa: MapaPrueba
    ) -> bool:
        if self.estado is not EstadoMano.LIBRE:
            return False
        mano = self.posicion_mano(jugador.posicion, cursor)
        if not mapa.puede_agarrar(jugador.posicion, mano):
            return False
        self.ancla = mano.copy()  # Coordenadas del mundo, no de una cámara.
        self.tiron_pendiente = 0.0
        self.estado = EstadoMano.AGARRADO_SUELO
        return True

    def soltar(self) -> None:
        self.estado = EstadoMano.LIBRE
        self.ancla = None
        self.tiron_pendiente = 0.0

    def tirar(
        self,
        jugador: Jugador,
        delta_raton: pygame.Vector2,
        tiempo: float,
        mapa: MapaPrueba,
    ) -> float:
        """El ratón retrocede hacia el torso y el torso se acerca al ancla."""
        if (
            self.estado is not EstadoMano.AGARRADO_SUELO
            or self.ancla is None
            or tiempo <= 0
        ):
            return 0.0
        hacia_ancla = self.ancla - jugador.posicion
        distancia_ancla = hacia_ancla.length()
        if distancia_ancla <= self.distancia_minima:
            self.tiron_pendiente = 0.0
            return 0.0
        direccion = hacia_ancla / distancia_ancla
        impulso = (-delta_raton).dot(direccion) * self.sensibilidad
        if impulso < 0:
            # Alejar el ratón del torso no produce desplazamiento gratuito.
            self.tiron_pendiente = 0.0
        else:
            self.tiron_pendiente = min(self.alcance, self.tiron_pendiente + impulso)
        avance_permitido = min(
            self.tiron_pendiente,
            self.velocidad_maxima * tiempo,
            distancia_ancla - self.distancia_minima,
        )
        recorrido = jugador.mover_hacia(self.ancla, avance_permitido, mapa)
        self.tiron_pendiente = max(0.0, self.tiron_pendiente - recorrido)
        if recorrido < avance_permitido - 0.05:
            # Evita acumular tirones si una pared detuvo al personaje.
            self.tiron_pendiente = 0.0
        return recorrido
