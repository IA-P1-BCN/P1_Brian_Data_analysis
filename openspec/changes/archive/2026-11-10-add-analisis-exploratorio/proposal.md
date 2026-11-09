# Proposal

## Why

El proyecto debe responder preguntas de negocio con datos, no solo describir
columnas. Hoy no existe un notebook que perfile el dataset, plantee
preguntas, compare variables y lea tendencias. Sin eso, no hay EDA que
entregar.

## What Changes

- Crear `notebooks/01_profiling.ipynb` con forma, tipos, nulos y duplicados.
- Definir 3 preguntas de negocio con su hipótesis antes de analizar.
- Añadir 3 análisis univariados y 3 bivariados con interpretación.
- Añadir análisis agregado por estado, correlación y tendencias temporales.
- Cerrar `notebooks/02_eda.ipynb` como notebook narrativo v1.

## Capabilities

### New Capabilities

- `analisis`: perfilado, preguntas de negocio, univariado, bivariado,
  agregados, correlación y tendencias.

### Modified Capabilities

Ninguna.

## Impact

- `notebooks/01_profiling.ipynb`, `notebooks/02_eda.ipynb`.
- `reports/figures/`.
- `src/eda/viz.py` (consumido desde `add-informe-ejecutivo`).
- `reports/informe.md` (consumido por `add-informe-ejecutivo`).
