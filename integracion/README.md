# Etapa 6 · Análisis conjunto

Esta parte se hace **entre las dos**, en una tercera rama:
`feature/integracion`.

No empieza hasta que las dos capas estén fusionadas en `main`. Si una todavía
no termina, la otra no puede avanzar aquí. Eso también es parte de lo que se
está aprendiendo.

---

## El entregable

Un notebook, `integracion/analisis_conjunto.ipynb`, que responda la pregunta del
proyecto:

> ¿La composición de las unidades económicas de Campeche se corresponde con el
> comportamiento de su actividad económica agregada?

Debe contener, al menos:

1. **Una consulta con JOIN** que traiga en la misma tabla el conteo de
   establecimientos por gran división (lado micro) y el valor del indicador
   correspondiente (lado macro). Esta consulta solo funciona si las dos
   cumplieron el contrato.

2. **Una gráfica** que ponga las dos cosas juntas de forma legible. Ojo: son
   magnitudes incomparables —conteos contra índices—. Resolver eso es parte del
   ejercicio, y la solución que elijan hay que justificarla.

3. **Un texto de media cuartilla** con la conclusión. Escrito para alguien que
   no sabe qué es SQLite ni le importa.

4. **Una sección de limitaciones**, honesta. Qué no se puede concluir con estos
   datos y por qué.

---

## Cómo trabajar en pareja sobre el mismo archivo

Los notebooks son un dolor de cabeza en Git: por dentro son JSON, y cualquier
ejecución cambia medio archivo aunque no hayan tocado el código. Si las dos
editan el mismo `.ipynb` al mismo tiempo, el conflicto es prácticamente
irresoluble.

Así que aquí la coordinación no es opcional. Dos formas de organizarse:

- **Por turnos.** Una trabaja, hace commit y push, avisa. La otra baja los
  cambios y sigue. Simple y suficiente para este tamaño.
- **Por partes.** Cada quien escribe su sección en un archivo `.py` o `.md`
  aparte, y al final una sola persona las integra al notebook.

Elijan una, escríbanla en el PR, y respétenla. Si acaban con un conflicto
irresoluble en el notebook, la salida es descartar una versión y rehacerla:
avísenle al supervisor antes de hacer eso.

---

## Una pista sobre lo que van a encontrar

Es muy probable que el conteo de establecimientos y el indicador macro **no se
parezcan en nada**. Las actividades primarias y las terciarias van a tener un
peso completamente distinto según se miren por número de negocios o por
actividad económica.

Eso no es un error de ustedes. Es el hallazgo. La pregunta interesante no es
"¿por qué no cuadra?" sino **"¿qué está midiendo cada uno, y para qué decisión
sirve cada cual?"**.

Una economía puede tener miles de changarros y poco valor agregado, o pocos
establecimientos y un peso enorme en el producto. Campeche es un caso de libro
de texto de esto último. Si logran explicar por qué, con sus propios datos, la
práctica cumplió su objetivo.

---

## Cierre

El PR de integración lo aprueban las dos y el supervisor. Después:

- Cada quien explica **el código de la otra**, no el propio.
- Entre las dos presentan la conclusión y las limitaciones.

Si alguien no puede explicar el código de su compañera, la revisión del PR fue
de mentiras y se nota inmediatamente. Ese es el punto de todo el ejercicio.
