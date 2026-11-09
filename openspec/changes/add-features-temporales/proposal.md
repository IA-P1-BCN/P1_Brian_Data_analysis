# Proposal

## Why

Los counts absolutos no permiten comparar estados ni leer tendencias: un
estado grande siempre parece “peor”. Faltan ratios por 100k, una segunda
fuente de población, media móvil, escala logarítmica y segmentos por
estado/región y por olas. Sin estas features, el nivel Avanzado no se
sostiene.

## What Changes

- Añadir `src/eda/features.py` con 3 features nuevas y sus tests.
- Integrar la población por estado con un merge validado.
- Calcular ratios por 100k habitantes.
- Añadir media móvil de 7 días y escala logarítmica.
- Segmentar por estado/región y por olas.

## Capabilities

### New Capabilities

- `features`: transformaciones derivadas (ratios, media móvil, log y
  segmentos) y integración de la población.

### Modified Capabilities

Ninguna.

## Impact

- `src/eda/features.py`, `tests/test_features.py`.
- `data/external/population.csv`.
- `notebooks/02_eda.ipynb`.
- `reports/informe.md` (hallazgos avanzados).
