# Proposal

## Why

El análisis necesita un dataset real, descargable y validado. Hoy no hay
código de carga ni un diccionario que explique qué significa cada columna.
Sin una ingesta reproducible, cada notebook descargaría el CSV a su manera y
los resultados no serían comparables.

## What Changes

- Añadir `src/eda/load.py` con descarga, caché local y lectura del COVID
  Tracking Project.
- Validar el esquema mínimo: ≥1000 filas, ≥8 columnas y columnas clave
  presentes.
- Documentar el dataset en `docs/data_dictionary.md`.
- Ignorar los CSV crudos en git y mantener una copia local en `data/raw/`.

## Capabilities

### New Capabilities

- `ingesta`: descarga, caché, lectura y validación del dataset crudo.

### Modified Capabilities

Ninguna.

## Impact

- `src/eda/load.py`, `tests/test_load.py`.
- `data/raw/`, `data/external/`.
- `docs/data_dictionary.md`, `README.md`.
- `openspec/changes/add-analisis-exploratorio/` consume esta capacidad.
