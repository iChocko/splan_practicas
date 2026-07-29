"""
core.config — Lectura de configuración y tokens.

INFRAESTRUCTURA COMÚN. No la modifiquen sin avisar.

Los tokens NO se escriben en el código. Viven en un archivo `.env` que
cada quien tiene en su computadora y que Git ignora (ver `.gitignore`).

Si este módulo les grita "falta el token", el problema está en su `.env`,
no en el código.
"""

from __future__ import annotations

import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO_ENV = RAIZ / ".env"
RUTA_BD = RAIZ / "datos" / "inegi.db"


class ErrorConfig(Exception):
    """Falta configuración o está mal escrita."""


def _cargar_env() -> dict[str, str]:
    """Lee el archivo .env y devuelve sus variables como diccionario."""
    if not ARCHIVO_ENV.exists():
        raise ErrorConfig(
            f"No encontré el archivo .env en {ARCHIVO_ENV}\n"
            f"Copia .env.example como .env y escribe ahí tu token."
        )

    variables: dict[str, str] = {}
    for linea in ARCHIVO_ENV.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        variables[clave.strip()] = valor.strip().strip('"').strip("'")
    return variables


def obtener_token(nombre: str) -> str:
    """
    Devuelve el token guardado bajo `nombre` en el archivo .env.

    Nombres esperados:
      - TOKEN_DENUE        (para la API del DENUE)
      - TOKEN_INDICADORES  (para la API de Indicadores / BIE)

    Hoy el INEGI entrega un mismo token para ambas APIs, así que lo más
    probable es que las dos variables tengan el mismo valor. Están separadas
    a propósito: si el INEGI vuelve a emitir tokens distintos por API, se
    cambia el .env y no el código.
    """
    variables = _cargar_env()
    # Permitimos también variables de entorno del sistema, por si acaso.
    valor = variables.get(nombre) or os.environ.get(nombre, "")

    if not valor or valor.startswith("pega-aqui"):
        raise ErrorConfig(
            f"La variable {nombre} está vacía en tu .env\n"
            f"Consíguela en https://www.inegi.org.mx/servicios/ y pégala ahí."
        )
    return valor


def ruta_base_datos() -> Path:
    """Devuelve la ruta al archivo SQLite, creando la carpeta si hace falta."""
    RUTA_BD.parent.mkdir(parents=True, exist_ok=True)
    return RUTA_BD
