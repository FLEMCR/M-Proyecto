# Proyecto de horror espacial — base de movimiento

Esta carpeta es el microprototipo **M1–M4** del [plan maestro](../PLAN_MAESTRO_30_BLOQUES.md). Todo lo que podemos nombrar libremente está en español: archivos, clases, funciones, pruebas, comentarios y mensajes. Los nombres propios de Python/Pygame (`__name__`, `pygame.Vector2`, `pygame.event.get`, `test_`) se conservan porque forman parte de sus bibliotecas o convenciones.

Todavía no es una misión: figuras simples permiten comprobar el control. El ratón orienta el brazo; clic sostenido apoya la mano en el suelo; arrastrar **hacia el torso** tira del cuerpo. **No hay movimiento WASD.**

## Preparación

Abre una terminal en esta carpeta:

```bash
python -m venv .venv
```

Activa el entorno virtual:

- PowerShell de Windows: `.venv\Scripts\Activate.ps1` (si la política de ejecución lo bloquea, prueba CMD).
- CMD de Windows: `.venv\Scripts\activate.bat`.
- Linux: `source .venv/bin/activate`.

Luego instala y ejecuta:

```bash
python -m pip install -r dependencias.txt
python principal.py
```

Si Windows no reconoce `python`, prueba `py`. No se necesita arte final, servicios ni servidor.

## Controles y prueba manual

- Mover el ratón: orientar la mano 360° dentro del alcance.
- Clic izquierdo sostenido sobre suelo válido: fijar la mano al mundo.
- Arrastrar el ratón **hacia el cuerpo** sin soltar: tirar del torso hacia la mano.
- Soltar clic: liberar ancla; elegir otro punto de apoyo.
- `Esc`: pausa/reanuda y libera el agarre.

La mano azul puede agarrar; la amarilla está anclada; la roja indica agarre inválido. Intenta rodear el muro y alcanzar el círculo verde. La prueba importante es si el movimiento **se siente bien**, no la calidad de las figuras.

## Pruebas automatizadas

```bash
python -m unittest discover -s pruebas -p "test_*.py" -v
```

En Linux, para comprobar el arranque sin abrir una ventana real:

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python principal.py --prueba-arranque
```

Esa prueba de tres cuadros no sustituye jugarlo personalmente.

## Archivos actuales

- `principal.py`: entrada, pausa, dibujo provisional y bucle; no debe acumular inventario o IA.
- `configuracion.py`: parámetros editables del control y colores temporales.
- `jugador.py`: torso y colisiones al moverlo; no lee el ratón.
- `brazo.py`: estados libre/agarrando, alcance, ancla y tracción; no dibuja.
- `mapa.py`: paredes, límites y suelo agarrable.
- `pruebas/test_movimiento.py`: pruebas de reglas sin ventana.
- `dependencias.txt`: biblioteca necesaria.
- `recursos/`: futuros gráficos/sonidos y sus licencias.

**Siguiente hito:** M5. Pruébalo, anota qué se siente extraño y ajusta alcance, velocidad o sensibilidad en `configuracion.py` antes de añadir enemigos, oscuridad o armas. Hay un plan archivo por archivo para la primera misión en la sección G del plan maestro.
