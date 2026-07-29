"""
extract.bie — Capa MACRO del proyecto.

DUEÑA DE ESTE ARCHIVO: Aremy.
Nadie más lo edita. Si alguien más necesita un cambio aquí, te lo pide
por un comentario en el PR o por un issue.

Tu trabajo es llenar los cuerpos de estas funciones. Las FIRMAS NO se
cambian: son parte del contrato de datos.

Lee primero: docs/practica-A-aremy-bie-macro.md
             docs/contrato-de-datos.md
"""

from __future__ import annotations

import pandas as pd

from core.api import obtener_json
from core.config import obtener_token
from core.db import guardar

BASE = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR"

# Áreas geográficas que vas a usar.
NACIONAL = "00"
CAMPECHE = "04"

# La fuente de diseminación en la URL SIEMPRE es "BISE", incluso para series
# del BIE. Escribir "BIE" ahí da un HTTP 400 con el mismo mensaje que un
# token inválido: "No se encontraron resultados". Es un error fácil de
# cometer -confundir el nombre del banco con el parámetro de la URL- y
# cuesta caro depurarlo si no sabes que existe.
FUENTE = "BISE"


def extraer(indicador_id: str, area_geografica: str) -> dict:
    """
    Descarga una serie completa del Banco de Información Económica.

    Parámetros
    ----------
    indicador_id : str
        Clave del indicador en el BIE. Se consigue filtrando el catálogo
        completo (`CL_INDICATOR`) o, si funciona, con el Constructor de
        consultas. La práctica te explica ambos caminos.
    area_geografica : str
        '00' para nacional, '04' para Campeche.

    Devuelve
    --------
    dict
        La respuesta completa del INEGI, sin procesar.

    Notas
    -----
    - La URL lleva este orden de parámetros:
      /INDICATOR/{id}/{idioma}/{area}/{recientes}/{fuente}/{versión}/{token}?type=json
      Un parámetro fuera de lugar da HTTP 400, no un mensaje amable.
    - `fuente` es literalmente el texto `BISE` (ver la constante `FUENTE` de
      este módulo). No es `BIE`, aunque el sistema de donde sale el dato se
      llame así.
    - `recientes` en 'false' trae la serie histórica completa; en 'true'
      trae solo el último dato. Para este proyecto quieres la historia.
    - El campo `COBER_GEO` que viene en cada observación de la respuesta es
      tu comprobante de que el parámetro de área sí filtró lo que pediste:
      debe coincidir con el área que enviaste en la URL.
    """
    # TODO (Aremy): construir la URL y llamar a obtener_json.
    raise NotImplementedError("Etapa 2 de tu práctica")


def transformar_observaciones(
    respuesta: dict, indicador_id: str, area_geografica: str
) -> pd.DataFrame:
    """
    Convierte la respuesta del BIE en un DataFrame que cumple EXACTAMENTE
    el contrato de la tabla `bie_observacion`.

    Columnas que debe tener, ni una más ni una menos:
        indicador_id, area_geografica, periodo, anio, trimestre,
        valor, fecha_extraccion

    Ojo con tres cosas:
      1. Los datos vienen anidados: hay que bajar varios niveles de
         diccionarios y listas antes de encontrar las observaciones.
      2. `periodo` llega como texto y su formato depende de la
         periodicidad de la serie. De ahí salen `anio` y `trimestre`.
         Si la serie no es trimestral, `trimestre` va en None.
      3. Los valores llegan como texto. Un valor vacío no es cero.
    """
    # TODO (Aremy): aplanar la respuesta y devolver el DataFrame.
    raise NotImplementedError("Etapa 3 de tu práctica")


def construir_catalogo(series: list[dict]) -> pd.DataFrame:
    """
    Arma el DataFrame de la tabla `bie_indicador` a partir de la lista de
    series que decidiste descargar.

    Columnas: indicador_id, indicador_nombre, gran_division, unidad,
              frecuencia, fuente

    `gran_division` es la columna más importante del proyecto: es la que
    permite unir tu capa macro con la capa micro de Abgail. Los valores
    válidos son exactamente: 'Primarias', 'Secundarias', 'Terciarias',
    'Total'. Cualquier otra cosa rompe el JOIN final.
    """
    # TODO (Aremy): devolver el catálogo como DataFrame.
    raise NotImplementedError("Etapa 3 de tu práctica")


def cargar_observaciones(df: pd.DataFrame) -> int:
    """Guarda observaciones en `bie_observacion`. Idempotente."""
    # TODO (Aremy): usar core.db.guardar.
    raise NotImplementedError("Etapa 4 de tu práctica")


def cargar_catalogo(df: pd.DataFrame) -> int:
    """Guarda metadatos en `bie_indicador`. Idempotente."""
    # TODO (Aremy): usar core.db.guardar.
    raise NotImplementedError("Etapa 4 de tu práctica")


def correr(series: list[dict], area_geografica: str = CAMPECHE) -> int:
    """
    Orquesta el pipeline completo. No la modifiques: `main.py` la llama
    sin saber cómo funciona por dentro.

    `series` es una lista de diccionarios, uno por indicador, con al
    menos las llaves que necesita `construir_catalogo`.
    """
    cargar_catalogo(construir_catalogo(series))

    total = 0
    for serie in series:
        respuesta = extraer(serie["indicador_id"], area_geografica)
        df = transformar_observaciones(
            respuesta, serie["indicador_id"], area_geografica
        )
        total += cargar_observaciones(df)
    return total
