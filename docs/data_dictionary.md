# Diccionario de datos · COVID Tracking Project

## Fuente

| Campo | Valor |
|---|---|
| Dataset | COVID Tracking Project · States Daily |
| URL | `https://raw.githubusercontent.com/COVID19Tracking/covid-tracking-data/master/data/states_daily_4pm_et.csv` |
| Fichero local | `data/raw/covid_tracking_states_daily.csv` |
| Descarga | `src.eda.load.load_covid_data()` |
| Periodo | 2020-01-13 → 2021-03-07 |
| Granularidad | una fila por `state` y `date` |
| Filas | 20 780 |
| Columnas | 56 |
| Cobertura | 56 códigos: 50 estados, DC y territorios (PR, GU, VI, AS, MP) |
| Duplicados `(state, date)` | 0 en la copia descargada el 2026-11-06 |

El proyecto cerró en marzo de 2021. El CSV es la **última foto** publicada, no
un feed en vivo. Cualquier cifra del informe describe ese periodo, no la
situación actual.

## Cómo se carga

```python
from src.eda.load import load_covid_data

df = load_covid_data()  # descarga si no hay caché
df = load_covid_data(force_download=True)  # fuerza una copia nueva
```

`load_covid_data()` valida que haya al menos 1000 filas, 8 columnas y las
columnas obligatorias `date`, `state`, `positive`, `death` y
`totalTestResults`.

## Tipos

- `date` llega como **entero** `YYYYMMDD` (`20200501`). Se convierte a
  `datetime64[ns]` en `clean.py`.
- Las columnas de conteo llegan como `float64` porque pueden tener nulos;
  se convierten a `Int64` cuando el análisis lo permita.
- `state` y `fips` se leen como texto para no perder ceros a la izquierda
  (`fips="02"` es Alaska).
- `totalTestResultsSource`, `lastUpdateEt`, `dateModified`, `checkTimeEt`,
  `dateChecked` y `hash` son texto.

## Columnas

### Identificadores

| Columna | Tipo | Significado |
|---|---|---|
| `date` | entero `YYYYMMDD` | Fecha del registro |
| `state` | texto | Abreviatura de dos letras |
| `fips` | texto | Código FIPS del estado o territorio |

### Casos

| Columna | Tipo | Unidad | Significado |
|---|---|---|---|
| `positive` | entero | casos | Positivos acumulados (PCR + antígeno según el estado) |
| `probableCases` | entero | casos | Casos probables acumulados |
| `positiveCasesViral` | entero | casos | Positivos confirmados por prueba viral |
| `positiveIncrease` | entero | casos/día | Nuevos positivos del día |
| `total` | entero | casos | `positive + probableCases` cuando existe |

### Tests

| Columna | Tipo | Unidad | Significado |
|---|---|---|---|
| `negative` | entero | tests | Tests negativos acumulados |
| `pending` | entero | tests | Tests pendientes de resultado |
| `totalTestResults` | entero | tests | Total de tests (positivos + negativos) |
| `totalTestResultsSource` | texto | — | Qué columnas componen el total |
| `totalTestResultsIncrease` | entero | tests/día | Nuevos tests del día |
| `negativeIncrease` | entero | tests/día | Nuevos negativos del día |
| `posNeg` | entero | tests | `positive + negative` |
| `totalTestsViral` | entero | tests | Tests virales acumulados |
| `positiveTestsViral` | entero | tests | Tests virales positivos |
| `negativeTestsViral` | entero | tests | Tests virales negativos |
| `totalTestsPeopleViral` | entero | personas | Personas testeadas con prueba viral |
| `totalTestEncountersViral` | entero | tests | Encuentros de test viral (incluye repetidos) |
| `totalTestsAntibody` | entero | tests | Tests de anticuerpos |
| `positiveTestsAntibody` | entero | tests | Anticuerpos positivos |
| `negativeTestsAntibody` | entero | tests | Anticuerpos negativos |
| `totalTestsPeopleAntibody` | entero | personas | Personas con test de anticuerpos |
| `positiveTestsPeopleAntibody` | entero | personas | Personas con anticuerpos positivos |
| `negativeTestsPeopleAntibody` | entero | personas | Personas con anticuerpos negativos |
| `totalTestsAntigen` | entero | tests | Tests de antígeno |
| `positiveTestsAntigen` | entero | tests | Antígenos positivos |
| `totalTestsPeopleAntigen` | entero | personas | Personas con test de antígeno |
| `positiveTestsPeopleAntigen` | entero | personas | Personas con antígeno positivo |

`totalTestResults` **cambió de definición** a lo largo del periodo: según el
estado y la fecha puede incluir tests virales, anticuerpos o encuentros. No es
una serie homogénea y no debe compararse sin revisar
`totalTestResultsSource`.

### Hospitalizaciones

| Columna | Tipo | Unidad | Significado |
|---|---|---|---|
| `hospitalizedCurrently` | entero | personas | Hospitalizados en la fecha |
| `hospitalizedCumulative` | entero | personas | Hospitalizados acumulados |
| `hospitalized` | entero | personas | Hospitalizaciones acumuladas (histórico) |
| `hospitalizedIncrease` | entero | personas/día | Nuevas hospitalizaciones del día |
| `hospitalizedDischarged` | entero | personas | Altas hospitalarias acumuladas |
| `inIcuCurrently` | entero | personas | En UCI en la fecha |
| `inIcuCumulative` | entero | personas | En UCI acumulados |
| `onVentilatorCurrently` | entero | personas | Con ventilador en la fecha |
| `onVentilatorCumulative` | entero | personas | Con ventilador acumulados |

### Muertes

| Columna | Tipo | Unidad | Significado |
|---|---|---|---|
| `death` | entero | personas | Muertes acumuladas |
| `deathConfirmed` | entero | personas | Muertes confirmadas por prueba |
| `deathProbable` | entero | personas | Muertes probables (sin prueba) |
| `deathIncrease` | entero | personas/día | Nuevas muertes del día |

### Metadatos y calidad

| Columna | Tipo | Significado |
|---|---|---|
| `lastUpdateEt` | texto | Última actualización declarada por el estado (hora del Este) |
| `dateModified` | texto | Fecha de modificación del registro |
| `checkTimeEt` | texto | Hora de comprobación del dato |
| `dateChecked` | texto | Fecha de la comprobación |
| `hash` | texto | Hash del registro original |
| `dataQualityGrade` | texto | Calidad declarada del dato |
| `grade` | texto | Nota de calidad calculada |
| `commercialScore` | número | Puntuación del componente comercial |
| `negativeRegularScore` | número | Puntuación de negativos regulares |
| `negativeScore` | número | Puntuación de negativos |
| `positiveScore` | número | Puntuación de positivos |
| `score` | número | Puntuación global |

## Columnas con más del 80 % de nulos

Calculado sobre la copia del 2026-11-06. Se excluyen del análisis principal
en `clean.py` y se documentan en la tabla de decisiones.

| Columna | % nulos |
|---|---|
| `dataQualityGrade` | 100,0 % |
| `grade` | 100,0 % |
| `positiveTestsPeopleAntigen` | 97,0 % |
| `negativeTestsPeopleAntibody` | 95,3 % |
| `totalTestsPeopleAntigen` | 95,2 % |
| `positiveTestsPeopleAntibody` | 94,7 % |
| `onVentilatorCumulative` | 93,8 % |
| `negativeTestsAntibody` | 93,0 % |
| `pending` | 89,7 % |
| `totalTestsPeopleAntibody` | 89,4 % |
| `positiveTestsAntigen` | 89,3 % |
| `hospitalizedDischarged` | 85,2 % |
| `positiveTestsAntibody` | 83,9 % |
| `totalTestsAntigen` | 83,5 % |
| `inIcuCumulative` | 81,8 % |

**Consecuencia:** `dataQualityGrade` está vacía al 100 %, así que el criterio
"conservar el duplicado de mayor calidad" no se puede aplicar con esta copia.
Si hay duplicados, se resolverán por fecha de modificación o por orden, y se
documentará.

## Reglas de interpretación

1. **No son casos reales, son casos reportados.** El subregistro varía por
   estado y por semana.
2. **Los incrementos pueden ser negativos.** En esta copia hay 24 negativos en
   `positiveIncrease`, 75 en `negativeIncrease`, 52 en
   `totalTestResultsIncrease`, 73 en `deathIncrease` y 88 en
   `hospitalizedIncrease`. Son correcciones de reporting, no errores de
   limpieza. Se cuentan y se tratan con una decisión explícita.
3. **Fines de semana y festivos** bajan el reporting. Para tendencia se usa
   media móvil de 7 días.
4. **Los counts no son comparables entre estados** sin normalizar por
   población.
5. **`totalTestResults` no es homogéneo** en el tiempo.
6. **No se puede inferir causalidad** de una serie temporal observacional.

## Métricas derivadas

| Métrica | Fórmula | Unidad |
|---|---|---|
| `positivity` | `positive / totalTestResults` | proporción 0–1 |
| `death_rate` | `death / positive` | proporción 0–1 |
| `positive_per_100k` | `positive / population * 100_000` | casos por 100k |
| `death_per_100k` | `death / population * 100_000` | muertes por 100k |
| `tests_per_100k` | `totalTestResults / population * 100_000` | tests por 100k |
| `positive_ma7` | media móvil de 7 días de `positiveIncrease` por estado | casos/día |

Reglas:

- Denominador 0 o nulo → `NaN`, nunca `inf`.
- La media móvil se calcula por estado, nunca sobre el dataset completo.
- Los ratios por 100k necesitan la población del estado y un merge validado.

## Segunda fuente: población

`data/external/population.csv` con columnas `state` y `population`. Se usa
para los ratios por 100k. El merge debe ser `many_to_one`, no debe perder
estados y no debe duplicar filas.

## Limitaciones del diccionario

- Las descripciones se basan en la documentación pública del COVID Tracking
  Project y en la inspección del CSV; no sustituyen al diccionario original.
- Los porcentajes de nulos son de esta copia concreta y cambian si se
  descarga otra versión.
- `dataQualityGrade` y `grade` están vacías: no se puede evaluar la calidad
  declarada.
