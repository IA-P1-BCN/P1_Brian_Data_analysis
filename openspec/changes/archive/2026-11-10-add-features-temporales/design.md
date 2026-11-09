# Design

## Context

El dataset limpio tiene una fila por estado y fecha. Para comparar estados y
leer tendencias hacen falta denominadores (población), suavizado y una
segmentación temporal explícita. La población es una segunda fuente que debe
validarse antes de usarla.

## Goals / Non-Goals

**Goals:**
- Tres features nuevas con fórmula y unidad documentadas.
- Merge de población sin pérdida de estados.
- Ratios por 100k comparables.
- Media móvil y escala logarítmica.
- Segmentos por región y por olas.

**Non-Goals:**
- Modelos predictivos.
- Imputar población faltante con medias.
- Cambiar la limpieza de `clean.py`.

## Decisions

### Decisión 1 · Población como tabla externa versionada

- **Qué:** `data/external/population.csv` con `state` y `population`.
- **Por qué:** es una fuente distinta y debe poder auditarse por separado.
- **Alternativas:** hardcodear la población en `features.py`.
- **Consecuencias:** hay que actualizar el CSV si cambia la fuente.

### Decisión 2 · Merge con validación estricta

- **Qué:** `merge(..., how="left", validate="many_to_one")` y asserts de
  estados y filas.
- **Por qué:** un merge silencioso duplica filas o pierde estados.
- **Alternativas:** `how="left"` sin validar (errores difíciles de ver).
- **Consecuencias:** si falta un estado, falla y se ve.

### Decisión 3 · Media móvil por estado, no global

- **Qué:** `groupby("state")["positiveIncrease"].transform(lambda s: s.rolling(7).mean())`.
- **Por qué:** mezclar estados en una media móvil no tiene sentido.
- **Alternativas:** `rolling` global (incorrecto).
- **Consecuencias:** los primeros 6 días de cada estado son `NaN`.

### Decisión 4 · Olas con fechas explícitas

- **Qué:** una tabla de olas con `wave`, `start`, `end`.
- **Por qué:** la definición debe ser la misma para todos los estados.
- **Alternativas:** detectar olas por picos (subjetivo y no reproducible).
- **Consecuencias:** se documenta la fuente de las fechas.

## Risks / Trade-offs

- La población de 2020 no refleja migraciones posteriores.
- La media móvil suaviza picos reales; se muestra también la serie original.
- La escala log puede ocultar diferencias absolutas; se explican los ejes.
- Las olas son una simplificación; se declara en limitaciones.
