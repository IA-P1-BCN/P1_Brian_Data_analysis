# Design

## Context

El dataset crudo tiene una fila por estado y fecha, pero no está listo para
analizar: los tipos son mixtos, hay nulos estructurales y valores negativos
que reflejan correcciones de reporting. La limpieza debe ser auditable y
reversible en sus decisiones.

## Goals / Non-Goals

**Goals:**
- Un `clean.py` con funciones pequeñas y testeables.
- Una tabla de decisiones antes/después.
- Un CSV procesado reproducible.
- Una auditoría que explique qué se cambió.

**Non-Goals:**
- Imputar valores con modelos.
- Eliminar outliers de forma automática.
- Integrar población (eso es `features.py`).
- Escribir el informe ejecutivo.

## Decisions

### Decisión 1 · Orden de limpieza

- **Qué:** fechas → duplicados → columnas >80 % → negativos → outliers →
  auditoría.
- **Por qué:** cada paso depende de que el anterior haya dejado el dataset
  consistente.
- **Alternativas:** limpiar todo en una función monolítica.
- **Consecuencias:** más funciones, pero cada una se testea sola.

### Decisión 2 · Negativos a `NaN`, no a 0

- **Qué:** los incrementos negativos se convierten en `NaN` para la serie
  diaria.
- **Por qué:** un 0 inventa un dato; `NaN` dice “no sé” y la media móvil lo
  propaga de forma honesta.
- **Alternativas:** borrar la fila (pierdes el resto de columnas) o dejarlos
  (rompen la media móvil).
- **Consecuencias:** hay que documentar el recuento y no usar esos valores
  en totales.

### Decisión 3 · Outliers: marcar, no borrar

- **Qué:** se calculan los límites IQR y se añade una columna booleana
  `is_outlier_<variable>`.
- **Por qué:** en datos de pandemia, los picos son información, no ruido.
- **Alternativas:** recortar o eliminar automáticamente (sesga la serie).
- **Consecuencias:** el analista decide en el notebook qué hacer con ellos.

### Decisión 4 · Columnas >80 % nulas fuera del análisis

- **Qué:** se excluyen del dataframe de análisis, no del CSV crudo.
- **Por qué:** una columna con 80 % de nulos no sostiene conclusiones.
- **Alternativas:** imputar (inventa datos).
- **Consecuencias:** la lista se documenta y se revisa si cambia el dataset.

## Risks / Trade-offs

- Convertir negativos a `NaN` reduce la muestra de la serie diaria.
- El umbral del 80 % es una convención; se documenta para que sea discutible.
- Los outliers de una pandemia no son errores; el tratamiento debe ser
  conservador.
- La auditoría puede quedarse obsoleta si se cambia la limpieza sin
  regenerarla.
