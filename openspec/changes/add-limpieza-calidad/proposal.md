# Proposal

## Why

El dataset crudo trae fechas como enteros, columnas con más del 80 % de
nulos, duplicados por `(state, date)`, incrementos negativos por correcciones
de reporting y valores atípicos. Sin una limpieza documentada, cualquier
conclusión del EDA es frágil y no se puede reproducir.

## What Changes

- Añadir `src/eda/clean.py` con la limpieza básica y la avanzada.
- Documentar cada decisión de limpieza con una tabla antes/después.
- Excluir del análisis las columnas con más del 80 % de nulos y justificarlo.
- Tratar los incrementos negativos sin borrarlos a ciegas.
- Analizar outliers con IQR y decidir qué hacer con ellos.
- Añadir una auditoría de calidad con recuentos y ejemplos.

## Capabilities

### New Capabilities

- `calidad-datos`: limpieza, decisiones documentadas y auditoría de calidad
  del dataset.

### Modified Capabilities

Ninguna.

## Impact

- `src/eda/clean.py`, `tests/test_clean.py`.
- `data/processed/covid_clean.csv`.
- `notebooks/01_profiling.ipynb`, `notebooks/02_eda.ipynb`.
- `reports/informe.md` (limitaciones).
- Issue N2-08 (tests) consume esta capacidad desde `add-pipeline-release`.
