import json

import pandas as pd

with open("catalogo_indicadores.json", encoding="utf-8") as f:
    datos = json.load(f)

df = pd.DataFrame(datos["CODE"])

frases = (
    "Total de la economía",
    "Actividades primarias",
    "Actividades secundarias",
    "Actividades terciarias",
)

sel = df[
    df["Description"].str.startswith("ITAEE", na=False)
    & ~df["Description"].str.contains("Serie Acumulada", na=False)
    & ~df["Description"].str.contains("Por región", na=False)
    & df["Description"].str.endswith(frases)
]
print("Descripciones tras afinar:", sel["Description"].nunique())
print()

for descripcion, grupo in sel.groupby("Description"):
    claves = grupo["value"].tolist()
    print(descripcion)
    print(f"  claves ({len(claves)}): {claves}")
    print()