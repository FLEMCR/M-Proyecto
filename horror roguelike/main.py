# Modulo: main.py

"""Microprototipo M1–M4: torso arrastrado mediante un solo brazo."""

import argparse
import math

import configuracion as ajustes
import pygame
from brazo import Brazo, EstadoMano
from jugador import Jugador
from mapa import MapaPrueba


def dibujar(
    pantalla: pygame.Surface,
    fuente: pygame.font.Font,
    jugador: Jugador,
    brazo: Brazo,
    mapa: MapaPrueba,
    en_pausa: bool,
    llegada: bool,
) -> None:
    pantalla.fill(ajustes.COLOR_FONDO)
    for x in range(0, mapa.ancho, 40):
        pygame.draw.line(pantalla, ajustes.COLOR_CUADRICULA, (x, 0), (x, mapa.alto))
    for y in range(0, mapa.alto, 40):
        pygame.draw.line(pantalla, ajustes.COLOR_CUADRICULA, (0, y), (mapa.ancho, y))
    for muro in mapa.muros:
        pygame.draw.rect(pantalla, ajustes.COLOR_MURO, muro)

    # Círculo de prueba; aún no representa la misión final.
    pygame.draw.circle(pantalla, (110, 168, 114), (830, 535), 35, width=2)
    pygame.draw.circle(pantalla, (110, 168, 114), (830, 535), 5)

    cursor = pygame.Vector2(pygame.mouse.get_pos())
    mano = brazo.posicion_mano(jugador.posicion, cursor)
    agarre_valido = (
        mapa.puede_agarrar(jugador.posicion, mano)
        if brazo.estado is EstadoMano.LIBRE
        else True
    )
    color_mano = (
        ajustes.COLOR_ANCLA
        if brazo.estado is EstadoMano.AGARRADO_SUELO
        else (
            ajustes.COLOR_MANO_LIBRE if agarre_valido else ajustes.COLOR_AGARRE_INVALIDO
        )
    )
    pygame.draw.circle(pantalla, ajustes.COLOR_TORSO, jugador.posicion, jugador.radio)
    # --- CÁLCULO DEL CODO (Cinemática Inversa) ---
    desplazamiento = mano - jugador.posicion
    d = desplazamiento.length()

    if d > 0:
        # Si el brazo está completamente estirado (o si hubo un error de redondeo)
        if d >= ajustes.ALCANCE_BRAZO:
            codo = (
                jugador.posicion + desplazamiento.normalize() * ajustes.LONGITUD_BRAZO
            )
        else:
            # Ley de cosenos para encontrar la posición del codo
            a = (ajustes.LONGITUD_BRAZO**2 - ajustes.LONGITUD_ANTEBRAZO**2 + d**2) / (
                2 * d
            )
            h = math.sqrt(max(0, ajustes.LONGITUD_BRAZO**2 - a**2))

            dir_n = desplazamiento.normalize()
            perp = pygame.Vector2(-dir_n.y, dir_n.x)  # Vector perpendicular

            # Sumamos la distancia 'a' en la dirección de la mano, y 'h' hacia un lado
            codo = jugador.posicion + (dir_n * a) + (perp * h)
    else:
        # Si la mano y el torso están exactamente en el mismo píxel
        codo = jugador.posicion + pygame.Vector2(ajustes.LONGITUD_BRAZO, 0)

    # --- DIBUJAR BRAZO Y ANTEBRAZO ---
    pygame.draw.circle(pantalla, ajustes.COLOR_TORSO, jugador.posicion, jugador.radio)

    # Línea del hombro al codo (Brazo)
    pygame.draw.line(pantalla, ajustes.COLOR_BRAZO, jugador.posicion, codo, width=6)
    # Línea del codo a la mano (Antebrazo)
    pygame.draw.line(pantalla, ajustes.COLOR_BRAZO, codo, mano, width=4)
    # Pequeño círculo para marcar la articulación del codo
    pygame.draw.circle(pantalla, ajustes.COLOR_BRAZO, codo, 4)

    pygame.draw.circle(
        pantalla, color_mano, mano, 7
    )  # --- CÁLCULO DEL CODO (Cinemática Inversa) ---
    desplazamiento = mano - jugador.posicion
    d = desplazamiento.length()

    if d > 0:
        # Si el brazo está completamente estirado (o si hubo un error de redondeo)
        if d >= ajustes.ALCANCE_BRAZO:
            codo = (
                jugador.posicion + desplazamiento.normalize() * ajustes.LONGITUD_BRAZO
            )
        else:
            # Ley de cosenos para encontrar la posición del codo
            a = (ajustes.LONGITUD_BRAZO**2 - ajustes.LONGITUD_ANTEBRAZO**2 + d**2) / (
                2 * d
            )
            h = math.sqrt(max(0, ajustes.LONGITUD_BRAZO**2 - a**2))

            dir_n = desplazamiento.normalize()
            perp = pygame.Vector2(-dir_n.y, dir_n.x)  # Vector perpendicular

            # Sumamos la distancia 'a' en la dirección de la mano, y 'h' hacia un lado
            codo = jugador.posicion + (dir_n * a) + (perp * h)
    else:
        # Si la mano y el torso están exactamente en el mismo píxel
        codo = jugador.posicion + pygame.Vector2(ajustes.LONGITUD_BRAZO, 0)

    # --- DIBUJAR BRAZO Y ANTEBRAZO ---
    pygame.draw.circle(pantalla, ajustes.COLOR_TORSO, jugador.posicion, jugador.radio)

    # Línea del hombro al codo (Brazo)
    pygame.draw.line(pantalla, ajustes.COLOR_BRAZO, jugador.posicion, codo, width=6)
    # Línea del codo a la mano (Antebrazo)
    pygame.draw.line(pantalla, ajustes.COLOR_BRAZO, codo, mano, width=4)
    # Pequeño círculo para marcar la articulación del codo
    pygame.draw.circle(pantalla, ajustes.COLOR_BRAZO, codo, 4)

    pygame.draw.circle(pantalla, color_mano, mano, 7)
    pygame.draw.circle(pantalla, color_mano, mano, 7)
    if brazo.estado is EstadoMano.AGARRADO_SUELO:
        pygame.draw.circle(pantalla, ajustes.COLOR_ANCLA, mano, 13, width=2)

    mensajes = [
        "RATÓN: orientar brazo | CLIC SOSTENIDO + arrastrar HACIA el torso: tirar",
        "SOLTAR clic: nuevo agarre | ESC: pausa/reanuda | Sin movimiento WASD",
        f"Mano: {brazo.estado.name} | Torso: ({jugador.posicion.x:.0f}, {jugador.posicion.y:.0f})",
        "Prueba: llega al círculo verde rodeando el muro.",
    ]
    if llegada:
        mensajes.append("¡Llegaste! Ahora comprueba si el control se siente bien.")
    if en_pausa:
        mensajes.append("PAUSA: se liberó el agarre. Pulsa ESC para continuar.")
    for indice, mensaje in enumerate(mensajes):
        texto = fuente.render(mensaje, True, ajustes.COLOR_TEXTO)
        pantalla.blit(texto, (12, 10 + indice * 24))
    pygame.display.flip()


def ejecutar(prueba_arranque: bool = False) -> None:
    pygame.init()
    pantalla = pygame.display.set_mode((ajustes.ANCHO, ajustes.ALTO))
    pygame.display.set_caption("Proyecto de horror espacial — prueba del brazo")
    fuente = pygame.font.Font(None, 23)
    reloj = pygame.time.Clock()
    jugador = Jugador()
    brazo = Brazo()
    mapa = MapaPrueba()
    en_pausa = False
    en_ejecucion = True
    cuadros = 0

    while en_ejecucion:
        tiempo = min(reloj.tick(ajustes.CUADROS_POR_SEGUNDO) / 1000.0, 1.0 / 30.0)
        delta_raton = pygame.Vector2()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_ejecucion = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                en_pausa = not en_pausa
                brazo.soltar()
            elif evento.type == getattr(pygame, "WINDOWFOCUSLOST", None):
                en_pausa = True
                brazo.soltar()
            elif (
                not en_pausa
                and evento.type == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
            ):
                brazo.intentar_agarrar(jugador, pygame.Vector2(evento.pos), mapa)
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                brazo.soltar()
            elif (
                not en_pausa
                and evento.type == pygame.MOUSEMOTION
                and brazo.estado is EstadoMano.AGARRADO_SUELO
            ):
                delta_raton += pygame.Vector2(evento.rel)
        if not en_pausa:
            brazo.tirar(jugador, delta_raton, tiempo, mapa)
        llegada = jugador.posicion.distance_to((830, 535)) < 45
        dibujar(pantalla, fuente, jugador, brazo, mapa, en_pausa, llegada)
        cuadros += 1
        if prueba_arranque and cuadros >= 3:
            en_ejecucion = False
    pygame.quit()


if __name__ == "__main__":
    argumentos = argparse.ArgumentParser(
        description="Prueba del desplazamiento mediante un brazo"
    )
    argumentos.add_argument(
        "--prueba-arranque",
        action="store_true",
        help="cerrar tras tres cuadros para comprobar el inicio",
    )
    opciones = argumentos.parse_args()
    ejecutar(prueba_arranque=opciones.prueba_arranque)
