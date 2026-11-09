"""Features derivadas del dataset del COVID Tracking Project.

Incluye métricas de positividad, tasas de mortalidad, media móvil y, cuando
está disponible la población por estado, ratios por 100k habitantes.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from src.eda.load import PROJECT_ROOT

DATA_EXTERNAL = PROJECT_ROOT / "data" / "external"
POPULATION_CSV_NAME = "population.csv"

logger = logging.getLogger(__name__)


def add_positivity(df: pd.DataFrame) -> pd.DataFrame:
    """Añade ``positivity = positive / totalTestResults`` (NaN si denom. 0)."""
    result = df.copy()
    denominator = result["totalTestResults"].replace(0, float("nan"))
    result["positivity"] = result["positive"] / denominator
    return result


def add_death_rate(df: pd.DataFrame) -> pd.DataFrame:
    """Añade ``death_rate = death / positive`` (NaN si denom. 0)."""
    result = df.copy()
    denominator = result["positive"].replace(0, float("nan"))
    result["death_rate"] = result["death"] / denominator
    return result


def add_daily_ma7(
    df: pd.DataFrame,
    group_col: str = "state",
    value_col: str = "positiveIncrease",
    window: int = 7,
) -> pd.DataFrame:
    """Añade la media móvil de ``window`` días de ``value_col`` por grupo."""
    result = df.copy()
    if "date" in result.columns:
        result = result.sort_values([group_col, "date"], kind="stable")
    result[f"{value_col}_ma{window}"] = result.groupby(group_col)[value_col].transform(
        lambda series: series.rolling(window, min_periods=window).mean()
    )
    return result


def add_base_features(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica las features base disponibles sin población externa."""
    result = add_positivity(df)
    result = add_death_rate(result)
    result = add_daily_ma7(result)
    return result


def merge_population(df: pd.DataFrame, population_path: Path | None = None) -> pd.DataFrame:
    """Integra la población por estado con validación estricta.

    Lanza ``ValueError`` si falta algún estado o si el merge cambia el número
    de filas.
    """
    path = (
        Path(population_path)
        if population_path is not None
        else DATA_EXTERNAL / POPULATION_CSV_NAME
    )
    if not path.exists():
        raise FileNotFoundError(f"No existe la tabla de población: {path}")

    population = pd.read_csv(path)
    if not {"state", "population"}.issubset(population.columns):
        raise ValueError("population.csv debe tener columnas 'state' y 'population'")

    before_rows = len(df)
    before_states = set(df["state"].dropna().unique())

    merged = df.merge(
        population[["state", "population"]], on="state", how="left", validate="many_to_one"
    )

    missing = before_states - set(population["state"].dropna().unique())
    if missing:
        raise ValueError(f"Faltan estados en population.csv: {sorted(missing)}")
    if len(merged) != before_rows:
        raise ValueError(f"El merge cambió el número de filas: {before_rows} -> {len(merged)}")
    if merged["population"].isna().any():
        raise ValueError("Hay estados sin población tras el merge")

    return merged


def add_per_capita(df: pd.DataFrame) -> pd.DataFrame:
    """Añade ratios por 100k habitantes (requiere columna ``population``)."""
    if "population" not in df.columns:
        raise ValueError("Falta la columna 'population': ejecuta merge_population primero")

    result = df.copy()
    population = result["population"].replace(0, float("nan"))
    result["positive_per_100k"] = result["positive"] / population * 100_000
    result["death_per_100k"] = result["death"] / population * 100_000
    if "totalTestResults" in result.columns:
        result["tests_per_100k"] = result["totalTestResults"] / population * 100_000
    return result


def add_all_features(df: pd.DataFrame, population_path: Path | None = None) -> pd.DataFrame:
    """Aplica features base y, si hay población, ratios por 100k."""
    result = add_base_features(df)
    try:
        result = merge_population(result, population_path=population_path)
        result = add_per_capita(result)
    except (FileNotFoundError, ValueError):
        logger.info("Población no disponible; se omiten los ratios por 100k")
    return result
