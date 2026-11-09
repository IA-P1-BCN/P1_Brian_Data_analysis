# features Specification

## Purpose
Añadir las transformaciones que hacen comparables los datos entre estados y
que permiten leer tendencias y segmentos sin caer en conclusiones engañosas
por counts absolutos o por ruido diario.

## Requirements

### Requirement: Tres features nuevas

`features.py` SHALL añadir al menos tres features derivadas y SHALL
documentar su fórmula y su unidad.

#### Scenario: Positividad

- **WHEN** se calcula `positivity`
- **THEN** es `positive / totalTestResults`, está entre 0 y 1 y es `NaN` si
  el denominador es 0 o nulo

#### Scenario: Casos por 100k

- **WHEN** se calcula `positive_per_100k`
- **THEN** usa la población del estado y no produce `inf`

#### Scenario: Media móvil

- **WHEN** se calcula `positive_ma7`
- **THEN** es la media de los 7 días anteriores por estado, ordenada por
  fecha y sin mezclar estados

### Requirement: Merge con población validado

`features.py` SHALL integrar la población por estado y SHALL validar que no
se pierden estados ni se duplican filas.

#### Scenario: Merge correcto

- **WHEN** se hace el merge con `population.csv`
- **THEN** el número de filas no cambia y todos los estados tienen población

#### Scenario: Estado sin población

- **WHEN** un estado del dataset no está en la tabla de población
- **THEN** el merge falla con la lista de estados que faltan

### Requirement: Ratios por 100k habitantes

El proyecto SHALL calcular al menos `positive_per_100k`,
`death_per_100k` y `tests_per_100k` y SHALL usarlos en las comparaciones
entre estados.

#### Scenario: Comparación entre estados

- **WHEN** se comparan dos estados de distinta población
- **THEN** la comparación usa el ratio por 100k, no el count absoluto

### Requirement: Media móvil y escala logarítmica

El notebook SHALL mostrar al menos una serie con media móvil de 7 días y al
menos un gráfico en escala logarítmica cuando la serie crezca de forma
exponencial.

#### Scenario: Serie suavizada

- **WHEN** se grafica una serie diaria
- **THEN** se muestran la serie original y la media móvil, y se explica qué
  se gana y qué se pierde

#### Scenario: Escala log

- **WHEN** la serie cubre varios órdenes de magnitud
- **THEN** se usa escala logarítmica y se avisa de que las diferencias
  visuales no son lineales

### Requirement: Segmentos por estado/región y por olas

El notebook SHALL segmentar al menos por región (o estado) y por olas
temporales, con una definición explícita de cada ola.

#### Scenario: Segmento por región

- **WHEN** se agrupa por región
- **THEN** se muestra la métrica por región y se explica qué estados la
  componen

#### Scenario: Segmento por ola

- **WHEN** se definen las olas
- **THEN** las fechas de inicio y fin están documentadas y son las mismas
  para todos los estados
