---
name: eda-convenciones
description: Convenciones del proyecto EDA (estructura de src/eda/, nombres, imports, rutas, tests, ruff, separación entre lógica y notebook y reglas de commits). Úsala al escribir o revisar código Python, tests o cualquier archivo de src/.
---

# Convenciones del proyecto EDA

## Estructura

```text
src/eda/
├── __init__.py
├── load.py        descarga, caché, lectura y validación del dataset
├── clean.py       tipos, fechas, nulos, duplicados, outliers
├── features.py    ratios, media móvil, log, segmentos
└── viz.py         funciones de gráficos reutilizables
```

Regla: **si una celda del notebook se repite dos veces, se mueve a `src/eda/`**.

## Nombres

| Elemento | Convención | Ejemplo |
|---|---|---|
| Módulo | `snake_case` | `clean.py` |
| Función | verbo + objeto | `clean_covid_data()` |
| Variable | `snake_case` | `daily_cases` |
| Constante | `UPPER_SNAKE` | `RAW_DATA_PATH` |
| Columna | `snake_case` en inglés | `positive_per_100k` |
| Test | `test_<comportamiento>` | `test_drops_columns_over_80_pct_null` |

## Funciones

- Type hints en la firma.
- Docstring corta en español (una o dos líneas).
- Sin `print` de depuración; devuelve valores o usa `logging`.
- Sin efectos secundarios ocultos: si escribe un fichero, que se vea en el
  nombre (`save_processed_data`).
- Preferir vectorización de pandas a bucles.
- No usar `inplace=True` salvo justificación.

```python
def clean_covid_data(df: pd.DataFrame, max_null_ratio: float = 0.80) -> pd.DataFrame:
    """Limpia tipos, fechas, duplicados y columnas con exceso de nulos."""
```

## Rutas

- Usar `pathlib.Path`, nunca rutas absolutas.
- Un único punto de entrada para la raíz del proyecto:

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
REPORTS = PROJECT_ROOT / "reports"
```

- `data/raw/` es de solo lectura.
- `data/processed/` es salida reproducible; no se versiona.

## Tests

- `pytest`, sin clases salvo que aporten.
- Un test por comportamiento observable.
- Datos de prueba pequeños y explícitos, no el CSV completo.
- Los tests no dependen de red.
- Nombres que digan qué rompe el test.

```python
def test_date_column_is_datetime():
    result = load_covid_data(sample_df)
    assert pd.api.types.is_datetime64_any_dtype(result["date"])
```

## Calidad

```bash
ruff check .
ruff format .
pytest -q
```

- `ruff` manda sobre el estilo; no se discute en la PR.
- Las funciones públicas tienen test.
- No se commitean notebooks con outputs ni datos crudos.

## Idioma

- Código, nombres y docstrings técnicos: **inglés**.
- Comentarios de negocio, documentación y mensajes de PR: **español**.

## Git

- Rama: `feat/N-slug`, `fix/N-slug`, `docs/N-slug`, `test/N-slug`.
- Commit: Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- Un commit = un cambio coherente; no mezclar limpieza con features.
- PR con `Closes #N` y CI verde.
- Squash merge a `develop`.
