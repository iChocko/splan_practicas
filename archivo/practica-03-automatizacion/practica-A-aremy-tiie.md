# Práctica A · Aremy — La TIIE a 28 días (Banco de México)

> **Antes de empezar:** lee [`00-conceptos-basicos.md`](00-conceptos-basicos.md). Todo lo que aquí suene raro está explicado ahí.

## Qué vas a construir

Un programa en Python que consulta la **TIIE a 28 días** (una tasa de interés de referencia que publica el Banco de México todos los días hábiles), la guarda en una base de datos, y que puede ejecutarse una y otra vez **sin duplicar información**. Todo tu trabajo quedará versionado en un repositorio de GitHub tuyo.

¿Por qué la TIIE? Porque es una de las tasas más importantes de la economía mexicana: los créditos, incluidos los que contratan los gobiernos estatales para financiar infraestructura, suelen estar referenciados a ella. El dato que vas a descargar es un dato que se usa de verdad.

## Qué vas a saber hacer al terminar

- Consumir una API pública que requiere autenticación con token.
- Guardar datos en una base de datos SQLite y consultarlos con SQL.
- Lograr que un programa sea seguro de re-ejecutar (ya descubrirás a qué nos referimos).
- Manejar un repositorio Git: crear, hacer commits y publicar en GitHub.
- Proteger credenciales con `.env` y `.gitignore`.

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

## Etapa 1 — Preparar el terreno

### 1.1 Consigue el enunciado

Clona el repositorio de prácticas (es del jefe, tú solo lo lees):

```
git clone https://github.com/iChocko/splan_practicas.git
```

### 1.2 Crea TU repositorio

1. En GitHub, crea un repositorio nuevo llamado `practica-03-tiie`. Déjalo público y **no** marques ninguna casilla de "inicializar con README" (lo harás tú desde la terminal, que es la gracia).
2. En tu computadora, crea una carpeta `practica-03-tiie`, entra en ella con la terminal, y conviértela en repositorio:

```
git init
git remote add origin https://github.com/TU_USUARIO/practica-03-tiie.git
```

> `git init` le dice a Git "empieza a vigilar esta carpeta". `git remote add origin ...` le dice "cuando yo diga *push*, envía todo a esta dirección de GitHub".

### 1.3 La estructura del proyecto

Tu carpeta deberá verse así (crea lo que falte; los archivos pueden ir vacíos por ahora):

```
practica-03-tiie/
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
# Credenciales — NUNCA se suben
.env

# Datos generados por el programa
data/

# Basura de Python
__pycache__/
*.pyc
```

> ¿Por qué es tan importante? Tu `.env` contendrá tu token. Si se sube a GitHub, queda expuesto públicamente **para siempre** (Git nunca olvida, ni siquiera si borras el archivo después). El `.gitignore` es tu cinturón de seguridad.

### 1.5 El `.env` y el `.env.example`

- En `.env` guardarás tu token real (lo obtienes en la Etapa 2). Por ahora déjalo con el renglón `BANXICO_TOKEN=` vacío.
- En `.env.example` va **la plantilla sin el secreto**, y este **sí** se sube a GitHub. Sirve para que cualquiera que clone tu proyecto sepa qué credenciales necesita conseguir, sin que tú expongas las tuyas:

```
BANXICO_TOKEN=tu_token_de_64_caracteres_aqui
```

### 1.6 Primer commit

```
git add .
git commit -m "Estructura inicial del proyecto"
git push -u origin main
```

> Si Git se queja de que tu rama se llama `master` en lugar de `main`, ejecuta `git branch -M main` y reintenta el push.

Entra a tu repositorio en GitHub desde el navegador y confirma dos cosas: que tus archivos están ahí, y que **el `.env` NO está** (si aparece, tu `.gitignore` tiene algo mal — corrígelo antes de seguir).

**✅ Hito de la etapa:** tu repositorio existe en GitHub, con la estructura del proyecto y sin el `.env`.

---

## Etapa 2 — Conectar con Banxico

### 2.1 Genera tu token

1. Entra a: https://www.banxico.org.mx/SieAPIRest/service/v1/token
2. Sigue el proceso de generación. Obtendrás una clave de **64 caracteres**.
3. Cópiala en tu `.env`: `BANXICO_TOKEN=tu_clave_de_64_caracteres`

Este token es tuyo. No lo compartas con nadie — ni con tu compañera, ni con la IA.

### 2.2 Conoce tu serie

La serie que vas a consumir es la **`SF43783` — TIIE a 28 días**. Banxico organiza todos sus datos en "series", cada una con un identificador. El endpoint para pedir datos de una serie en un rango de fechas es:

```
https://www.banxico.org.mx/SieAPIRest/service/v1/series/{ID_SERIE}/datos/{FECHA_INICIO}/{FECHA_FIN}
```

con fechas en formato `yyyy-mm-dd`, y el token viajando en un header llamado `Bmx-Token`.

### 2.3 Primera llamada

Pídele a la IA algo como:

> *"Escribe un script de Python que use la librería `requests` para hacer una petición GET al API SIE de Banxico, serie SF43783, con datos del 2026-01-01 a hoy. El token debe leerse de un archivo `.env` (variable `BANXICO_TOKEN`) usando la librería `python-dotenv`, y debe enviarse en el header `Bmx-Token`. Por ahora solo imprime la respuesta JSON tal cual llega. Explícame línea por línea qué hace el script y dime qué librerías necesito instalar con pip."*

Ejecuta el script. Deberías ver un bloque grande de JSON con muchas fechas y valores.

> **Si algo falla:** un error `400` o un mensaje de "Token inválido" casi siempre significa que el token no está llegando bien (revisa el `.env` y el nombre de la variable). Pídele a la IA que te ayude a diagnosticar, pero recuerda: pega el mensaje de error, **no** tu token.

**✅ Hito de la etapa:** ves el JSON de la TIIE en tu pantalla.

---

## Etapa 3 — Entender la respuesta

Antes de guardar nada, hay que entender qué llegó. Observa el JSON con calma y responde en tu cuaderno (o en comentarios del código):

1. ¿Cuántos niveles de "cajas dentro de cajas" hay que abrir para llegar a la lista de datos? (Pista: la ruta pasa por `bmx`, luego `series`, luego `datos`.)
2. Mira una fecha: ¿en qué formato viene? ¿Es el mismo formato que usan tus tablas de Excel o tus queries de SQL?
3. Mira un valor: ¿viene como número o como texto entre comillas? ¿Qué problema podría causar eso al querer, por ejemplo, calcular un promedio?

Estas dos "trampas" (el formato de la fecha y el valor como texto) son reales y tendrás que resolverlas en la siguiente etapa. Las APIs rara vez entregan los datos exactamente como los necesitas — limpiar es parte del oficio.

**✅ Hito de la etapa:** puedes explicar con tus palabras la estructura del JSON y has identificado las dos trampas.

---

## Etapa 4 — Guardar en la base de datos

Ahora convierte ese JSON en registros dentro de una base SQLite ubicada en `data/tiie.db`, en una tabla llamada `tiie` con estas columnas:

| Columna | Tipo | Contenido |
|---------|------|-----------|
| `id_serie` | texto | Siempre `SF43783` (por ahora) |
| `fecha` | texto | La fecha **en formato `yyyy-mm-dd`** (¡convertida!) |
| `valor` | real (decimal) | La tasa **como número** (¡convertida!) |

Pídele a la IA algo como:

> *"Modifica mi script para que, además de traer los datos, los guarde en una base SQLite en `data/tiie.db` usando la librería `sqlite3` que viene con Python. Crea una tabla `tiie` con columnas id_serie (texto), fecha (texto) y valor (decimal). Convierte las fechas de formato dd/mm/yyyy a yyyy-mm-dd y los valores de texto a número antes de insertar. Explícame el código, especialmente la parte de CREATE TABLE y la conversión de fechas."*

Verifica que funcionó consultando tu propia base. Puedes pedirle a la IA:

> *"Dame un mini script (o un comando de terminal con sqlite3) para hacer SELECT de las últimas 10 filas de mi tabla tiie y contar cuántas filas hay en total."*

Aquí ya estás usando tu SQL: prueba un `SELECT` con `WHERE`, busca el valor máximo del año, lo que se te ocurra.

**✅ Hito de la etapa:** el archivo `data/tiie.db` existe y un `SELECT COUNT(*)` te dice cuántos registros guardaste. Anota ese número, lo vas a necesitar.

*(No olvides tu commit: `git add .` → `git commit -m "..."` → `git push`. Fíjate que `data/` no viaja a GitHub — está en el `.gitignore`, porque los datos se regeneran con el script; lo valioso es el código.)*

---

## Etapa 5 — El problema

Esta etapa es corta y no hay que programar nada nuevo.

1. Ejecuta tu script **otra vez**, tal cual está.
2. Cuenta las filas de la tabla otra vez.
3. Compara con el número que anotaste.

¿Qué pasó? Descríbelo con tus propias palabras en tu README (una frase basta). Piensa: si este programa corriera solo, automáticamente, todos los días… ¿qué le pasaría a tu tabla al cabo de un mes?

**✅ Hito de la etapa:** observaste el problema y lo escribiste con tus palabras. No lo resuelvas todavía.

---

## Etapa 6 — La solución

El problema que encontraste tiene nombre en el mundo de la ingeniería de datos: un programa que puede ejecutarse muchas veces produciendo el mismo resultado que si se ejecutara una sola vez se llama **idempotente**. Tu misión es volver idempotente tu script.

La pregunta clave es: **¿qué combinación de columnas identifica de forma única a un registro?** Piénsalo antes de seguir: si tienes dos filas con la misma serie y la misma fecha… ¿pueden ser legítimamente registros distintos, o una es forzosamente un duplicado?

Cuando tengas tu respuesta, pídele a la IA algo como:

> *"Mi tabla tiie se llena de duplicados cada vez que corro el script. Quiero que la combinación de id_serie y fecha sea única, y que al insertar se ignoren los registros que ya existen. Explícame cómo lograrlo en SQLite con una restricción UNIQUE y con INSERT OR IGNORE, y por qué funciona."*

Verifica: ejecuta el script **tres o cuatro veces seguidas** y confirma con `SELECT COUNT(*)` que el número de filas ya no crece.

**✅ Hito de la etapa:** tu script es idempotente y lo demostraste.

---

## Etapa 7 — Cerrar

1. Escribe tu `README.md` (el de TU repositorio). Debe contestar, en corto:
   - ¿Qué hace este proyecto?
   - ¿Qué se necesita para correrlo? (Python, librerías, un token de Banxico — aquí es donde tu `.env.example` cobra sentido)
   - ¿Cómo se corre?
   - ¿Qué fue lo más difícil y qué aprendiste? (dos o tres líneas honestas)
2. Commit y push final.
3. Ejecuta `git log --oneline` y contempla tu historial: esa lista es la historia de tu semana.

**✅ Hito final:** tu repositorio en GitHub está completo, ordenado, con README, y sin ningún secreto expuesto.

---

## Para pensar

*(No hay que entregar nada de esto. Son las preguntas que abren la siguiente puerta.)*

- Si quisieras que este script corriera solo, todos los días a las 9:00 am, sin que tú lo ejecutes… ¿qué necesitarías?
- ¿Qué hace hoy tu script si Banxico no responde (se cae la red, el servicio está en mantenimiento)? ¿Truena? ¿Y cómo debería comportarse?
- Si el script corriera solo y fallara un martes a las 3 am, ¿cómo te enterarías?
- ¿Qué tendrías que cambiar para guardar en PostgreSQL en lugar de SQLite?
- **Reto:** Banxico permite pedir varias series en una sola llamada, separando los IDs con comas. Agrega la serie `SP1` (el INPC, con el que se mide la inflación). Ojo: es **mensual**, no diaria. ¿Tu tabla aguanta mezclar frecuencias distintas? ¿Tu clave única sigue funcionando?

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

**Consejo sobre mensajes de commit:** describe *qué cambió*, en presente y en corto: "Agrega conexión con API de Banxico", "Corrige duplicados con INSERT OR IGNORE". Tu yo del futuro (y tu jefe) te lo agradecerán.
