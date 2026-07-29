# Práctica B · Abigail — Capa micro: el DENUE

**Tu archivo:** `extract/denue.py`
**Tu rama:** `feature/denue-abigail`
**Tu token:** el de la API del DENUE, en `.env` como `TOKEN_DENUE`

---

## De qué se trata

El Directorio Estadístico Nacional de Unidades Económicas es el censo de negocios
de México: cada establecimiento con actividad económica, con su ubicación, su
giro y su tamaño. En Campeche hay poco menos de **48 mil**.

Tú vas a bajar ese universo —o la parte de él que decidas— y dejarlo ordenado en
una base de datos, con la calidad suficiente para que se pueda sacar una
conclusión con él.

Esto no es un ejercicio de juguete. Es el mismo tipo de dato que se usa para
decidir dónde poner un programa de apoyo a microempresas, y las decisiones que
tomes sobre cómo limpiarlo cambian la respuesta.

---

## Dónde está la documentación

**https://www.inegi.org.mx/servicios/api_denue.html**

Léela antes de escribir nada. Vas a usar dos de sus métodos:

- **`Cuantificar`** — te dice *cuántos* establecimientos hay, sin bajarlos.
- **`BuscarAreaAct`** — te los baja, filtrando por geografía y actividad.

Fíjate bien en el orden de los parámetros de cada URL. La API no te va a decir
"te faltó un parámetro": te va a dar un error genérico o, peor, datos que no son
los que pediste.

---

## Etapa 1 · Terreno preparado

Clona el repositorio, crea tu rama, arma el entorno, pon tu token en `.env` y
corre `python main.py`. Debe crearte la base de datos con los catálogos cargados.

**Hito:** `python main.py` termina sin error y te muestra `dim_municipio` con 13
renglones. Primer commit hecho en tu rama.

---

## Etapa 2 · Extracción

Implementa `cuantificar()` y `extraer()`.

`cuantificar()` es la fácil y es la que va primero, por una razón muy concreta
que vas a agradecer: **el método `BuscarAreaAct` no se porta bien cuando no hay
resultados.** Si le pides los establecimientos de minería en Tenabo —donde no
hay ninguno— no te devuelve una lista vacía: corta la conexión y tu programa ve
un error de red. Si no lo previenes, tu pipeline se va a caer a la mitad y vas a
pensar que fallaste tú.

Por eso el orden es: primero preguntas cuántos hay, y solo pides los que existen.

`extraer()` tiene la parte nueva de esta práctica: **paginación**. La API te
obliga a pedir rangos de registros. Si pides del 1 al 1000 y te llegan
exactamente 1000, es muy probable que haya más y tengas que pedir del 1001 al
2000. Y así hasta que te llegue una página incompleta.

> Sugerencia de prompt:
> "Estoy consumiendo una API que devuelve resultados paginados: recibe un
> registro inicial y uno final. Explícame el patrón general para recorrer todas
> las páginas sin saber de antemano cuántas hay, y cuál es el riesgo si me
> equivoco en la condición de salida. No me des el código todavía, quiero
> entender la lógica y escribirlo yo."

**Hito:** puedes traer todos los establecimientos de un municipio chico
completo, y el número que obtienes coincide con lo que te dijo `cuantificar()`.

---

## Etapa 3 · Transformación

Implementa `transformar()`. Aquí es donde el ejercicio deja de ser técnico y
empieza a ser de criterio.

Tres cosas que vas a tener que resolver:

**El estrato.** El DENUE no te dice cuánta gente trabaja en cada negocio. Te
dice un rango, en texto: `'0 a 5 personas'`, `'11 a 30 personas'`,
`'251 y más personas'`. El contrato te pide dos columnas numéricas, `estrato_min`
y `estrato_max`. Los rangos cerrados son directos. El último no lo es: no tiene
tope. **Tú decides qué hacer con él y lo escribes en tu PR.** No hay una
respuesta correcta única, pero sí hay respuestas que se pueden defender y
respuestas que no.

**El municipio.** El contrato pide `cve_mun` de tres dígitos. La API no te manda
un campo que se llame así. La clave está adentro de otro campo, pegada a otras.
Encuéntrala y explica en tu PR cómo la sacaste.

**Los números que llegan como texto.** Latitud y longitud vienen como cadenas.
Si no las conviertes, se guardan como texto y cualquier cálculo geográfico
posterior falla en silencio.

> Sugerencia de prompt:
> "Tengo una columna de texto con rangos como '0 a 5 personas', '11 a 30
> personas' y '251 y más personas'. Quiero sacar dos columnas numéricas, mínimo
> y máximo. Muéstrame dos o tres estrategias distintas para hacerlo en pandas,
> y dime en qué casos falla cada una. Quiero elegir yo, no que elijas por mí."

**Hito:** `transformar()` devuelve un DataFrame que `core.db.guardar()` acepta
sin quejarse. Si te reclama columnas, léelo con calma: te está diciendo
exactamente qué te falta.

---

## Etapa 4 · Carga y control de calidad

Implementa `cargar()`. Es corto: `core.db.guardar()` ya hace el trabajo.

Lo que sí es tuyo es **comprobar que quedó bien**:

1. Corre tu pipeline dos veces seguidas. El número de filas en la base **no debe
   cambiar**. Si crece, algo está mal con la llave primaria.
2. Compara lo que guardaste contra lo que dijo `cuantificar()`. Si no cuadra,
   averigua por qué antes de seguir. Puede haber una explicación legítima —los
   duplicados, por ejemplo— pero tienes que saber cuál es.
3. Revisa que no haya `sector_id` que no exista en `dim_sector_actividad`.

**Hito:** la base tiene tus datos, el conteo cuadra o sabes explicar la
diferencia, y reejecutar no duplica nada.

---

## Etapa 5 · Pull request

Sube tu rama y abre el PR. En la descripción incluye, como mínimo:

- Qué municipios y sectores descargaste, y **por qué esos**.
- Qué decidiste sobre el estrato abierto y con qué argumento.
- Cuántas filas quedaron y si cuadraron con `cuantificar()`.
- Una cosa que no te gusta de tu propio código.

Ese último punto no es humildad decorativa: quien revisa lee mejor cuando sabe
dónde mirar.

Después, **revisa el PR de Aremy**. Léelo de verdad. Deja al menos un comentario
sustantivo. Si algo no entiendes, ese es exactamente el comentario que hay que
dejar.

**Hito:** tu PR aprobado y fusionado, y tu comentario puesto en el de ella.

---

## Etapa 6 · Integración

Ver [`integracion/README.md`](../integracion/README.md). Esa parte se hace en
pareja.

---

## Para pensar

No hay que entregar respuestas escritas de esto, pero sí hay que poder
sostenerlas en voz alta:

- El DENUE cuenta *establecimientos*, no *empresas*. Una cadena con 40 sucursales
  aparece 40 veces. ¿Cambia eso alguna conclusión que hayas sacado?
- Contaste unidades económicas, no empleo ni producción. Un municipio con muchos
  negocios chiquitos y otro con pocos negocios grandes se ven muy distintos según
  qué midas. ¿Cuál de los dos "pesa más" en la economía del estado, y con qué
  dato lo demostrarías?
- El DENUE se actualiza por rondas de campo, no en tiempo real. ¿Qué tipo de
  negocio crees que está sobrerrepresentado y cuál subrepresentado?
- Si mañana te pidieran usar esto para decidir dónde abrir un módulo de atención
  a microempresas, ¿qué columna te haría falta que no tienes?
