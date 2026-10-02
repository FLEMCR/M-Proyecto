# config.py

# Pantalla
ANCHO = 1000
ALTO = 700
FPS = 60

# Colores (RGB)
NEGRO = (15, 15, 18)
ROJO_TORSO = (180, 40, 40)
PIEL_BRAZO = (200, 150, 120)
BLANCO_MANO = (230, 230, 230)
VERDE_ANCLA = (50, 205, 50)

# Parámetros del Jugador y Brazo
RADIO_CUERPO = 20
LARGO_BRAZO = 35  # Longitud del Hombro al Codo (L1)
LARGO_ANTEBRAZO = 35  # Longitud del Codo a la Mano (L2)

# Físicas de Tracción
FUERZA_JALON = 0.8  # Multiplicador de fuerza al jalar
FRICCION = 0.92  # Fricción del suelo (1.0 = sin fricción, 0.0 = freno instantáneo)
MASA_JUGADOR = 1.0
