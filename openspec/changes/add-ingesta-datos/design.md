# Design

## Context

El COVID Tracking Project publica un CSV diario por estado. El fichero es
grande, cambia con el tiempo y no debe versionarse. Los notebooks necesitan
una función estable que devuelva siempre el mismo tipo de `DataFrame`.

## Goals / Non-Goals

**Goals:**
- Una única función de carga para notebooks y tests.
- Caché local que evite descargas repetidas.
- Validación temprana del esquema.
- Diccionario que explique las columnas.

**Non-Goals:**
- Limpiar tipos y nulos (eso es `clean.py`).
- Integrar la población (eso es `features.py`).
- Descargar datos en la CI (los tests usan fixtures).

## Decisions

### Decisión 1 · URL única y configurable

- **Qué:** `COVID_DATA_URL` como constante, con posibilidad de pasar otra
  URL por parámetro.
- **Por qué:** permite tests y cambios de espejo sin tocar la lógica.
- **Alternativas:** hardcodear la URL en el notebook.
- **Consecuencias:** la URL se documenta en el diccionario.

### Decisión 2 · Caché por nombre de fichero

- **Qué:** `data/raw/covid_tracking.csv`.
- **Por qué:** simple, visible y fácil de borrar para forzar la descarga.
- **Alternativas:** caché por hash (más complejo, no aporta aquí).
- **Consecuencias:** si el dataset remoto cambia, hay que borrar el fichero
  a mano o añadir un parámetro `force=True`.

### Decisión 3 · Validación en `load.py`, no en el notebook

- **Qué:** `validate_schema(df)` dentro de `load.py`.
- **Por qué:** falla pronto y el notebook no repite comprobaciones.
- **Alternativas:** validar en cada notebook (se duplica).
- **Consecuencias:** los tests pueden probar la validación sin red.

### Decisión 4 · Tests con fixtures, no con red

- **Qué:** un CSV pequeño en `tests/fixtures/`.
- **Por qué:** la CI no depende del servicio externo.
- **Alternativas:** descargar en la CI (frágil y lento).
- **Consecuencias:** hay que mantener el fixture actualizado.

## Risks / Trade-offs

- El dataset original puede dejar de estar disponible; se documenta la fecha
  de descarga y se permite un espejo local.
- El CSV completo puede cambiar de esquema; la validación lo detecta.
- El diccionario se desactualiza si se añaden columnas sin documentar.
