import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent

with open(RAIZ / "catalogo_indicadores.json", encoding="utf-8") as f:
    datos = json.load(f)

df = pd.DataFrame(datos["CODE"])
print("Columnas:", list(df.columns))

frases = [
    "Total de la economía",
    "Actividades primarias",
    "Actividades secundarias",
    "Actividades terciarias",
]
patron = "|".join(frases)
sel = df[df["Description"].str.contains(patron, case=False, na=False)]
print("Descripciones que coinciden:", len(sel))

for descripcion, grupo in sel.groupby("Description"):
    claves = grupo["value"].tolist()
    print()
    print(descripcion)
    print(f"  claves ({len(claves)}): {claves}")