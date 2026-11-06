# Tasks

## 1. Implementación

- [x] 1.1 `N1-02` (#3) Implementar `load_covid_data()` con descarga y caché
  - Criterio: descarga si falta y lee del disco si existe
  - Validación: `pytest tests/test_load.py -q`

- [x] 1.2 `N1-02` (#3) Implementar `validate_schema()`
  - Criterio: ≥1000 filas, ≥8 columnas y columnas clave presentes
  - Validación: tests de dataset válido e inválido

- [x] 1.3 `N1-02` (#3) Crear `docs/data_dictionary.md`
  - Criterio: cada columna usada tiene significado, tipo y unidad
  - Validación: revisión manual

## 2. Tests

- [x] 2.1 `N1-02` (#3) Añadir fixture pequeño en `tests/fixtures/`
  - Criterio: el test no hace red
  - Validación: `pytest tests/test_load.py -q`

- [x] 2.2 `N1-02` (#3) Probar caché, esquema inválido y fallo de red
  - Criterio: los tres caminos tienen test
  - Validación: `pytest -q`

## 3. Cierre

- [ ] 3.1 Ejecutar `/sdd-review`
- [ ] 3.2 Ejecutar `/verify`
- [ ] 3.3 Registrar en `docs/ai-log.md`
