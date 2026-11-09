# Proposal

## Why

El análisis funciona en local, pero no hay tests de limpieza y features, no
hay un pipeline reproducible de raw a processed y la CI no ejecuta los
notebooks. Sin esto, el nivel Avanzado queda a medias y la entrega no se
puede reproducir.

## What Changes

- Añadir tests de limpieza y features.
- Crear `scripts/run_pipeline.py` que ejecute carga, limpieza, features y
  guarde el dataset procesado.
- Ampliar la CI para ejecutar tests, notebooks y validación de specs.
- Preparar el release `v1.0.0` con el informe y el README finales.

## Capabilities

### New Capabilities

- `ingenieria`: tests, pipeline reproducible, CI y release.

### Modified Capabilities

Ninguna.

## Impact

- `tests/`, `scripts/run_pipeline.py`.
- `.github/workflows/ci.yml`.
- Tag `v1.0.0` y release en GitHub.
- `README.md`.
