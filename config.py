# config.py

import json
import os

RUTA_JSON = os.path.join(os.path.dirname(__file__), "configuration.json")

AJUSTES_POR_DEFECTO = {"Width": 800, "Height": 600, "FPS_MAX": 60}

""" --------------------------------------------------------- """


def _crear_si_no_existe():
    if not os.path.exists(RUTA_JSON):
        with open(RUTA_JSON, "w", encoding="utf-8") as f:
            json.dump(AJUSTES_POR_DEFECTO, f, indent=4, ensure_ascii=False)
        print("No se encontró archivo de ajustes. Se creó uno nuevo.")


def cargar():
    _crear_si_no_existe()
    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar(ajustes):
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(ajustes, f, indent=4, ensure_ascii=False)


def resetear():
    guardar(AJUSTES_POR_DEFECTO)


""" --------------------------------------------------------- """
_ajustes = cargar()

ANCHO = _ajustes["Width"]
ALTO = _ajustes["Height"]
FPS = _ajustes["FPS_MAX"]
