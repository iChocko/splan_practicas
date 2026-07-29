"""
core.db — Acceso a la base de datos SQLite compartida.

INFRAESTRUCTURA COMÚN. No la modifiquen sin avisar.

Regla de oro de este módulo: **guardar es idempotente**. Correr el pipeline
dos veces no debe duplicar filas. Eso se logra con `INSERT OR REPLACE` sobre
las llaves primarias definidas en `esquema.sql`.

Si al reejecutar les crece el número de filas, algo está mal: o la llave
primaria no es la correcta, o están escribiendo por fuera de este módulo.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from core.config import RAIZ, ruta_base_datos


def conectar() -> sqlite3.Connection:
    """Abre (o crea) la base de datos y activa las llaves foráneas."""
    conexion = sqlite3.connect(ruta_base_datos())
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion


def crear_esquema() -> None:
    """
    Ejecuta `esquema.sql`. Es seguro correrlo muchas veces: todas las
    sentencias usan IF NOT EXISTS / INSERT OR IGNORE.
    """
    ruta_sql = RAIZ / "esquema.sql"
    if not ruta_sql.exists():
        raise FileNotFoundError(f"No encontré {ruta_sql}")

    with conectar() as conexion:
        conexion.executescript(ruta_sql.read_text(encoding="utf-8"))
    print(f"Esquema aplicado sobre {ruta_base_datos()}")


def guardar(df: pd.DataFrame, tabla: str) -> int:
    """
    Guarda un DataFrame en `tabla` sin generar duplicados.

    Las columnas del DataFrame deben llamarse EXACTAMENTE igual que las
    columnas de la tabla. Si sobra o falta alguna, esto truena a propósito:
    es la forma de enterarse temprano de que rompieron el contrato de datos.

    Devuelve el número de filas escritas.
    """
    if df.empty:
        print(f"  · Nada que guardar en {tabla} (DataFrame vacío)")
        return 0

    with conectar() as conexion:
        columnas_tabla = [
            fila[1] for fila in conexion.execute(f"PRAGMA table_info({tabla});")
        ]
        if not columnas_tabla:
            raise ValueError(
                f"La tabla '{tabla}' no existe. ¿Corriste crear_esquema() antes?"
            )

        faltantes = set(columnas_tabla) - set(df.columns)
        sobrantes = set(df.columns) - set(columnas_tabla)
        if faltantes or sobrantes:
            raise ValueError(
                f"El DataFrame no cuadra con la tabla '{tabla}'.\n"
                f"  Faltan columnas: {sorted(faltantes) or 'ninguna'}\n"
                f"  Sobran columnas: {sorted(sobrantes) or 'ninguna'}\n"
                f"Revisa docs/contrato-de-datos.md"
            )

        df = df[columnas_tabla]
        marcadores = ", ".join("?" for _ in columnas_tabla)
        nombres = ", ".join(columnas_tabla)
        sentencia = f"INSERT OR REPLACE INTO {tabla} ({nombres}) VALUES ({marcadores})"
        conexion.executemany(sentencia, df.itertuples(index=False, name=None))

    print(f"  · {len(df)} filas guardadas en {tabla}")
    return len(df)


def consultar(sql: str, parametros: tuple = ()) -> pd.DataFrame:
    """Ejecuta un SELECT y devuelve el resultado como DataFrame."""
    with conectar() as conexion:
        return pd.read_sql_query(sql, conexion, params=parametros)


def resumen() -> pd.DataFrame:
    """Cuenta las filas de cada tabla. Útil para verificar el estado del pipeline."""
    with conectar() as conexion:
        tablas = [
            fila[0] for fila in conexion.execute(
                "SELECT name FROM sqlite_master WHERE type='table' "
                "AND name NOT LIKE 'sqlite_%' ORDER BY name;"
            )
        ]
        filas = [
            {"tabla": t,
             "filas": conexion.execute(f"SELECT COUNT(*) FROM {t};").fetchone()[0]}
            for t in tablas
        ]
    return pd.DataFrame(filas)
