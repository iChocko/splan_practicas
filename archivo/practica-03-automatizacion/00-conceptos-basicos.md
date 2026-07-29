# Conceptos básicos

Lee esto antes de empezar tu práctica. No necesitas memorizarlo: es un mapa para que las palabras que vas a encontrar no te suenen a otro idioma. Regresa aquí cada vez que un término no te haga sentido.

---

## Sobre internet y las APIs

### ¿Qué es una API?

**API** significa *Application Programming Interface* (interfaz de programación de aplicaciones). Es la forma en que un programa le pide información a otro programa a través de internet.

Piénsalo así: cuando entras a la página del Banco de México con tu navegador, ves tablas y gráficas diseñadas para humanos. Una API es la misma información, pero servida en un formato diseñado para **programas**: sin colores, sin botones, solo datos.

En esta práctica, tu script de Python será el que "visite" la API y se traiga los datos.

### ¿Qué es una petición (request) y qué es GET?

Cuando tu programa le pide algo a una API, eso se llama hacer una **petición** (*request* en inglés). La API contesta con una **respuesta** (*response*).

Las peticiones tienen "verbos" que indican la intención. Los más comunes:

| Verbo | Para qué sirve | Ejemplo cotidiano |
|-------|----------------|-------------------|
| **GET** | Pedir información (solo leer) | "Dame el tipo de cambio de hoy" |
| **POST** | Enviar información (crear algo) | "Registra este nuevo formulario" |

En esta práctica **solo usarás GET**, porque solo vas a leer datos, nunca a modificarlos. Cuando veas en Python algo como `requests.get(...)`, eso es: una petición de lectura.

### ¿Qué es un endpoint?

Un **endpoint** es la dirección exacta (URL) a la que haces la petición. Una misma API tiene varios endpoints, como un edificio tiene varias ventanillas: una para pedir el catálogo, otra para pedir los datos, etc.

Ejemplo: `https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43783/datos` es un endpoint que devuelve los datos de una serie específica.

### ¿Qué es JSON?

**JSON** es el formato de texto en el que la mayoría de las APIs devuelven sus respuestas. Se ve así:

```json
{
  "fecha": "20/07/2026",
  "dato": "6.7458"
}
```

Son pares de `"nombre": valor`, que pueden anidarse (un valor puede contener a su vez más pares adentro, como cajas dentro de cajas). Python convierte el JSON en diccionarios y listas, que ya conoces.

### ¿Qué es un token (o API key)?

Un **token** es una clave larga de letras y números que te identifica ante una API. Funciona como una credencial: la API sabe quién le está pidiendo datos y puede limitar cuántas peticiones haces.

Dos cosas importantes:

1. **No todas las APIs piden token.** Algunas son totalmente abiertas.
2. **Un token es información privada.** No se comparte, no se sube a GitHub, no se pega en chats. Aunque un token de solo lectura no es tan delicado como una contraseña bancaria, el hábito de protegerlo es el mismo, y ese hábito es parte de lo que estás aprendiendo.

### ¿Qué es un header?

Cuando haces una petición, además de la URL puedes enviar información extra "en el sobre", llamada **headers** (encabezados). El uso más común: enviar tu token para identificarte. Por ejemplo, Banxico espera el token en un header llamado `Bmx-Token`.

---

## Sobre guardar los datos

### ¿Qué es SQLite?

**SQLite** es una base de datos que vive en un solo archivo (por ejemplo, `datos.db`). No hay que instalar ningún servidor ni configurar nada: Python ya la trae integrada.

Todo el SQL que ya conoces (`SELECT`, `WHERE`...) funciona igual. Lo nuevo será crear tablas (`CREATE TABLE`) e insertar datos (`INSERT`).

### ¿Por qué no guardar todo en un CSV y ya?

Podrías. Pero una base de datos te permite hacer preguntas con SQL, te ayuda a evitar registros duplicados (esto será importante a media práctica) y es el camino natural hacia herramientas más grandes como PostgreSQL, que se usa en sistemas reales.

---

## Sobre la configuración

### ¿Qué es una variable de entorno y qué es un archivo `.env`?

Regla profesional: **el código y las credenciales viven separados**. Si escribes tu token directamente dentro de tu script y subes el script a GitHub, tu token queda público para siempre (sí, aunque lo borres después: Git recuerda todo).

La solución es un archivo llamado `.env` que vive junto a tu código pero **nunca se sube a GitHub**. Ahí escribes cosas como:

```
BANXICO_TOKEN=aqui_va_tu_token
```

Tu script de Python lee ese archivo al arrancar. Cualquiera puede ver tu código en GitHub, pero nadie ve tus claves.

¿Y cómo evitamos que el `.env` se suba por accidente? Con el `.gitignore`, que viene en la siguiente sección.

---

## Sobre Git y GitHub

### ¿Qué es Git y qué es GitHub?

- **Git** es un programa que corre en tu computadora y lleva el historial de cambios de tu proyecto. Cada vez que "guardas una versión", Git la registra con fecha, autor y descripción. A cada versión guardada se le llama **commit**.
- **GitHub** es un sitio web donde puedes publicar tu repositorio Git para respaldarlo y compartirlo.

Analogía: Git es como el control de cambios de Word, pero para carpetas enteras de código; GitHub es como el Drive donde subes el documento para que otros lo vean.

### Los cuatro conceptos que usarás toda la semana

| Concepto | Qué es |
|----------|--------|
| **Repositorio (repo)** | Una carpeta cuyo historial está siendo registrado por Git |
| **Commit** | Una "fotografía" de tu proyecto en un momento dado, con un mensaje que describe qué cambió |
| **Push** | Enviar tus commits desde tu computadora hacia GitHub |
| **Clone** | Descargar un repositorio completo de GitHub a tu computadora |

### ¿Qué es el `.gitignore`?

Es un archivo de texto donde le dices a Git: "estos archivos **no** los registres nunca". Es la red de seguridad que evita que tu `.env` (con tu token) o tus archivos de datos terminen publicados en GitHub.

### ¿Qué es la terminal?

La terminal (o línea de comandos) es una ventana donde escribes instrucciones con texto en lugar de hacer clic. Git se maneja desde ahí. Al principio se siente árida; para el viernes ya vas a escribir `git status` sin pensarlo.

- En **Mac**: aplicación "Terminal".
- En **Windows**: te recomendamos "Git Bash" (se instala junto con Git).

---

## Cómo pedirle las cosas a la IA

Vas a usar un asistente de IA (opencode u otro) para generar el código. Eso está bien y es intencional: en el trabajo real así se programa hoy. Pero hay una diferencia enorme entre *usar* la IA y *depender ciegamente* de ella. Tres reglas:

1. **Pide siempre la explicación.** Termina tus peticiones con algo como *"...y explícame línea por línea qué hace"*. Leer la explicación es donde ocurre el aprendizaje.
2. **Pide poco a la vez.** Es mejor pedir "un script que solo haga la petición y me muestre la respuesta" que "hazme toda la práctica". Si pides todo junto, obtendrás un bloque que no entiendes y que no podrás defender el viernes.
3. **Nunca compartas tus secretos.** Ni el token ni el contenido de tu `.env` van en el chat. Si necesitas ayuda con algo que involucra el token, reemplázalo por `MI_TOKEN` en lo que pegues.

Cada práctica incluye, en cada etapa, un ejemplo de cómo redactar tu petición a la IA. Son sugerencias: puedes ajustarlas con tus palabras.
