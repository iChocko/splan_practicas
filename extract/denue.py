"""
extract.denue — Capa MICRO del proyecto.

DUEÑA DE ESTE ARCHIVO: Abigail.
Nadie más lo edita. Si alguien más necesita un cambio aquí, te lo pide
por un comentario en el PR o por un issue.

Tu trabajo es llenar los cuerpos de estas tres funciones. Las FIRMAS
(el nombre, los parámetros y lo que devuelve cada una) NO se cambian:
son parte del contrato de datos y `main.py` y la práctica de Aremy
asumen que existen tal como están.

Lee primero: docs/practica-B-abigail-denue-micro.md
             docs/contrato-de-datos.md
"""

from __future__ import annotations

import pandas as pd

from core.api import obtener_json
from core.config import obtener_token
from core.db import guardar

BASE = "https://www.inegi.org.mx/app/api/denue/v1/consulta"
ENTIDAD_CAMPECHE = "04"


def cuantificar(cve_mun: str) -> dict[str, int]:
    """
    Devuelve cuántos establecimientos hay en un municipio, por sector SCIAN,
    SIN descargar los registros. Es una llamada barata que sirve para dos cosas:

      1. Saber a qué sectores vale la pena pedirle datos al DENUE.
      2. Al final, comparar contra lo que realmente descargaste. Si no
         cuadra, algo se te perdió en el camino.

    Parámetros
    ----------
    cve_mun : str
        Clave de municipio de 3 dígitos, ej. '002'.

    Devuelve
    --------
    dict[str, int]
        {'46': 265, '72': 94, ...} — solo sectores de 2 dígitos.

    Notas
    -----
    - El método del DENUE que necesitas es `Cuantificar`, y el área
      geográfica se arma pegando entidad + municipio ('04' + '008').
    - La respuesta trae también subsectores, ramas y clases. Tú solo
      quieres los códigos de 2 dígitos.
    """
    # TODO (Abigail): construir la URL, llamar a obtener_json y filtrar.
    raise NotImplementedError("Etapa 2 de tu práctica")


def extraer(cve_mun: str, sector_id: str) -> list[dict]:
    """
    Descarga del DENUE todos los establecimientos de un municipio y un
    sector SCIAN, recorriendo las páginas que haga falta.

    Parámetros
    ----------
    cve_mun : str
        Clave de municipio de 3 dígitos, ej. '002'.
    sector_id : str
        Sector SCIAN de 2 dígitos, ej. '46'.

    Devuelve
    --------
    list[dict]
        Los registros tal como los entrega el INEGI, sin limpiar.
        Lista vacía si no hay establecimientos.

    Notas
    -----
    - El método que necesitas es `BuscarAreaAct`. Lee la documentación
      oficial para armar la URL; la práctica te dice dónde está.
    - La API te obliga a pedir un rango de registros (del N al M).
      Si pides 1 a 1000 y te devuelve exactamente 1000, es señal de que
      probablemente hay más. Ahí entra la paginación.
    - Usa `obtener_json(url, descripcion=...)` de core.api. No uses
      requests ni urllib directamente: el reintento ya está resuelto.
    - ADVERTENCIA VERIFICADA: cuando una combinación municipio × sector
      no tiene ningún establecimiento, este método NO devuelve una lista
      vacía. Corta la conexión y tu programa va a ver un error. Por eso
      existe `cuantificar()`: úsalo antes para no pedir lo que no existe.
    """
    # TODO (Abigail): construir la URL, paginar y acumular resultados.
    raise NotImplementedError("Etapa 2 de tu práctica")


def transformar(registros: list[dict]) -> pd.DataFrame:
    """
    Convierte los registros crudos del DENUE en un DataFrame que cumple
    EXACTAMENTE el contrato de la tabla `denue_establecimiento`.

    Columnas que debe tener, ni una más ni una menos:
        id_establecimiento, clee, nombre, razon_social, cve_ent, cve_mun,
        sector_id, clase_actividad_id, clase_actividad, estrato_texto,
        estrato_min, estrato_max, latitud, longitud, fecha_alta,
        fecha_extraccion

    Ojo con tres cosas:
      1. `Estrato` viene como texto en rangos ('0 a 5 personas').
         De ahí salen `estrato_min` y `estrato_max`. Tú decides cómo
         tratar el estrato más grande, y lo documentas.
      2. Latitud y longitud vienen como texto, no como número.
      3. `cve_mun` no viene en un campo propio. Está adentro de otro
         campo del registro. Encuéntralo.
    """
    # TODO (Abigail): limpiar, derivar columnas y devolver el DataFrame.
    raise NotImplementedError("Etapa 3 de tu práctica")


def cargar(df: pd.DataFrame) -> int:
    """
    Guarda el DataFrame en la tabla `denue_establecimiento`.
    Debe poder ejecutarse dos veces sin duplicar filas.

    Devuelve el número de filas escritas.
    """
    # TODO (Abigail): usar core.db.guardar. Es una línea.
    raise NotImplementedError("Etapa 4 de tu práctica")


def correr(municipios: list[str], sectores: list[str]) -> int:
    """
    Orquesta el pipeline completo para varias combinaciones de
    municipio × sector. No la modifiques: sirve para que `main.py`
    llame tu parte sin saber cómo funciona por dentro.
    """
    total = 0
    for cve_mun in municipios:
        universo = cuantificar(cve_mun)
        for sector_id in sectores:
            if universo.get(sector_id, 0) == 0:
                print(f"  · {cve_mun}/{sector_id}: sin establecimientos, se omite")
                continue
            crudos = extraer(cve_mun, sector_id)
            if not crudos:
                continue
            df = transformar(crudos)
            escritas = cargar(df)
            esperadas = universo[sector_id]
            if escritas != esperadas:
                print(f"  ! {cve_mun}/{sector_id}: esperaba {esperadas}, "
                      f"guardé {escritas}. Documenta la diferencia.")
            total += escritas
    return total
