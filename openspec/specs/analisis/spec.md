# analisis Specification

## Purpose
Convertir el dataset limpio en respuestas verificables a preguntas de
negocio, con estadística descriptiva, comparaciones, correlaciones y
tendencias temporales documentadas en notebooks reproducibles.

## Requirements

### Requirement: Perfilado del dataset

`01_profiling.ipynb` SHALL mostrar la forma, los tipos, los nulos, los
duplicados y un resumen estadístico del dataset limpio.

#### Scenario: Perfil completo

- **WHEN** se ejecuta el notebook de perfilado
- **THEN** se ven `shape`, `info`, `describe`, el porcentaje de nulos por
  columna y el número de duplicados por `(state, date)`

### Requirement: Preguntas de negocio e hipótesis

El notebook SHALL definir al menos 3 preguntas de negocio, cada una con su
hipótesis y la métrica que la responde, antes de cualquier análisis.

#### Scenario: Pregunta con hipótesis

- **WHEN** se lee la sección de preguntas
- **THEN** cada pregunta tiene hipótesis, métrica, periodo y criterio de
  respuesta

### Requirement: Análisis univariado

El notebook SHALL incluir al menos 3 análisis univariados con su gráfico y
su interpretación.

#### Scenario: Variable numérica

- **WHEN** se analiza una variable numérica
- **THEN** se muestra su distribución (histograma o boxplot), medidas de
  centro y dispersión, y una lectura en español

#### Scenario: Variable categórica

- **WHEN** se analiza una variable categórica
- **THEN** se muestra su frecuencia y se explica la categoría dominante

### Requirement: Análisis bivariado

El notebook SHALL incluir al menos 3 relaciones bivariadas con su gráfico y
su interpretación.

#### Scenario: Dos variables numéricas

- **WHEN** se comparan dos variables numéricas
- **THEN** se muestra un scatter con tendencia y se reporta la correlación
  con su limitación

#### Scenario: Variable numérica y categórica

- **WHEN** se compara una numérica con una categórica
- **THEN** se muestra la comparación por grupo y se evita inferir causalidad

### Requirement: Análisis agregado por estado

El notebook SHALL agregar al menos una métrica por estado y SHALL presentar
una tabla ordenada.

#### Scenario: Ranking por estado

- **WHEN** se agrupa por `state`
- **THEN** se muestra una tabla con la métrica, el número de observaciones y
  una advertencia sobre comparar counts sin normalizar

### Requirement: Correlación

El notebook SHALL incluir una matriz de correlación de las variables
numéricas relevantes y SHALL explicar que correlación no implica causalidad.

#### Scenario: Heatmap

- **WHEN** se calcula la correlación
- **THEN** se muestra un heatmap con los coeficientes y se comentan los
  pares más altos y más bajos

### Requirement: Tendencias temporales

El notebook SHALL mostrar al menos una serie temporal y SHALL leerla con
media móvil de 7 días cuando la serie sea diaria.

#### Scenario: Serie diaria

- **WHEN** se grafica una métrica diaria
- **THEN** se muestra la serie original y la media móvil de 7 días, y se
  explica el efecto del fin de semana

### Requirement: Notebook narrativo v1

`02_eda.ipynb` SHALL ejecutarse de arriba abajo y SHALL tener una sección de
conclusiones que responda a las 3 preguntas.

#### Scenario: Ejecución limpia

- **WHEN** se ejecuta el notebook en un entorno limpio
- **THEN** termina sin errores y las conclusiones citan cifras de las celdas
  anteriores
