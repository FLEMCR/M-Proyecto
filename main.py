# Modulo: main.py
import pygame

import config

# ---------- CONFIGURACIÓN INICIAL ----------
pygame.init()
pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
pygame.display.set_caption("PYPENE")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Arial", 20)  # Para mostrar texto (ej. FPS)

# ---------- ESTADO DEL JUEGO ----------
funcionando = True
dt = 0  # delta time: segundos desde el frame anterior

# El jugador es un círculo. Vector2 es cómodo para posiciones y velocidades
jugador_pos = pygame.Vector2(config.ANCHO / 2, config.ALTO / 2)
jugador_radio = 45
jugador_color = "red"
jugador_velocidad = 500  # píxeles por segundo

# ---------- BUCLE PRINCIPAL ----------
while funcionando:
    # 1) EVENTOS (cosas puntuales: cerrar, clics, teclas presionadas una vez)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            funcionando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                funcionando = False
            if evento.key == pygame.K_SPACE:
                print("¡Saltaste!")

    # 2) ENTRADA CONTINUA (mantener teclas pulsadas)
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        jugador_pos.y -= jugador_velocidad * dt
    if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        jugador_pos.y += jugador_velocidad * dt
    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        jugador_pos.x -= jugador_velocidad * dt
    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        jugador_pos.x += jugador_velocidad * dt

    # Limitar al jugador dentro de la pantalla
    jugador_pos.x = max(jugador_radio, min(config.ANCHO - jugador_radio, jugador_pos.x))
    jugador_pos.y = max(jugador_radio, min(config.ALTO - jugador_radio, jugador_pos.y))

    # 3) DIBUJAR
    pantalla.fill("white")  # borra el frame anterior
    pygame.draw.circle(pantalla, jugador_color, jugador_pos, jugador_radio)

    # Texto con los FPS (útil para depurar)
    texto = fuente.render(f"FPS: {reloj.get_fps():.0f}", True, "black")
    pantalla.blit(texto, (10, 10))

    # 4) MOSTRAR Y ESPERAR
    pygame.display.flip()
    dt = reloj.tick(config.FPS) / 1000  # delta time en segundos

# ---------- SALIR ----------
pygame.quit()
