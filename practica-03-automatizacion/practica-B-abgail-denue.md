# Práctica B · Abgail — El DENUE por estado (Data México)

> **Antes de empezar:** lee [`00-conceptos-basicos.md`](00-conceptos-basicos.md). Todo lo que aquí suene raro está explicado ahí.

## Qué vas a construir

Un programa en Python que consulta el número de **establecimientos económicos registrados en el DENUE** (el directorio de negocios del INEGI) para todos los estados del país y todos los años disponibles, lo guarda en una base de datos, y puede ejecutarse una y otra vez **sin duplicar información**. Todo tu trabajo quedará versionado en un repositorio de GitHub tuyo.

La fuente será **Data México**, una plataforma de la Secretaría de Economía que concentra decenas de bases de datos públicas y las sirve a través de una sola API. A diferencia de otras APIs, esta no pide token: es completamente abierta. Tu reto no será la autenticación, sino algo más interesante: **navegar un catálogo con 97 bases de datos distintas y armar la consulta correcta**.

## Qué vas a saber hacer al terminar

- Explorar el catálogo de una API para descubrir qué datos ofrece y cómo pedirlos.
- Consumir una API pública y armar consultas con parámetros.
- Guardar datos en una base de datos SQLite y consultarlos con SQL.
- Lograr que un programa sea seguro de re-ejecutar (ya descubrirás a qué nos referimos).
- Manejar un repositorio Git: crear, hacer commits y publicar en GitHub.
- Separar la configuración del código con `.env` y `.gitignore`.

## Requisitos previos

Verifica que tengas instalado:

- **Python 3** — en la terminal, escribe `python3 --version` (o `python --version`). Debe responder con un número de versión.
- **Git** — escribe `git --version`.
- Tu **cuenta de GitHub** activa.

Si Git es nuevo en tu máquina, preséntate con él (esto se hace una sola vez en la vida):

```
git config --global user.name "Tu Nombre"
git config --global user.email "tu_correo_de_github@ejemplo.com"
```

---

## ⚠️ Aviso importante antes de arrancar

En internet (y en lo que te sugiera la IA) encontrarás muchos tutoriales que usan la dirección `api.datamexico.org`. **Ese dominio ya no existe.** La API se mudó a:

```
https://www.economia.gob.mx/apidatamexico/tesseract/
```

Si la IA te genera código con la dirección vieja, corrígela tú misma con la nueva. Que esto te quede de lección doble: las APIs cambian con el tiempo, y la IA no siempre está al día — quien valida eres tú.

---

## Etapa 1 — Preparar el terreno

### 1.1 Consigue el enunciado

Clona el repositorio de prácticas (es del jefe, tú solo lo lees):

```
git clone https://github.com/iChocko/splan_practicas.git
```

### 1.2 Crea TU repositorio

1. En GitHub, crea un repositorio nuevo llamado `practica-03-denue`. Déjalo público y **no** marques ninguna casilla de "inicializar con README" (lo harás tú desde la terminal, que es la gracia).
2. En tu computadora, crea una carpeta `practica-03-denue`, entra en ella con la terminal, y conviértela en repositorio:

```
git init
git remote add origin https://github.com/TU_USUARIO/practica-03-denue.git
```

> `git init` le dice a Git "empieza a vigilar esta carpeta". `git remote add origin ...` le dice "cuando yo diga *push*, envía todo a esta dirección de GitHub".

### 1.3 La estructura del proyecto

Tu carpeta deberá verse así (crea lo que falte; los archivos pueden ir vacíos por ahora):

```
practica-03-denue/
├── .gitignore
├── .env
├── .env.example
├── README.md
├── extraer.py
└── data/
```

### 1.4 El `.gitignore` (este sí te lo damos textual)

Crea el archivo `.gitignore` con exactamente este contenido:

```
# Configuración local
.env

# Datos generados por el programa
data/

# Basura de Python
__pycache__/
*.pyc
```

> Tu API no usa token, entonces ¿qué protege este `.gitignore`? Dos cosas. Primero, la carpeta `data/`: los archivos de datos **no se versionan** — se regeneran con el script; lo valioso es el código, no el archivo que produce. Segundo, tu `.env`, que aquí no guarda secretos pero sí configuración, y es buena costumbre mantenerlo local. Tu compañera Aremy tiene una tercera razón más dramática; pregúntale el viernes.

### 1.5 El `.env` y el `.env.example`

Aunque esta API no pide credenciales, vas a usar el `.env` para la **configuración**: qué URL base usar y qué base de datos consultar. Así, si mañana la API vuelve a cambiar de dominio (ya pasó una vez), corriges un renglón del `.env` sin tocar el código.

Contenido de tu `.env` (y de tu `.env.example` — en tu caso pueden ser idénticos, porque nada aquí es secreto; reflexiona por qué en el caso de Aremy no pueden serlo):

```
DATAMEXICO_BASE_URL=https://www.economia.gob.mx/apidatamexico/tesseract
DATAMEXICO_CUBO=inegi_denue
```

> **Configuración vs. secreto:** un token es un *secreto* (nunca se publica). Una URL base es *configuración* (puede publicarse, pero conviene tenerla fuera del código para poder cambiarla fácil). Ambos viven cómodos en un `.env`; la diferencia está en qué haces con el `.env.example`.

### 1.6 Primer commit

```
git add .
git commit -m "Estructura inicial del proyecto"
git push -u origin main
```

> Si Git se queja de que tu rama se llama `master` en lugar de `main`, ejecuta `git branch -M main` y reintenta el push.

Entra a tu repositorio en GitHub desde el navegador y confirma que tus archivos están ahí y que la carpeta `data/` **no** aparece.

**✅ Hito de la etapa:** tu repositorio existe en GitHub con la estructura del proyecto.

---

## Etapa 2 — Explorar el catálogo

Data México organiza sus datos en **cubos**. Un cubo es una base de datos con:

- **Dimensiones** (*drilldowns*): los ejes por los que puedes desglosar — geografía, año, industria…
- **Medidas** (*measures*): los números que puedes pedir — cantidad de empresas, empleados…

### 2.1 Mira el catálogo completo

Abre esta URL **en tu navegador** (sí, las peticiones GET también se pueden hacer desde el navegador — eso es exactamente lo que hace el navegador al visitar cualquier página):

```
https://www.economia.gob.mx/apidatamexico/tesseract/cubes
```

Verás un JSON enorme: son los 97 cubos disponibles. No intentes leerlo todo. Solo dimensiona la riqueza: comercio exterior, pobreza, censos económicos, inversión extranjera…

### 2.2 Inspecciona tu cubo

El tuyo es **`inegi_denue`**. Su ficha técnica está en:

```
https://www.economia.gob.mx/apidatamexico/tesseract/cubes/inegi_denue
```

Ábrela y responde en tu cuaderno: ¿qué dimensiones tiene? ¿qué medidas? Busca dónde dice `Geography` y dónde dice `Companies`.

### 2.3 Primera consulta de datos

Las consultas de datos van al endpoint `data.jsonrecords`, con parámetros que indican cubo, dimensiones y medidas. Pídele a la IA algo como:

> *"Escribe un script de Python que use la librería `requests` para hacer una petición GET a la API de Data México. La URL base debe leerse de un archivo `.env` (variable `DATAMEXICO_BASE_URL`) con la librería `python-dotenv`. El endpoint es `{base}/data.jsonrecords` y los parámetros son: cube=inegi_denue, drilldowns=State,Year, measures=Companies, parents=false, sparse=false. Por ahora solo imprime la respuesta JSON tal cual llega. Explícame línea por línea, incluido cómo `requests` arma los parámetros de la URL, y dime qué librerías instalo con pip."*

**Importante:** si la IA te pone `api.datamexico.org` en el código, ya sabes qué hacer.

Ejecuta el script. Deberías ver una lista con cientos de registros: cada uno con estado, año y número de empresas.

**✅ Hito de la etapa:** ves los datos del DENUE en tu pantalla.

---

## Etapa 3 — Entender la respuesta

Observa el JSON con calma y responde en tu cuaderno (o en comentarios del código):

1. ¿Dónde está la lista de registros dentro de la respuesta? (Pista: busca la llave `data`.)
2. ¿Cada registro trae los valores como números o como texto?
3. Localiza los registros de **Campeche** (State ID = 4). Mira los valores año por año: ¿notas algo raro entre 2015 y 2016? ¿Y en 2023 comparado con 2024?

Sobre la pregunta 3: **no es un error tuyo ni de tu script.** El INEGI actualiza el DENUE por bloques, y hay años con cortes parciales que producen saltos bruscos en las cifras. Es una lección importante: que un dato venga de una fuente oficial y llegue sin errores técnicos **no significa que puedas usarlo sin entender cómo se produce**. Anota este hallazgo: es oro para tu README.

**✅ Hito de la etapa:** puedes explicar la estructura de la respuesta y documentaste la anomalía de los datos de Campeche.

---

## Etapa 4 — Guardar en la base de datos

Ahora convierte esa respuesta en registros dentro de una base SQLite ubicada en `data/denue.db`, en una tabla llamada `denue` con estas columnas:

| Columna | Tipo | Contenido |
|---------|------|-----------|
| `estado_id` | entero | El identificador numérico del estado |
| `estado` | texto | El nombre del estado |
| `anio` | entero | El año |
| `empresas` | entero | El número de establecimientos |

Guarda **todos los estados**, no solo Campeche: la gracia de tener una base de datos es poder filtrarla después con SQL.

Pídele a la IA algo como:

> *"Modifica mi script para que, además de traer los datos, los guarde en una base SQLite en `data/denue.db` usando la librería `sqlite3` que viene con Python. Crea una tabla `denue` con columnas estado_id (entero), estado (texto), anio (entero) y empresas (entero), e inserta todos los registros de la respuesta. Explícame el código, especialmente el CREATE TABLE y el ciclo de inserción."*

Verifica que funcionó consultando tu propia base con el SQL que ya sabes:

> *"Dame un mini script (o un comando de terminal con sqlite3) para consultar mi tabla denue: las filas de Campeche ordenadas por año, y el total de filas de la tabla."*

Juega un poco: ¿qué estado tiene más establecimientos en el último año? ¿Un `GROUP BY` por año, qué te dice?

**✅ Hito de la etapa:** el archivo `data/denue.db` existe y un `SELECT COUNT(*)` te dice cuántos registros guardaste. Anota ese número, lo vas a necesitar.

*(No olvides tu commit: `git add .` → `git commit -m "..."` → `git push`.)*

---

## Etapa 5 — El problema

Esta etapa es corta y no hay que programar nada nuevo.

1. Ejecuta tu script **otra vez**, tal cual está.
2. Cuenta las filas de la tabla otra vez.
3. Compara con el número que anotaste.

¿Qué pasó? Descríbelo con tus propias palabras en tu README (una frase basta). Piensa: si este programa corriera solo, automáticamente, cada semana… ¿qué le pasaría a tu tabla al cabo de un año?

**✅ Hito de la etapa:** observaste el problema y lo escribiste con tus palabras. No lo resuelvas todavía.

---

## Etapa 6 — La solución

El problema que encontraste tiene nombre en el mundo de la ingeniería de datos: un programa que puede ejecutarse muchas veces produciendo el mismo resultado que si se ejecutara una sola vez se llama **idempotente**. Tu misión es volver idempotente tu script.

La pregunta clave es: **¿qué combinación de columnas identifica de forma única a un registro?** Piénsalo con cuidado, porque en tu tabla la respuesta requiere más de una columna: ¿basta el estado? ¿basta el año? ¿O es la *pareja* de ambos la que no puede repetirse? Argumenta tu respuesta antes de seguir: ¿pueden existir legítimamente dos filas con el mismo estado y el mismo año?

Cuando tengas tu respuesta, pídele a la IA algo como:

> *"Mi tabla denue se llena de duplicados cada vez que corro el script. Quiero que la combinación de estado_id y anio sea única, y que al insertar se ignoren los registros que ya existen. Explícame cómo lograrlo en SQLite con una restricción UNIQUE sobre varias columnas y con INSERT OR IGNORE, y por qué funciona."*

Verifica: ejecuta el script **tres o cuatro veces seguidas** y confirma con `SELECT COUNT(*)` que el número de filas ya no crece.

**✅ Hito de la etapa:** tu script es idempotente y lo demostraste.

---

## Etapa 7 — Cerrar

1. Escribe tu `README.md` (el de TU repositorio). Debe contestar, en corto:
   - ¿Qué hace este proyecto?
   - ¿Qué se necesita para correrlo y cómo se corre?
   - La anomalía que encontraste en los datos de Campeche y por qué importa.
   - ¿Qué fue lo más difícil y qué aprendiste? (dos o tres líneas honestas)
2. Commit y push final.
3. Ejecuta `git log --oneline` y contempla tu historial: esa lista es la historia de tu semana.

**✅ Hito final:** tu repositorio en GitHub está completo, ordenado y con README.

---

## Para pensar

*(No hay que entregar nada de esto. Son las preguntas que abren la siguiente puerta.)*

- Si quisieras que este script corriera solo, cada lunes a las 8:00 am, sin que tú lo ejecutes… ¿qué necesitarías?
- ¿Qué hace hoy tu script si la API no responde (se cae la red, el servicio está en mantenimiento)? ¿Truena? ¿Y cómo debería comportarse?
- Si el script corriera solo y fallara, ¿cómo te enterarías?
- ¿Qué tendrías que cambiar para guardar en PostgreSQL en lugar de SQLite?
- **Reto:** agrega la dimensión `Industry` a tus drilldowns, para tener empresas por estado, año **e industria**. Pregunta clave: ¿tu restricción UNIQUE de `(estado_id, anio)` sigue siendo correcta, o acabas de romper tu propia solución? ¿Cuál sería la clave única ahora?

---

## Anexo — Tus comandos Git de la semana

| Comando | Qué hace |
|---------|----------|
| `git status` | Te dice qué archivos cambiaron y qué está listo para commit. **Úsalo todo el tiempo.** |
| `git add .` | Prepara todos los cambios para el próximo commit |
| `git commit -m "mensaje"` | Guarda la fotografía con su descripción |
| `git push` | Envía tus commits a GitHub |
| `git log --oneline` | Muestra tu historial resumido |
| `git clone URL` | Descarga un repositorio existente |
| `git init` | Convierte la carpeta actual en repositorio |
| `git remote add origin URL` | Conecta tu repositorio local con uno de GitHub |

**Consejo sobre mensajes de commit:** describe *qué cambió*, en presente y en corto: "Agrega consulta al cubo inegi_denue", "Corrige duplicados con INSERT OR IGNORE". Tu yo del futuro (y tu jefe) te lo agradecerán.
