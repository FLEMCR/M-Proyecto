# src/fisicas/traccion.py
import math
import pygame


def calcular_posicion_codo(
    hombro: pygame.Vector2, mano: pygame.Vector2, l1: float, l2: float
):
    """
    Calcula la posición (x, y) del codo usando Cinemática Inversa de 2 articulaciones.
    """
    vector_dir = mano - hombro
    distancia = vector_dir.length()

    # Limitar la distancia al alcance máximo del brazo
    alcance_maximo = l1 + l2 - 0.1
    if distancia > alcance_maximo:
        distancia = alcance_maximo
        vector_dir.scale_to_length(alcance_maximo)
        mano = hombro + vector_dir

    if distancia == 0:
        return hombro + pygame.Vector2(0, l1)

    # Teorema del Coseno para calcular el ángulo del codo
    cos_angulo = (l1**2 + distancia**2 - l2**2) / (2 * l1 * distancia)
    cos_angulo = max(-1.0, min(1.0, cos_angulo))  # Asegurar rango [-1, 1]

    angulo_base = math.atan2(vector_dir.y, vector_dir.x)
    angulo_codo = math.acos(cos_angulo)

    # Posición del codo (doblado hacia un lado)
    codo_x = hombro.x + l1 * math.cos(angulo_base - angulo_codo)
    codo_y = hombro.y + l1 * math.sin(angulo_base - angulo_codo)

    return pygame.Vector2(codo_x, codo_y), mano


def calcular_fuerza_traccion(
    pos_cuerpo: pygame.Vector2, pos_ancla: pygame.Vector2, fuerza_mult: float
) -> pygame.Vector2:
    """
    Calcula la aceleración generada cuando el cuerpo jala hacia el punto de anclaje.
    """
    direccion = pos_ancla - pos_cuerpo
    distancia = direccion.length()

    if distancia > 5:  # Si aún no ha llegado al punto de la mano
        direccion.normalize_ip()
        return direccion * (distancia * 0.1) * fuerza_mult

    return pygame.Vector2(0, 0)
