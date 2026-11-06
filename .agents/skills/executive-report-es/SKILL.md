---
name: executive-report-es
description: Plantilla y estilo del informe ejecutivo del EDA en español (1-2 páginas, audiencia CEO, sin jerga, cifras trazables, limitaciones y recomendaciones). Úsala al escribir o revisar reports/informe.md.
---

# Informe ejecutivo en español

## Audiencia

CEO o directivo no técnico. Sabe leer una tabla y un gráfico, pero **no**
quiere ver código, nombres de columnas ni p-valores sin explicación.

## Extensión

**1–2 páginas.** Si no cabe, el problema es de selección, no de espacio.

## Estructura

```markdown
# <Título con el hallazgo principal>

## Resumen ejecutivo
- 3 bullets con las conclusiones más importantes.
- Cada bullet con una cifra y su unidad.

## Contexto y datos
- Qué dataset, qué periodo, cuántas filas y estados.
- Qué limitaciones tiene la fuente.

## Qué hicimos
- 3–5 líneas: limpieza, normalización, integración de población.
- Sin detalle técnico innecesario.

## Hallazgos
### 1. <Hallazgo>
- Evidencia: cifra + gráfico/tabla.
- Lectura: qué significa.

### 2. <Hallazgo>
...

### 3. <Hallazgo>
...

## Recomendaciones
- 3 acciones concretas, priorizadas.
- Cada una ligada a un hallazgo.

## Limitaciones
- Subregistro, cambios de reporting, fines de semana, comparabilidad.
- Qué no se puede concluir con estos datos.

## Próximos pasos
- Qué haría falta para responder mejor la pregunta.
```

## Reglas de estilo

- **Español claro.** Frases cortas. Voz activa.
- **Sin jerga.** Si usas “positividad”, defínelo la primera vez.
- **Cifras con unidad y periodo.** “12,3 % en julio de 2020”, no “12,3”.
- **Una idea por párrafo.**
- **Cada cifra es trazable** a una celda del notebook o a una figura de
  `reports/figures/`. Si no, no va.
- **No causalidad.** “Se observa una asociación”, no “X causa Y”.
- **No adornos.** Sin “revolucionario”, “sin precedentes” ni adjetivos vacíos.
- **Tablas pequeñas.** Máximo 5 columnas y 10 filas; el resto, anexo.

## Figuras

- 1–2 figuras como máximo en el cuerpo.
- Título que diga el hallazgo, no la variable.
- Ejes con unidad.
- Fuente y periodo en el pie.
- Si el gráfico necesita explicación larga, no es un buen gráfico ejecutivo.

## Checklist antes de entregar

- [ ] Cabe en 2 páginas.
- [ ] El resumen ejecutivo se entiende sin leer el resto.
- [ ] Cada hallazgo tiene cifra y evidencia.
- [ ] Las recomendaciones se derivan de los hallazgos.
- [ ] Hay una sección de limitaciones.
- [ ] No hay nombres de columnas del dataset sin explicar.
- [ ] No hay ninguna cifra inventada.
