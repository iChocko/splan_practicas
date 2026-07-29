# Práctica A · Aremy — Capa macro: el Banco de Información Económica

**Tu archivo:** `extract/bie.py`
**Tu rama:** `feature/bie-aremy`
**Tu token:** el de la API de Indicadores, en `.env` como `TOKEN_INDICADORES`

---

## De qué se trata

El Banco de Información Económica es donde el INEGI publica las series de tiempo
de la economía mexicana. Ahí vive el **ITAEE**: el Indicador Trimestral de la
Actividad Económica Estatal, que es lo más cercano que existe a un "PIB
trimestral" por entidad federativa.

Tú vas a bajar el ITAEE de Campeche —el total y sus tres grandes divisiones:
actividades primarias, secundarias y terciarias— y dejarlo en la base de datos
como una serie limpia y consultable.

Es el mismo dato que se cita en los informes de gobierno. Vale la pena que sepas
de dónde sale y qué tan fácil o difícil es obtenerlo bien.

---

## Antes que nada: dos tokens distintos

El INEGI entrega **un token por API**. El token del DENUE que usa Abgail no te
sirve a ti, y el tuyo no le sirve a ella. Si intentas usar el equivocado, la
respuesta no te va a decir "token inválido": te va a decir *"No se encontraron
resultados"*, que es un mensaje engañoso y te va a hacer perder tiempo buscando
el error en el lugar equivocado.

El tuyo se pide en: **https://www.inegi.org.mx/servicios/api_indicadores.html**

---

## Etapa 1 · Terreno preparado

Clona el repositorio, crea tu rama, arma el entorno, pon tu token en `.env` y
corre `python main.py`. Debe crearte la base de datos con los catálogos cargados.

**Hito:** `python main.py` termina sin error y te muestra `dim_sector_actividad`
con 23 renglones. Primer commit hecho en tu rama.

---

## Etapa 2 · Encontrar los indicadores y extraerlos

Esta etapa tiene un paso previo que Abgail no tiene, y es la parte más parecida
a la investigación real: **la API no te dice qué indicadores existen. Tienes que
averiguar sus claves tú.**

La forma prevista para esto es el **Constructor de consultas**, enlazado desde
la misma página de la documentación. Pruébalo primero. Pero hay una posibilidad
real de que te encuentres con que **el árbol temático no carga** — el servicio
que lo alimenta puede estar temporalmente caído del lado del INEGI. Si eso te
pasa, no es tu conexión ni tu código: es su servidor. No pierdas más de diez
minutos intentándolo antes de pasar al método de respaldo.

### Método de respaldo: bajar el catálogo completo y filtrar tú misma

La API de Indicadores tiene un método aparte, `CL_INDICATOR`, pensado para
consultar el nombre de una clave que ya conoces. Lo que no está documentado a
simple vista es que **también acepta pedir el catálogo entero**, mandando
`null` donde normalmente iría una clave:

```
https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/CL_INDICATOR/null/es/BISE/2.0/TU_TOKEN?type=json
```

Eso te devuelve más de 30 mil indicadores con su clave y su descripción, en un
archivo de unos 4 MB. Se descarga en un par de segundos. De ahí puedes filtrar
en Python los que contengan `"ITAEE"` en la descripción, y afinar por las
palabras `"Total de la economía"`, `"Actividades primarias"`,
`"Actividades secundarias"` y `"Actividades terciarias"`.

Vas a encontrar que **hay varias claves con la misma descripción exacta**. No
es un error del catálogo: son distintas variantes de la misma serie —
distinta unidad de medida (índice, variación porcentual anual, contribución a
la variación nacional) y distinta frecuencia (trimestral, anual). Antes de
elegir, tienes que verificar cada candidata:

- Hay un método más, `CL_UNIT`, que te traduce el código de unidad a texto
  legible. Búscalo con la clave `UNIT` que trae la respuesta de cada serie.
  Tú quieres la que diga algo como *"Índice de volumen físico base 2018=100"*
  — es la que te deja comparar niveles a través del tiempo, no una tasa de
  variación.
- Hay un tercer método, `CL_FREQ`, para lo mismo con la frecuencia.
- El campo `TOPIC` de cada serie es el identificador del tema. Puedes
  confirmar que apunta a donde crees consultando `CL_TOPIC` con `null` — trae
  todos los temas del BIE, y ahí vas a encontrar el que corresponde al ITAEE
  por su nombre.

> Sugerencia de prompt:
> "Voy a bajar el catálogo completo de indicadores de una API pública, en
> formato JSON, con un campo `value` (la clave) y `Description` (el nombre).
> Quiero filtrar en pandas los que contengan cierta palabra en la descripción,
> y luego contar cuántas descripciones distintas hay entre los resultados.
> Ayúdame a escribir eso, explicando cada paso."

Documenta en tu PR **cómo** llegaste a las cuatro claves finales —by qué
descartaste las demás variantes— porque en tres meses nadie, ni tú, se va a
acordar.

Un par de datos del ITAEE que te conviene saber de antemano, porque explican
lo que vas a ver:

- El programa del ITAEE existe desde 2009 y tiene series retropoladas desde
  2003, pero eso es la historia completa del *programa estadístico*, no
  necesariamente lo que cualquier clave particular de la API te va a
  devolver. Cada rebase de año base genera claves nuevas, y una clave nueva
  puede traer menos historia que el programa en su conjunto. **Verifica el
  rango real de tu serie contigo misma; no lo asumas.**
- El año base actual es **2018**, y el clasificador de actividades es **SCIAN
  2018** — el mismo que usa el DENUE de Abgail. Que las dos fuentes compartan
  clasificador no es casualidad: es lo que hace posible el análisis conjunto.

Una advertencia sobre la IA aquí: si le pides claves de indicadores del INEGI
directamente, te las va a inventar con toda seguridad y toda confianza. Las
claves son números largos, son exactamente el tipo de dato que un modelo
alucina, y no hay forma de distinguir una inventada de una real salvo
probándola contra la API. **Sácalas del catálogo, nunca del chat.** Puedes
usar la IA para todo lo demás de esta etapa: para escribir el código que
filtra el catálogo, para entender la estructura de la respuesta, para armar
la URL. Solo la clave final tiene que salir de un dato verificado.

Después implementa `extraer()`. La URL lleva un orden estricto de parámetros:
indicador, idioma, área geográfica, si quieres solo el dato más reciente, la
fuente, la versión y el token. Un parámetro fuera de lugar da error HTTP 400 —
y para colmo, un error 400 por parámetro mal puesto se ve **igual** que un
error 400 por token inválido. Cuando te pase, revisa primero el orden de la
URL contra la documentación, letra por letra.

**Hito:** obtienes una respuesta con datos reales de una de las cuatro series,
y el campo `COBER_GEO` de la observación coincide con el área que pediste.

---

## Etapa 3 · Transformación

Implementa `transformar_observaciones()` y `construir_catalogo()`.

Aquí tu dificultad es distinta a la de Abgail. Ella pelea con volumen; tú peleas
con **estructura anidada**.

La respuesta del INEGI no es una tabla. Es un diccionario que contiene una lista,
que contiene otro diccionario, que contiene la lista de observaciones. Antes de
escribir cualquier transformación, imprime la respuesta y **recórrela con los
ojos** hasta entender dónde vive cada cosa. Ese rato de exploración se paga solo.

Dos cosas más:

**Los periodos.** Llegan como texto y su formato depende de la periodicidad de
la serie. El contrato pide `anio` y `trimestre` por separado. Si algún día bajas
una serie mensual o anual, `trimestre` tiene que ir en `None`, no en cero. La
diferencia importa: cero es un valor, `None` es "no aplica".

**Los valores vacíos.** Un dato faltante no es un cero. Si conviertes vacíos a
cero, tus promedios y tus tasas de crecimiento van a estar mal y no vas a notarlo.

Y una que es de criterio, no técnica: en `construir_catalogo()` tienes que
asignar la `gran_division` de cada serie. Los valores válidos son exactamente
`Primarias`, `Secundarias`, `Terciarias` y `Total`. **Si escribes cualquier otra
cosa, el análisis final devuelve una tabla vacía sin ningún mensaje de error.**
Es el error más caro de este proyecto y el más silencioso.

> Sugerencia de prompt:
> "Tengo una respuesta JSON con varios niveles de anidamiento. Te la pego:
> [pegar la respuesta, sin el token]. Ayúdame a describir su estructura nivel
> por nivel, y dime en qué nivel están los datos que se repiten por periodo.
> No me des código, quiero entender el mapa primero."

**Hito:** las cuatro series pasan por `transformar_observaciones()` y el
resultado lo acepta `core.db.guardar()` sin quejarse.

---

## Etapa 4 · Carga y control de calidad

Implementa `cargar_observaciones()` y `cargar_catalogo()`. Son cortos.

Lo tuyo es verificar:

1. Corre tu pipeline dos veces. Las filas **no deben crecer**.
2. Revisa que cada serie tenga la cantidad de trimestres que esperas, sin huecos
   en medio. Un trimestre faltante en medio de una serie es una bandera roja.
3. Compara un par de valores contra lo que muestra el sitio del INEGI en pantalla.
   Si no coinciden, el problema está en tu transformación, no en el INEGI.
4. Confirma que las cuatro `gran_division` quedaron escritas exactamente como
   pide el contrato.

**Hito:** la base tiene tus cuatro series completas y verificadas contra la
fuente.

---

## Etapa 5 · Pull request

Sube tu rama y abre el PR. En la descripción incluye, como mínimo:

- Las cuatro claves de indicador y **cómo las obtuviste**.
- Desde qué año arranca cada serie y si alguna tiene huecos.
- Qué hiciste con los valores faltantes.
- Una cosa que no te gusta de tu propio código.

Después, **revisa el PR de Abgail**. Léelo de verdad. Deja al menos un comentario
sustantivo. Presta atención a lo que ella decidió sobre el estrato abierto: esa
decisión afecta el análisis conjunto, y tú eres la única persona que la va a leer
antes de que se vuelva permanente.

**Hito:** tu PR aprobado y fusionado, y tu comentario puesto en el de ella.

---

## Etapa 6 · Integración

Ver [`integracion/README.md`](../integracion/README.md). Esa parte se hace en
pareja.

---

## Para pensar

No hay que entregar respuestas escritas de esto, pero sí hay que poder
sostenerlas en voz alta:

- El ITAEE es un índice, no un monto. ¿Qué puedes y qué no puedes decir con un
  índice? ¿Puedes sumarlo entre entidades? ¿Puedes compararlo entre trimestres?
- Campeche tiene una economía donde el petróleo pesa muchísimo. ¿Qué le hace eso
  al ITAEE total, y por qué la serie de actividades secundarias se comporta
  distinto a la del resto del país?
- El ITAEE se publica alrededor de 120 días después del trimestre. Si en agosto
  te piden un diagnóstico de la economía estatal, ¿cuál es el dato más reciente
  que realmente tienes, y qué haces con ese rezago?
- Bajaste series de tiempo trimestrales. Abgail bajó una fotografía de un
  momento. ¿Es legítimo compararlas? ¿Qué tendrías que decir en una nota al pie
  para que la comparación sea honesta?
