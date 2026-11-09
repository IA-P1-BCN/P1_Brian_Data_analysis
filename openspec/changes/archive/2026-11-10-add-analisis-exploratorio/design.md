# Design

## Context

El dataset limpio está en `data/processed/`. Los notebooks deben narrar el
análisis sin duplicar lógica y deben poder ejecutarse de arriba abajo. Las
preguntas de negocio se definen antes de mirar los resultados para evitar
sesgo de confirmación.

## Goals / Non-Goals

**Goals:**
- Un perfilado reproducible del dataset.
- 3 preguntas con hipótesis y respuesta.
- 3 univariados y 3 bivariados con interpretación.
- Agregados, correlación y tendencias.
- Un notebook que se lea como un informe.

**Non-Goals:**
- Entrenar modelos predictivos.
- Hacer inferencia causal.
- Escribir el informe ejecutivo (eso es `add-informe-ejecutivo`).

## Decisions

### Decisión 1 · Preguntas antes que gráficos

- **Qué:** la sección 2 del notebook define las preguntas y las hipótesis.
- **Por qué:** evita el “analizo lo que sale” y hace que cada gráfico tenga
  un propósito.
- **Alternativas:** escribir las conclusiones al final y adaptar las
  preguntas (sesgo).
- **Consecuencias:** si una pregunta no se puede responder, se dice.

### Decisión 2 · Tres preguntas, no diez

- **Qué:** 3 preguntas de negocio bien respondidas.
- **Por qué:** la rúbrica valora profundidad, no cantidad.
- **Alternativas:** un catálogo de 10 gráficos sin hilo.
- **Consecuencias:** el informe se construye sobre 3 hallazgos sólidos.

### Decisión 3 · Comparaciones normalizadas cuando toque

- **Qué:** los counts se muestran, pero las comparaciones entre estados se
  hacen por 100k habitantes.
- **Por qué:** California y Wyoming no son comparables en valores absolutos.
- **Alternativas:** ranking por counts (engañoso).
- **Consecuencias:** depende de `add-features-temporales` para la población;
  si aún no está, se usa una tabla de población provisional documentada.

### Decisión 4 · Media móvil para tendencias

- **Qué:** toda serie diaria se muestra con media móvil de 7 días.
- **Por qué:** el reporting de fin de semana distorsiona la serie.
- **Alternativas:** solo serie cruda (picos falsos).
- **Consecuencias:** se explica que la media móvil suaviza, no predice.

## Risks / Trade-offs

- Tres preguntas pueden quedarse cortas si el dataset no las responde; se
  documenta la limitación.
- La correlación puede ser espuria por tendencia temporal; se advierte.
- Los agregados por estado pueden ocultar heterogeneidad temporal.
- El notebook puede crecer demasiado; se mueve lógica a `src/eda/`.
