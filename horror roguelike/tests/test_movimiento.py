"""Pruebas de movimiento; no necesitan abrir una ventana."""

import unittest

import pygame

from brazo import Brazo, EstadoMano
from jugador import Jugador
from mapa import MapaPrueba


class PruebasBrazo(unittest.TestCase):
    def setUp(self):
        self.mapa = MapaPrueba()
        self.jugador = Jugador(pygame.Vector2(170, 320))
        self.brazo = Brazo()

    def test_mano_limitada_en_todas_las_direcciones(self):
        for cursor in ((2000, 320), (-1000, 320), (170, -1000), (170, 2000)):
            mano = self.brazo.posicion_mano(self.jugador.posicion, pygame.Vector2(cursor))
            self.assertAlmostEqual(self.jugador.posicion.distance_to(mano), self.brazo.alcance)

    def test_clic_sin_arrastrar_no_mueve(self):
        self.assertTrue(self.brazo.intentar_agarrar(self.jugador, pygame.Vector2(265, 320), self.mapa))
        anterior = self.jugador.posicion.copy()
        self.brazo.tirar(self.jugador, pygame.Vector2(), 1 / 60, self.mapa)
        self.assertEqual(anterior, self.jugador.posicion)

    def test_arrastrar_hacia_torso_acerca_al_ancla(self):
        self.assertTrue(self.brazo.intentar_agarrar(self.jugador, pygame.Vector2(265, 320), self.mapa))
        ancla = self.brazo.ancla.copy()
        x_inicial = self.jugador.posicion.x
        distancia = self.brazo.tirar(self.jugador, pygame.Vector2(-30, 0), 1 / 60, self.mapa)
        self.assertGreater(distancia, 0)
        self.assertGreater(self.jugador.posicion.x, x_inicial)
        self.assertEqual(self.brazo.ancla, ancla)

    def test_arrastrar_en_sentido_contrario_no_impulsa(self):
        self.brazo.intentar_agarrar(self.jugador, pygame.Vector2(265, 320), self.mapa)
        distancia = self.brazo.tirar(self.jugador, pygame.Vector2(30, 0), 1 / 60, self.mapa)
        self.assertEqual(distancia, 0)

    def test_soltar_restaurar_estado_y_cancelar_tiron(self):
        self.brazo.intentar_agarrar(self.jugador, pygame.Vector2(265, 320), self.mapa)
        self.brazo.tirar(self.jugador, pygame.Vector2(-30, 0), 1 / 60, self.mapa)
        self.brazo.soltar()
        self.assertEqual(self.brazo.estado, EstadoMano.LIBRE)
        self.assertIsNone(self.brazo.ancla)
        self.assertEqual(self.brazo.tiron_pendiente, 0)
        anterior = self.jugador.posicion.copy()
        self.brazo.tirar(self.jugador, pygame.Vector2(-30, 0), 1 / 60, self.mapa)
        self.assertEqual(anterior, self.jugador.posicion)

    def test_muro_impide_agarrar_detras(self):
        self.jugador.posicion = pygame.Vector2(380, 320)
        self.assertFalse(self.brazo.intentar_agarrar(self.jugador, pygame.Vector2(482, 320), self.mapa))
        self.assertIsNone(self.brazo.ancla)

    def test_muro_detiene_tiron_grande(self):
        self.jugador.posicion = pygame.Vector2(360, 320)
        self.brazo.intentar_agarrar(self.jugador, pygame.Vector2(412, 320), self.mapa)
        for _ in range(60):
            self.brazo.tirar(self.jugador, pygame.Vector2(-200, 0), 1 / 60, self.mapa)
        self.assertLessEqual(self.jugador.posicion.x + self.jugador.radio, 430)

    def test_no_agarrar_muro_ni_fuera_de_mapa(self):
        self.assertFalse(self.mapa.puede_agarrar(self.jugador.posicion, pygame.Vector2(450, 320)))
        self.assertFalse(self.mapa.puede_agarrar(self.jugador.posicion, pygame.Vector2(-2, 320)))


if __name__ == '__main__':
    unittest.main()
