import json

import pandas as pd

with open("catalogo_indicadores.json", encoding="utf-8") as f:
    datos = json.load(f)

df = pd.DataFrame(datos["CODE"])
print("Total de indicadores:", len(df))

filtrados = df[df["Description"].str.contains("ITAEE", case=False, na=False)]
print("Con 'ITAEE' en la descripción:", len(filtrados))

print("Descripciones distintas:", filtrados["Description"].nunique())
print(filtrados["Description"].value_counts().to_string())