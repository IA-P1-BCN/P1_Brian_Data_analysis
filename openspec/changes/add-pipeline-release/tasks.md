# Tasks

## 1. Tests (N2)

- [ ] 1.1 `N2-08` (#17) Añadir `tests/test_clean.py`
  - Criterio: fechas, duplicados, nulos, negativos y outliers cubiertos
  - Validación: `pytest tests/test_clean.py -q`

- [ ] 1.2 `N2-08` (#17) Añadir `tests/test_features.py`
  - Criterio: ratios, media móvil y merge cubiertos
  - Validación: `pytest tests/test_features.py -q`

## 2. Pipeline (N3)

- [ ] 2.1 `N3-07` (#26) Crear `scripts/run_pipeline.py`
  - Criterio: raw → processed en un comando
  - Validación: `python scripts/run_pipeline.py`

- [ ] 2.2 `N3-07` (#26) Ampliar la CI con el job de notebooks
  - Criterio: se ejecuta en PRs que tocan `notebooks/` o `src/`
  - Validación: PR de prueba con un notebook roto

## 3. Release (N3)

- [ ] 3.1 `N3-08` (#27) QA final: `/verify` y revisión del informe
  - Criterio: ruff, pytest, notebooks, OpenSpec y agentes en verde
  - Validación: salida de `/verify`

- [ ] 3.2 `N3-08` (#27) Crear el tag `v1.0.0` y la release
  - Criterio: release con resumen y enlaces al notebook y al informe
  - Validación: `gh release view v1.0.0`

## 4. Cierre

- [ ] 4.1 Ejecutar `/sdd-review`
- [ ] 4.2 Ejecutar `/verify`
- [ ] 4.3 Registrar en `docs/ai-log.md`
