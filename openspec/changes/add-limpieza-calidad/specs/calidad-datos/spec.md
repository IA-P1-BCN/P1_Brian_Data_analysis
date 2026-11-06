# Spec Delta

## Purpose

Convertir el dataset crudo en un dataset limpio, documentado y reproducible,
de modo que el análisis posterior no dependa de decisiones implícitas ni de
valores anómalos sin tratar.

## ADDED Requirements

### Requirement: Fechas normalizadas

`clean.py` SHALL convertir la columna `date` de entero `YYYYMMDD` a
`datetime64[ns]` y SHALL informar del número de fechas inválidas.

#### Scenario: Fecha válida

- **WHEN** `date` vale `20200501`
- **THEN** la columna resultante contiene `2020-05-01 00:00:00`

#### Scenario: Fecha inválida

- **WHEN** `date` no tiene 8 dígitos o no existe en el calendario
- **THEN** la fila se marca como inválida, se cuenta y se documenta

### Requirement: Duplicados por estado y fecha

`clean.py` SHALL eliminar los duplicados de `(state, date)` conservando un
único registro y SHALL documentar el criterio de selección.

#### Scenario: Duplicado exacto

- **WHEN** hay dos filas con el mismo `state` y `date`
- **THEN** queda una sola fila y el recuento de eliminadas se registra

#### Scenario: Duplicado con distinta calidad

- **WHEN** las dos filas difieren en `dataQualityGrade`
- **THEN** se conserva la de mayor calidad y se explica en el informe

### Requirement: Columnas con más del 80 % de nulos

`clean.py` SHALL calcular el porcentaje de nulos por columna y SHALL excluir
del dataframe de análisis las que superen el 80 %, documentando la lista.

#### Scenario: Columna mayoritariamente nula

- **WHEN** una columna tiene más del 80 % de nulos
- **THEN** se excluye del análisis y aparece en la tabla de decisiones

#### Scenario: Columna con nulos moderados

- **WHEN** una columna tiene entre 0 % y 80 % de nulos
- **THEN** se conserva y se documenta su tratamiento

### Requirement: Incrementos negativos

`clean.py` SHALL detectar los valores negativos en `positiveIncrease`,
`negativeIncrease`, `totalTestResultsIncrease`, `deathIncrease` y
`hospitalizedIncrease` y SHALL aplicar una decisión explícita y documentada.

#### Scenario: Incremento negativo

- **WHEN** `deathIncrease` es negativo
- **THEN** se cuenta, se conserva o se convierte en `NaN` según la decisión
  documentada, nunca se borra silenciosamente

#### Scenario: Recuento por estado

- **WHEN** se ejecuta la auditoría
- **THEN** se muestra cuántos negativos hay por columna y por estado

### Requirement: Outliers con IQR

`clean.py` SHALL calcular los límites de Tukey (Q1 − 1,5·IQR y Q3 + 1,5·IQR)
para las variables numéricas relevantes y SHALL documentar cuántos valores
quedan fuera.

#### Scenario: Valor atípico

- **WHEN** un valor está fuera de los límites de Tukey
- **THEN** se marca como outlier y se decide si se conserva, se recorta o se
  excluye, con justificación

### Requirement: Auditoría de calidad

El proyecto SHALL producir una tabla de auditoría con filas iniciales,
filas finales, columnas eliminadas, duplicados, fechas inválidas y negativos
por columna.

#### Scenario: Cierre de la limpieza

- **WHEN** termina `clean.py`
- **THEN** la auditoría se guarda en `reports/` o se muestra en el notebook
  y permite reconstruir qué se hizo
