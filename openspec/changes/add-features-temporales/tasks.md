# Tasks

## 1. Features base (N2)

- [ ] 1.1 `N2-05` Añadir `positivity`, `positive_per_100k` y `positive_ma7`
  - Criterio: fórmulas documentadas y sin `inf`
  - Validación: `pytest tests/test_features.py -q`

## 2. Población y ratios (N3)

- [ ] 2.1 `N3-02` Crear `data/external/population.csv` y documentar la fuente
  - Criterio: una fila por estado y población positiva
  - Validación: revisión manual

- [ ] 2.2 `N3-02` Implementar `merge_population()` con validación estricta
  - Criterio: no se pierden estados ni se duplican filas
  - Validación: tests de merge correcto y estado ausente

- [ ] 2.3 `N3-01` Calcular `positive_per_100k`, `death_per_100k` y
  `tests_per_100k`
  - Criterio: comparaciones entre estados normalizadas
  - Validación: test de ratio y figura comparativa

## 3. Tendencias y segmentos (N3)

- [ ] 3.1 `N3-04` Añadir media móvil de 7 días y gráfico logarítmico
  - Criterio: serie original + suavizada + lectura
  - Validación: figura en `reports/figures/`

- [ ] 3.2 `N3-05` Segmentar por región/estado y por olas
  - Criterio: definición de región y de olas documentada
  - Validación: tabla y figura por segmento

## 4. Cierre

- [ ] 4.1 Ejecutar `/sdd-review`
- [ ] 4.2 Ejecutar `/verify`
- [ ] 4.3 Registrar en `docs/ai-log.md`
