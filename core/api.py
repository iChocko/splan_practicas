"""
core.api — Cliente HTTP compartido para las APIs del INEGI.

Este módulo es INFRAESTRUCTURA COMÚN. No lo modifiquen sin abrir un issue
y avisar a la otra persona: si una lo cambia, la otra se rompe.

Lo que resuelve por ustedes:
  - reintentos automáticos cuando la API del INEGI falla temporalmente
  - timeouts (para que el programa no se quede colgado para siempre)
  - traducción de errores HTTP a mensajes en español que se entiendan
  - una pausa cortés entre llamadas, para no saturar el servidor del INEGI

Lo que NO resuelve: qué URL construir. Eso es trabajo de cada quien,
en su propio módulo dentro de extract/.
"""

from __future__ import annotations

import time
import json
import urllib.error
import urllib.request


class ErrorAPI(Exception):
    """Se lanza cuando la API del INEGI responde algo que no podemos usar."""


# Pausa entre peticiones consecutivas, en segundos.
# Bajarlo hace el pipeline más rápido y más grosero con el servidor del INEGI.
PAUSA_ENTRE_LLAMADAS = 0.4

TIMEOUT = 60
REINTENTOS = 3


def obtener_json(url: str, *, descripcion: str = "") -> list | dict:
    """
    Hace una petición GET a `url` y devuelve la respuesta ya convertida a
    objetos de Python (listas y diccionarios).

    Parámetros
    ----------
    url : str
        La URL completa, con token incluido.
    descripcion : str
        Texto corto que aparece en los mensajes de error, para saber
        qué llamada falló. Ej: "DENUE municipio 002 sector 46".

    Devuelve
    --------
    list | dict
        Lo que haya respondido la API, ya parseado.

    Lanza
    -----
    ErrorAPI
        Si tras todos los reintentos no se pudo obtener una respuesta válida.
    """
    etiqueta = descripcion or "petición"
    ultimo_error = None

    for intento in range(1, REINTENTOS + 1):
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT) as respuesta:
                crudo = respuesta.read().decode("utf-8")
            time.sleep(PAUSA_ENTRE_LLAMADAS)
            datos = json.loads(crudo)

            # El INEGI a veces responde 200 con una lista de errores adentro.
            if isinstance(datos, list) and datos and isinstance(datos[0], str):
                if datos[0].startswith("ErrorInfo"):
                    raise ErrorAPI(f"[{etiqueta}] El INEGI respondió: {datos}")

            return datos

        except urllib.error.HTTPError as e:
            cuerpo = e.read().decode("utf-8", errors="ignore")[:300]
            if e.code == 400:
                # 400 en el INEGI casi siempre significa: parámetros mal armados
                # o token inválido. Reintentar no lo va a arreglar.
                raise ErrorAPI(
                    f"[{etiqueta}] El INEGI rechazó la petición (HTTP 400). "
                    f"Revisa el token y el orden de los parámetros en la URL.\n"
                    f"Respuesta: {cuerpo}"
                ) from e
            ultimo_error = f"HTTP {e.code}: {cuerpo}"

        except urllib.error.URLError as e:
            ultimo_error = f"No hubo conexión: {e.reason}"

        except json.JSONDecodeError:
            ultimo_error = "La respuesta no era JSON válido"

        if intento < REINTENTOS:
            espera = 2 ** intento
            print(f"  · [{etiqueta}] falló ({ultimo_error}). "
                  f"Reintento {intento + 1}/{REINTENTOS} en {espera}s...")
            time.sleep(espera)

    raise ErrorAPI(f"[{etiqueta}] Falló tras {REINTENTOS} intentos. "
                   f"Último error: {ultimo_error}")
