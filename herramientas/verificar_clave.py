import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.api import obtener_json
from core.config import obtener_token
from extract.bie import extraer

token = obtener_token("TOKEN_INDICADORES")
BASE = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/"


def traducir(metodo: str, codigo: str) -> str:
    url = BASE + f"{metodo}/{codigo}/es/BISE/2.0/{token}?type=json"
    datos = obtener_json(url, descripcion=f"{metodo} {codigo}")
    return datos["CODE"][0]["Description"]


for clave in ("6207137768", "6207137758", "6207137762"):
    serie = extraer(clave, "04")["Series"][0]
    unidad = traducir("CL_UNIT", serie["UNIT"])
    frecuencia = traducir("CL_FREQ", serie["FREQ"])
    print(f"{clave} | UNIT {serie['UNIT']} | FREQ {serie['FREQ']}")
    print(f"  Unidad exacta: {unidad}")
    print(f"  Frecuencia exacta: {frecuencia}")