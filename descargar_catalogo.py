import json

from core.api import obtener_json
from core.config import obtener_token, RAIZ

token = obtener_token("TOKEN_INDICADORES")

url = (
    "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/"
    f"CL_INDICATOR/null/es/BISE/2.0/{token}?type=json"
)

catalogo = obtener_json(url, descripcion="catálogo CL_INDICATOR")

ruta = RAIZ / "catalogo_indicadores.json"
ruta.write_text(json.dumps(catalogo, ensure_ascii=False), encoding="utf-8")

print(f"Peso del archivo: {ruta.stat().st_size} bytes")