# Conceptos nuevos de esta práctica

En la práctica anterior usaron Git como una libreta personal: escribían,
guardaban, subían. Aquí Git empieza a hacer lo que realmente sabe hacer, que es
coordinar a varias personas escribiendo sobre lo mismo sin pisarse.

Léanlo completo antes de empezar. Son siete ideas y ninguna es complicada.

---

## 1. Rama (*branch*)

Una rama es una **línea de trabajo paralela**. Cuando creas una rama, te llevas
una copia del proyecto tal como está en ese momento y empiezas a hacerle cambios
sin que nadie más los vea todavía.

La analogía: el expediente está en el archivo (`main`). Tú sacas una copia de
trabajo, le haces anotaciones durante días, y solo cuando está lista pides que
se integre al expediente oficial. Mientras tanto, el original sigue intacto y tu
compañera puede sacar su propia copia sin estorbarte.

```bash
git checkout -b feature/mi-rama    # crea la rama y te cambia a ella
git branch                          # ver en cuál estás
git checkout main                   # regresar a la principal
```

En este proyecto:

- Aremy → `feature/bie-aremy`
- Abigail → `feature/denue-abigail`

**`main` es sagrada.** Nadie le hace commits directos. `main` siempre debe estar
en un estado que funcione.

---

## 2. Pull request (PR)

Un pull request es **la solicitud formal de que tu rama se integre a `main`**.
No es un comando de Git: es una pantalla de GitHub donde se ve exactamente qué
líneas agregaste, cuáles quitaste, y donde la otra persona puede comentar.

Es, literalmente, un oficio: "solicito que estos cambios se incorporen, por estas
razones". Y como todo oficio, alguien lo tiene que revisar antes de que surta
efecto.

Se abre desde GitHub, después de haber subido tu rama:

```bash
git push -u origin feature/mi-rama
```

GitHub te va a mostrar un botón para abrir el PR. En la descripción explica:
qué hace tu cambio, qué probaste, y qué te dejó dudando. Esa última parte es la
más útil para quien revisa.

---

## 3. Revisión (*code review*)

Es leer el trabajo de la otra persona **antes** de que entre al proyecto.

No es un examen ni una auditoría. Es la última oportunidad de que alguien
encuentre un problema barato antes de que se vuelva caro. En esta práctica es
obligatoria: **ningún PR se fusiona sin que la otra deje al menos un comentario
sustantivo.**

Qué sí es un comentario sustantivo:

- "Aquí conviertes a número pero no manejas el caso de que venga vacío, ¿qué pasa
  si el INEGI manda una celda en blanco?"
- "No entiendo por qué usas `estrato_max` en None cuando el estrato es el más
  grande. ¿Es a propósito?"
- "Esta función hace dos cosas distintas, ¿no convendría partirla?"

Qué no cuenta: "se ve bien", "ok", un pulgar arriba.

Cuando revises, pregunta de verdad. Cuando te revisen, no lo tomes personal:
se está revisando el código, no a ti.

---

## 4. Merge y conflicto de merge

**Merge** es la fusión: los cambios de tu rama pasan a `main`.

Casi siempre Git lo resuelve solo. Pero si las dos modificaron **la misma línea
del mismo archivo**, Git se detiene y dice: "aquí no puedo decidir por ustedes".
Eso es un **conflicto**.

No es un error ni una falla. Es Git negándose a adivinar.

Cuando pasa, el archivo se te marca así:

```
<<<<<<< HEAD
| Micro | Abigail | Funcionando | 47,821 |
=======
| Macro | Aremy | Funcionando | 96 |
>>>>>>> feature/bie-aremy
```

Arriba está lo que ya estaba en `main`, abajo lo que traes tú. Tu trabajo es
**abrir el archivo, decidir cómo debe quedar el texto final, y borrar las marcas
`<<<<<<<`, `=======` y `>>>>>>>`.** En este ejemplo la respuesta correcta es
obvia: dejar los dos renglones. En otros casos hay que hablarlo.

Después:

```bash
git add <archivo>
git commit
```

Va a pasar en esta práctica. Está previsto. Cuando les toque, no lo resuelvan
solas: háblenlo entre ustedes.

---

## 5. Mantener tu rama al día

Mientras trabajas, `main` puede haber avanzado con los cambios de la otra. Antes
de abrir tu PR, tráete esos cambios a tu rama:

```bash
git checkout main
git pull                      # baja lo último de GitHub
git checkout feature/mi-rama
git merge main                # trae main a tu rama
```

Si hay conflicto, es mejor descubrirlo aquí, en tu rama, que en el PR.

---

## 6. Issue

Un issue es **un pendiente escrito en GitHub**: un error encontrado, una duda que
bloquea, una decisión que hay que tomar entre las dos.

En este proyecto úsenlo para todo lo que afecte a la otra: cualquier cambio a
`core/` o a `esquema.sql`, cualquier hallazgo raro en los datos, cualquier
decisión sobre el análisis final.

La regla práctica: **si lo que vas a decidir cambia el trabajo de la otra, no lo
decidas sola. Ábrelo como issue.**

---

## 7. Contrato de datos

Es un concepto que no es de Git, sino de trabajar en equipo con datos.

Un contrato de datos es **el acuerdo sobre la forma exacta que van a tener los
datos**: qué tablas hay, qué columnas tiene cada una, de qué tipo son, cómo se
llaman. Una vez acordado, ninguna de las dos puede cambiarlo sin avisar, porque
la otra construyó su parte asumiendo que se iba a cumplir.

Aquí el contrato vive en `esquema.sql` y está explicado en
[`contrato-de-datos.md`](contrato-de-datos.md).

En su trabajo real esto va a aparecer todo el tiempo, aunque nadie lo llame así:
cuando una dependencia les manda un padrón con las columnas cambiadas de nombre,
lo que se rompió fue un contrato de datos.

---

## Cómo pedirle ayuda a la IA sobre Git

Git es de las pocas cosas donde la IA es excelente maestra, porque los mensajes
de error son crípticos pero muy estándar. Peguen el error completo y pregunten.

Ejemplos de buenos prompts:

> Estoy trabajando en una rama llamada `feature/denue-abigail` y al hacer
> `git merge main` me salió este mensaje: [pegar el mensaje completo].
> Explícame qué significa, qué archivo tengo que abrir y qué tengo que decidir.
> No me des los comandos todavía, primero quiero entender qué está pasando.

> Hice tres commits en mi rama pero uno de ellos no debía ir. ¿Cuáles son mis
> opciones para quitarlo, con las ventajas y riesgos de cada una? Todavía no he
> subido nada a GitHub.

Lo que **no** conviene pedirle: que les resuelva el conflicto sin que ustedes
lean el archivo. El conflicto es una decisión sobre el contenido, y el contenido
lo conocen ustedes, no la IA.
