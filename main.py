"""
main.py — Punto de entrada del pipeline completo.

ARCHIVO COMPARTIDO: las dos lo editan. Es el único lugar del proyecto
donde eso pasa, y es a propósito: aquí van a aprender qué es un conflicto
de merge y cómo se resuelve.

Uso:
    python main.py            # corre todo
    python main.py denue      # corre solo la capa micro
    python main.py bie        # corre solo la capa macro
"""

from __future__ import annotations

import sys

from core.db import crear_esquema, resumen


def correr_denue() -> None:
    """Capa micro — implementa Abigail."""
    from extract import denue

    # --- INICIO CONFIGURACIÓN DENUE (Abigail) -------------------------
    # Define aquí qué municipios y qué sectores vas a descargar.
    municipios: list[str] = []
    sectores: list[str] = []
    # --- FIN CONFIGURACIÓN DENUE -------------------------------------

    if not municipios or not sectores:
        print("Falta configurar municipios y sectores en main.py")
        return

    filas = denue.correr(municipios, sectores)
    print(f"DENUE: {filas} filas procesadas")


def correr_bie() -> None:
    """Capa macro — implementa Aremy."""
    from extract import bie

    # --- INICIO CONFIGURACIÓN BIE (Aremy) ----------------------------
    # Define aquí las series que vas a descargar. Cada elemento es un
    # diccionario con los metadatos que pide construir_catalogo().
    series: list[dict] = [
        {
            "indicador_id": "6207137837",
            "indicador_nombre": (
                "ITAEE. Año base 2018. Actividades económicas por "
                "entidad federativa. Total de la economía"
            ),
            "gran_division": "Total",
            "unidad": "Índice de volumen físico base 2018=100",
            "frecuencia": "Trimestral",
            "fuente": "BIE",
        },
        {
            "indicador_id": "6207137768",
            "indicador_nombre": (
                "ITAEE. Año base 2018. Actividades económicas por "
                "entidad federativa. Actividades primarias"
            ),
            "gran_division": "Primarias",
            "unidad": "Índice de volumen físico base 2018=100",
            "frecuencia": "Trimestral",
            "fuente": "BIE",
        },
        {
            "indicador_id": "6207137758",
            "indicador_nombre": (
                "ITAEE. Año base 2018. Actividades económicas por "
                "entidad federativa. Actividades secundarias"
            ),
            "gran_division": "Secundarias",
            "unidad": "Índice de volumen físico base 2018=100",
            "frecuencia": "Trimestral",
            "fuente": "BIE",
        },
        {
            "indicador_id": "6207137762",
            "indicador_nombre": (
                "ITAEE. Año base 2018. Actividades económicas por "
                "entidad federativa. Actividades terciarias"
            ),
            "gran_division": "Terciarias",
            "unidad": "Índice de volumen físico base 2018=100",
            "frecuencia": "Trimestral",
            "fuente": "BIE",
        },
    ]
    # --- FIN CONFIGURACIÓN BIE ---------------------------------------

    if not series:
        print("Falta configurar las series en main.py")
        return

    filas = bie.correr(series)
    print(f"BIE: {filas} filas procesadas")


def main() -> None:
    crear_esquema()

    que = sys.argv[1] if len(sys.argv) > 1 else "todo"

    if que in ("todo", "denue"):
        correr_denue()
    if que in ("todo", "bie"):
        correr_bie()

    print("\nEstado de la base de datos:")
    print(resumen().to_string(index=False))


if __name__ == "__main__":
    main()
