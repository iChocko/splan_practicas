# Contrato de datos

Esto es lo que las dos se están prometiendo. Mientras se cumpla, cada quien puede
trabajar sin preguntarle nada a la otra. En cuanto una lo rompa, la otra se entera
de la peor manera.

## Regla general

`core/db.py` **valida el contrato automáticamente**. Si tu DataFrame no tiene
exactamente las columnas de la tabla —ni una más, ni una menos, con los mismos
nombres— la función `guardar()` truena y te dice cuáles faltan y cuáles sobran.

Eso es a propósito. Es mejor que truene ahí, en tu computadora, a que se guarde
mal y lo descubran hasta el análisis final.

---

## Tabla `denue_establecimiento` — la llena Abgail

Un renglón = un establecimiento.

| Columna | Tipo | Notas |
|---|---|---|
| `id_establecimiento` | TEXT | Llave primaria. Es el campo `Id` del DENUE |
| `clee` | TEXT | Clave única del establecimiento |
| `nombre` | TEXT | |
| `razon_social` | TEXT | Puede venir vacío |
| `cve_ent` | TEXT | `'04'` |
| `cve_mun` | TEXT | Tres dígitos: `'001'`…`'013'` |
| `sector_id` | TEXT | SCIAN de 2 dígitos. **Debe existir en `dim_sector_actividad`** |
| `clase_actividad_id` | TEXT | SCIAN a 6 dígitos |
| `clase_actividad` | TEXT | |
| `estrato_texto` | TEXT | Tal como lo manda el INEGI |
| `estrato_min` | INTEGER | Derivada |
| `estrato_max` | INTEGER | Derivada. Puede ir en `None` |
| `latitud` | REAL | Número, no texto |
| `longitud` | REAL | Número, no texto |
| `fecha_alta` | TEXT | |
| `fecha_extraccion` | TEXT | Fecha en que corriste el pipeline, `AAAA-MM-DD` |

**Compromiso de Abgail:** `sector_id` siempre viene con dos dígitos y siempre
existe en el catálogo. Si algún día aparece un sector nuevo, se abre un issue,
no se mete a la fuerza.

---

## Tabla `bie_observacion` — la llena Aremy

Un renglón = el valor de una serie en un periodo.

| Columna | Tipo | Notas |
|---|---|---|
| `indicador_id` | TEXT | Parte de la llave primaria |
| `area_geografica` | TEXT | `'00'` nacional, `'04'` Campeche. Parte de la llave |
| `periodo` | TEXT | Tal como lo manda el INEGI. Parte de la llave |
| `anio` | INTEGER | Derivada |
| `trimestre` | INTEGER | Derivada. `None` si la serie no es trimestral |
| `valor` | REAL | Número, no texto. Vacío es `None`, **no cero** |
| `fecha_extraccion` | TEXT | `AAAA-MM-DD` |

## Tabla `bie_indicador` — la llena Aremy

Un renglón = una serie descargada.

| Columna | Tipo | Notas |
|---|---|---|
| `indicador_id` | TEXT | Llave primaria |
| `indicador_nombre` | TEXT | Nombre legible, para que se entienda en el análisis |
| `gran_division` | TEXT | **Solo estos valores:** `Primarias`, `Secundarias`, `Terciarias`, `Total` |
| `unidad` | TEXT | |
| `frecuencia` | TEXT | `Trimestral`, `Mensual` o `Anual` |
| `fuente` | TEXT | `BIE` |

**Compromiso de Aremy:** `gran_division` se escribe exactamente así, con esa
mayúscula inicial y sin acentos de más. Si escribes `terciarias` o `Terciario`,
el JOIN final devuelve cero renglones y nadie va a entender por qué.

---

## El puente

Esta es la razón de ser del contrato. La consulta del análisis final se ve, en
esencia, así:

```
denue_establecimiento
    → dim_sector_actividad   (por sector_id)
        → gran_division  ←→  bie_indicador.gran_division
            → bie_observacion   (por indicador_id)
```

Del lado micro se cuenta cuántos establecimientos hay por gran división. Del lado
macro se toma el valor del indicador de esa misma gran división. Solo así son
comparables.

**Si cualquiera de las dos cambia cómo escribe `gran_division`, el puente se cae
en silencio.** No sale ningún error: simplemente el resultado viene vacío. Es la
clase de error más difícil de encontrar, y por eso está escrito aquí.

---

## Cómo cambiar el contrato

No está prohibido. Está regulado:

1. Se abre un issue explicando qué hace falta y por qué.
2. Se discute entre las dos. Si el cambio afecta a `esquema.sql`, también se
   consulta con el supervisor.
3. Se hace en **un PR aparte**, que solo toque el contrato.
4. Las dos lo aprueban antes de fusionar.
5. Las dos actualizan su código en su propia rama.

Nunca metan un cambio de contrato escondido dentro de un PR que hace otra cosa.
Eso es lo que en el trabajo real hace que un sistema se caiga un viernes.
