# Práctica 04 · Estructura económica de Campeche

Pipeline de datos del INEGI construido **entre dos personas, en un solo repositorio**.

Hasta ahora cada quien trabajó en su propio repo. Esta vez no. El producto final
no existe si falta cualquiera de las dos mitades, y eso cambia la forma de
trabajar: hay que ponerse de acuerdo, revisarse el trabajo y resolver los choques.

> **Ojo con el cambio.** Antes este repositorio era solo de lectura: traía los
> enunciados y cada quien desarrollaba en su propio repo. **Ahora este repositorio
> es el proyecto.** Aquí se trabaja, aquí van los commits de las dos. Las prácticas
> anteriores quedaron guardadas en [`archivo/`](archivo/).

## La pregunta que queremos responder

> ¿La composición de las unidades económicas de Campeche se corresponde con el
> comportamiento de su actividad económica agregada?

Dicho en corto: hay muchísimos comercios pequeños en el estado, pero el ITAEE lo
mueven otras cosas. Queremos ver ese desajuste con datos, no con intuición.

Ninguna de las dos puede contestar esto sola.

## Las dos mitades

| Persona | Capa | Fuente | Qué construye |
|---------|------|--------|---------------|
| **Abgail** | Micro | API del DENUE | Un renglón por establecimiento: dónde está, a qué se dedica, de qué tamaño es |
| **Aremy** | Macro | API de Indicadores (BIE) | Series de tiempo de actividad económica de Campeche y del país |

Las dos capas se unen por la columna `gran_division` (Primarias / Secundarias /
Terciarias). Esa columna es el puente y por eso está definida en `esquema.sql`
y no la inventa nadie sobre la marcha.

## Estructura del proyecto

```
.
├── main.py                 ← punto de entrada · LAS DOS lo editan
├── esquema.sql             ← el contrato: estructura de la base de datos
├── core/                   ← infraestructura compartida · NADIE la edita sin avisar
│   ├── api.py              ·  cliente HTTP con reintentos
│   ├── config.py           ·  lectura de tokens desde .env
│   └── db.py               ·  guardado en SQLite sin duplicados
├── extract/
│   ├── denue.py            ← dueña: Abgail
│   └── bie.py              ← dueña: Aremy
├── docs/                   ← consignas, contrato de datos y conceptos
├── integracion/            ← el análisis final, que se hace en pareja
└── archivo/                ← prácticas anteriores, solo de consulta
```

## Antes de escribir una sola línea

1. Lee **[`docs/00-conceptos-trabajo-en-equipo.md`](docs/00-conceptos-trabajo-en-equipo.md)**.
   Trae los conceptos nuevos de esta práctica: rama, pull request, revisión,
   conflicto de merge, issue.
2. Lee **[`docs/contrato-de-datos.md`](docs/contrato-de-datos.md)**. Es lo que
   las dos se están prometiendo mutuamente.
3. Lee tu consigna:
   - Aremy → [`docs/practica-A-aremy-bie-macro.md`](docs/practica-A-aremy-bie-macro.md)
   - Abgail → [`docs/practica-B-abgail-denue-micro.md`](docs/practica-B-abgail-denue-micro.md)

## Puesta en marcha

```bash
git clone https://github.com/iChocko/splan_practicas.git
cd splan_practicas

python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # y pega tu token adentro
```

Para comprobar que todo quedó bien instalado:

```bash
python main.py
```

Debe crear la base de datos y mostrarte una tabla con los catálogos ya cargados
y las tablas de datos en cero. Si llegaste hasta ahí, estás lista para empezar.

## Reglas del juego

- **Nadie trabaja en `main`.** Cada quien en su rama. Los cambios entran por
  pull request.
- **Ningún PR se fusiona sin revisión de la otra.** Al menos un comentario
  sustantivo: una duda real, algo que no se entiende, algo que se puede romper.
  "Se ve bien" no cuenta como revisión.
- **Un commit al día como mínimo.** El historial cuenta la historia del trabajo.
- **`core/` y `esquema.sql` no se tocan por libre.** Si algo de ahí les estorba,
  abran un issue, discútanlo, y cámbienlo en un PR aparte que las dos aprueben.
- **Pueden y deben usar asistentes de IA.** Cada etapa trae sugerencias de cómo
  pedir las cosas. La regla de siempre: **nunca aceptes código que no puedas
  explicar.** En un PR van a tener que defenderlo.
- **El `.env` no se sube nunca.** Ni el token en el chat de la IA, ni en un
  commit, ni en una captura de pantalla.
- Si se atoran más de veinte minutos en el mismo error, anoten qué intentaron
  y pregunten. En este proyecto atorarse en silencio bloquea también a la otra.

## Estado del pipeline

<!-- Cada quien agrega su renglón cuando su capa quede funcionando. -->

| Capa | Responsable | Estado | Filas cargadas |
|------|-------------|--------|----------------|
