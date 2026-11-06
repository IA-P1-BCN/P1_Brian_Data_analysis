---
name: covid-data-dictionary
description: Diccionario y reglas del COVID Tracking Project (columnas, formato de fecha YYYYMMDD, incrementos negativos, columnas con >80 % de nulos, abreviaturas de estado, merge con población y métricas por 100k). Úsala al cargar, limpiar, agregar o interpretar cualquier columna del dataset.
---

# COVID Tracking Project · diccionario y reglas

## Fuente

- Dataset: **COVID Tracking Project** (Estados Unidos), serie diaria por estado.
- Granularidad: una fila por `state` y `date`.
- Cobertura: 50 estados + DC + territorios (PR, GU, VI, AS, MP).
- Los datos son **acumulados** en varias columnas y **diarios** en las que
  terminan en `Increase`.

## Columnas principales

| Columna | Tipo | Significado |
|---|---|---|
| `date` | entero `YYYYMMDD` | Fecha del registro |
| `state` | texto | Abreviatura de dos letras |
| `positive` | entero | Casos positivos acumulados |
| `negative` | entero | Tests negativos acumulados |
| `pending` | entero | Tests pendientes |
| `totalTestResults` | entero | Total de tests (positivos + negativos) |
| `hospitalizedCurrently` | entero | Hospitalizados actuales |
| `hospitalizedCumulative` | entero | Hospitalizados acumulados |
| `inIcuCurrently` | entero | En UCI actuales |
| `inIcuCumulative` | entero | En UCI acumulados |
| `onVentilatorCurrently` | entero | Con ventilador actuales |
| `onVentilatorCumulative` | entero | Con ventilador acumulados |
| `recovered` | entero | Recuperados |
| `death` | entero | Muertes acumuladas |
| `deathConfirmed` | entero | Muertes confirmadas |
| `deathProbable` | entero | Muertes probables |
| `hospitalized` | entero | Hospitalizaciones acumuladas (histórico) |
| `hospitalizedDischarged` | entero | Altas hospitalarias |
| `positiveIncrease` | entero | Nuevos positivos del día |
| `negativeIncrease` | entero | Nuevos negativos del día |
| `totalTestResultsIncrease` | entero | Nuevos tests del día |
| `deathIncrease` | entero | Nuevas muertes del día |
| `hospitalizedIncrease` | entero | Nuevas hospitalizaciones del día |
| `dataQualityGrade` | texto | Calidad declarada (A+, A, B, C…) |
| `fips` | texto | Código FIPS del estado |

## Reglas de limpieza obligatorias

### 1. Fechas

`date` viene como entero `YYYYMMDD` (por ejemplo `20200501`). Convertir con:

```python
df["date"] = pd.to_datetime(df["date"].astype(str), format="%Y%m%d", errors="coerce")
```

Si `errors="coerce"` produce nulos, cuéntalos y documenta el descarte. No
inventes fechas.

### 2. Incrementos negativos

`positiveIncrease`, `negativeIncrease`, `totalTestResultsIncrease`,
`deathIncrease` y `hospitalizedIncrease` pueden ser **negativos** por
correcciones de reporting. No los borres sin más:

- Cuenta cuántos hay por columna y por estado.
- Documenta la decisión: mantener, poner a `NaN` o imputar a 0.
- Si se usa la serie diaria para una media móvil, `NaN` es más honesto que 0.
- Nunca los uses para calcular totales acumulados.

### 3. Columnas con >80 % de nulos

Calcula el porcentaje de nulos por columna. Las que superen el **80 %** se
excluyen del análisis principal y se documentan en una tabla:

```python
missing = df.isna().mean().sort_values(ascending=False)
dropped = missing[missing > 0.80]
```

No las elimines del CSV crudo; elimínalas del dataframe de análisis y explica
por qué.

### 4. Duplicados

La clave es `(state, date)`. Si hay duplicados, quédate con el registro de
mayor calidad (`dataQualityGrade`) o con el último, y documenta el criterio.

### 5. Abreviaturas y población

- `state` son abreviaturas de dos letras (`CA`, `TX`, `NY`…).
- Para el merge con población, usa una tabla con `state` y `population`.
- Verifica que el merge no pierda estados ni duplique filas:

```python
assert set(df["state"]) == set(pop["state"])
assert df.shape[0] == before
```

## Métricas derivadas

```python
df["positivity"] = df["positive"] / df["totalTestResults"]
df["death_rate"] = df["death"] / df["positive"]
df["positive_per_100k"] = df["positive"] / df["population"] * 100_000
df["death_per_100k"] = df["death"] / df["population"] * 100_000
df["tests_per_100k"] = df["totalTestResults"] / df["population"] * 100_000
```

Reglas:

- Si el denominador es 0 o nulo, el ratio es `NaN`, no `inf`.
- Un ratio por 100k solo es comparable entre estados si la población es
  correcta y la fecha es la misma.
- Para series diarias, usa `*Increase`, no la diferencia de acumulados
  (hay correcciones que rompen la resta).

## Advertencias de interpretación

- **No son casos reales**, son casos reportados. El subregistro varía por
  estado y por semana.
- Los fines de semana y festivos bajan el reporting; por eso la media móvil
  de 7 días es la forma correcta de leer tendencias.
- `totalTestResults` cambió de definición a lo largo de la pandemia.
- Comparar estados sin normalizar por población es engañoso.
- No se puede inferir causalidad de una serie temporal observacional.

## Segundo dataset: población

- Fuente recomendada: U.S. Census Bureau (población por estado).
- Guardar en `data/external/` con nombre versionado.
- Columnas mínimas: `state` (abreviatura o nombre) y `population`.
- Si usas nombres completos, crea un mapa nombre → abreviatura y valídalo.
