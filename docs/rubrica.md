# Rúbrica de evaluación

Se evalúa por separado a cada quien, salvo la última sección.

| Criterio | Peso | Qué se busca |
|---|---|---|
| **Pipeline funcionando** | 25 % | Las tres etapas —extraer, transformar, cargar— corren de principio a fin sin intervención manual, y reejecutar no duplica filas |
| **Cumplimiento del contrato** | 15 % | Las columnas, los tipos y los valores permitidos son exactamente los acordados. El JOIN final funciona |
| **Control de calidad** | 15 % | Se verificó el resultado contra la fuente y las diferencias están explicadas, no ignoradas |
| **Uso de Git** | 15 % | Rama propia, commits frecuentes y con mensajes que se entienden, `main` nunca tocada directo, `.env` nunca subido |
| **Calidad de la revisión** | 15 % | El comentario dejado en el PR de la otra es sustantivo: encuentra algo, pregunta algo, previene algo |
| **Descripción del PR** | 10 % | Explica qué se hizo, qué se decidió y con qué argumento. Las decisiones de criterio están justificadas |
| **Análisis conjunto** | 5 % | Conclusión legible y sección de limitaciones honesta (calificación compartida) |

---

## Lo que sube la calificación

- Encontrar un problema real en el código de la compañera durante la revisión.
- Documentar una decisión de criterio con un argumento, aunque la decisión sea
  discutible. Se evalúa el razonamiento, no el acierto.
- Detectar una inconsistencia en los datos del INEGI y reportarla como issue en
  vez de taparla en el código.
- Un mensaje de commit que le sirva a alguien dentro de seis meses.

## Lo que la baja

- Código que no se puede explicar cuando se pregunta. Sin excepciones y sin
  importar de dónde salió.
- Un `.env` o un token en el historial de Git. Esto se revisa siempre.
- Aprobar un PR sin haberlo leído. Se nota en la sesión de cierre, cuando toca
  explicar el código de la otra.
- Cambiar `core/` o `esquema.sql` sin issue previo.
- Resolver un conflicto de merge borrando el trabajo de la otra.

---

## Sesión de cierre

Cada quien explica **el código de su compañera**: qué hace, por qué está escrito
así, y qué decisión tomó ella que se pudo haber tomado de otro modo.

Después, entre las dos, la conclusión del análisis y sus limitaciones.

No es examen. Es la forma más rápida de saber si la revisión de los PR fue real.
