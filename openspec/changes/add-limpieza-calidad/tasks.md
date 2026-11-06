# Tasks

## 1. Limpieza básica (N1)

- [ ] 1.1 `N1-04` Convertir `date` a `datetime` y validar fechas
  - Criterio: no quedan fechas inválidas sin contar
  - Validación: `pytest tests/test_clean.py -q`

- [ ] 1.2 `N1-04` Eliminar duplicados de `(state, date)`
  - Criterio: la clave es única y el recuento queda registrado
  - Validación: test de duplicado exacto y con distinta calidad

- [ ] 1.3 `N1-04` Guardar `data/processed/covid_clean.csv`
  - Criterio: el CSV se regenera desde `data/raw/` sin pasos manuales
  - Validación: ejecutar `clean.py` dos veces y comparar

## 2. Decisiones justificadas (N2)

- [ ] 2.1 `N2-01` Documentar la tabla antes/después
  - Criterio: filas, columnas, nulos y duplicados antes y después
  - Validación: revisión en el notebook

- [ ] 2.2 `N2-02` Excluir columnas con más del 80 % de nulos
  - Criterio: la lista está documentada y el dataframe de análisis no las
    contiene
  - Validación: test con una columna al 85 % de nulos

- [ ] 2.3 `N2-03` Analizar outliers con IQR y boxplots
  - Criterio: límites de Tukey y recuento por variable
  - Validación: figuras en `reports/figures/`

## 3. Auditoría (N3)

- [ ] 3.1 `N3-03` Detectar y tratar incrementos negativos
  - Criterio: recuento por columna y por estado; decisión documentada
  - Validación: test con un incremento negativo

- [ ] 3.2 `N3-03` Generar la auditoría de calidad
  - Criterio: filas iniciales/finales, columnas eliminadas, duplicados,
    fechas inválidas y negativos
  - Validación: tabla reproducible en el notebook

## 4. Cierre

- [ ] 4.1 Ejecutar `/sdd-review`
- [ ] 4.2 Ejecutar `/verify`
- [ ] 4.3 Registrar en `docs/ai-log.md`
