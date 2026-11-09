"""Limpieza básica del dataset del COVID Tracking Project.

Convierte las fechas, elimina duplicados por ``(state, date)`` y guarda el
resultado en ``data/processed/``. Las decisiones de limpieza avanzada
(nulos > 80 %, incrementos negativos, outliers) viven en los issues N2 y N3.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from src.eda.load import PROJECT_ROOT, load_covid_data

DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
PROCESSED_CSV_NAME = "covid_clean.csv"

logger = logging.getLogger(__name__)


def parse_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte ``date`` de ``YYYYMMDD`` a ``datetime64[ns]``.

    Las fechas imposibles se convierten en ``NaT``; el recuento se obtiene con
    ``audit_cleaning`` o mirando los nulos de la columna.
    """
    result = df.copy()
    if pd.api.types.is_datetime64_any_dtype(result["date"]):
        return result

    values = pd.to_numeric(result["date"], errors="coerce").astype("Int64").astype("string")
    result["date"] = pd.to_datetime(values, format="%Y%m%d", errors="coerce")
    return result


def drop_invalid_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina las filas sin fecha válida y reinicia el índice."""
    return df.dropna(subset=["date"]).reset_index(drop=True)


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Conserva un registro por ``(state, date)``.

    Si existe ``dateModified``, se queda con el registro modificado más
    recientemente; si no, con el último del fichero. Mantiene el orden
    original de las filas que sobreviven.
    """
    subset = ["state", "date"]
    if "dateModified" in df.columns:
        ordered = df.sort_values("dateModified", kind="stable")
        keep = ordered.drop_duplicates(subset=subset, keep="last").index
    else:
        keep = df.drop_duplicates(subset=subset, keep="last").index

    return df.loc[sorted(keep)].reset_index(drop=True)


def clean_covid_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica la limpieza básica: fechas válidas y sin duplicados."""
    cleaned = parse_date_column(df)
    cleaned = drop_invalid_dates(cleaned)
    cleaned = remove_duplicates(cleaned)
    return cleaned


def drop_high_null_columns(
    df: pd.DataFrame, threshold: float = 0.80
) -> tuple[pd.DataFrame, list[str]]:
    """Excluye las columnas con más del umbral de nulos.

    Devuelve ``(dataframe sin esas columnas, lista de columnas excluidas)``.
    """
    null_ratio = df.isna().mean()
    excluded = sorted(null_ratio[null_ratio > threshold].index.tolist())
    return df.drop(columns=excluded), excluded


def iqr_bounds(series: pd.Series, factor: float = 1.5) -> tuple[float, float]:
    """Devuelve los límites de Tukey (Q1 − factor·IQR, Q3 + factor·IQR)."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return float(q1 - factor * iqr), float(q3 + factor * iqr)


def mark_outliers(
    df: pd.DataFrame, columns: list[str], factor: float = 1.5
) -> pd.DataFrame:
    """Añade una columna booleana ``is_outlier_<columna>`` por cada variable."""
    result = df.copy()
    for column in columns:
        lower, upper = iqr_bounds(result[column].dropna(), factor=factor)
        result[f"is_outlier_{column}"] = (
            (result[column] < lower) | (result[column] > upper)
        ).fillna(False)
    return result


def clean_advanced(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    """Aplica la limpieza avanzada y devuelve ``(df, auditoría)``.

    Excluye columnas con más del 80 % de nulos, convierte los incrementos
    negativos a ``NaN`` y marca outliers por IQR. No borra filas.
    """
    excluded: list[str]
    df, excluded = drop_high_null_columns(df, threshold=0.80)
    neg_counts = count_negative_increments(df)
    df = apply_negative_strategy(df, strategy="nan")
    df = mark_outliers(df, columns=["positive", "death", "positiveIncrease", "deathIncrease"])
    report = {
        "columns_dropped": excluded,
        "negative_increments": neg_counts,
        "outliers": {
            col: int(df[f"is_outlier_{col}"].sum())
            for col in ["positive", "death", "positiveIncrease", "deathIncrease"]
        },
    }
    return df, report


def save_processed_data(df: pd.DataFrame, path: Path | None = None) -> Path:
    """Guarda el dataset limpio en ``data/processed/`` y devuelve la ruta."""
    target = Path(path) if path is not None else DATA_PROCESSED / PROCESSED_CSV_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target, index=False)
    logger.info("Dataset limpio guardado en %s", target)
    return target


INCREMENT_COLUMNS: tuple[str, ...] = (
    "positiveIncrease",
    "negativeIncrease",
    "totalTestResultsIncrease",
    "deathIncrease",
    "hospitalizedIncrease",
)


def count_negative_increments(df: pd.DataFrame) -> dict[str, int]:
    """Cuenta los valores negativos en las columnas de incremento diario."""
    return {
        column: int((df[column] < 0).sum())
        for column in INCREMENT_COLUMNS
        if column in df.columns
    }


def apply_negative_strategy(
    df: pd.DataFrame, strategy: str = "nan"
) -> pd.DataFrame:
    """Aplica la estrategia elegida a los incrementos negativos.

    ``strategy`` puede ser ``"nan"`` (convierte a NaN), ``"zero"`` (a 0) o
    ``"keep"`` (no toca).
    """
    if strategy not in {"nan", "zero", "keep"}:
        raise ValueError(f"estrategia no válida: {strategy}")

    result = df.copy()
    if strategy == "keep":
        return result

    replacement = float("nan") if strategy == "nan" else 0
    for column in INCREMENT_COLUMNS:
        if column in result.columns:
            mask = result[column] < 0
            result.loc[mask, column] = replacement
    return result


def audit_cleaning(
    raw: pd.DataFrame,
    clean: pd.DataFrame,
    excluded_columns: list[str] | None = None,
    negative_counts: dict[str, int] | None = None,
) -> dict[str, object]:
    """Devuelve las cifras que justifican la limpieza."""
    parsed = parse_date_column(raw)
    report: dict[str, object] = {
        "rows_in": len(raw),
        "rows_out": len(clean),
        "rows_removed": len(raw) - len(clean),
        "invalid_dates": int(parsed["date"].isna().sum()),
        "duplicates": int(raw.duplicated(subset=["state", "date"]).sum()),
        "date_min": clean["date"].min() if len(clean) else None,
        "date_max": clean["date"].max() if len(clean) else None,
        "columns_dropped": excluded_columns or [],
        "negative_increments": negative_counts
        if negative_counts is not None
        else count_negative_increments(raw),
    }
    return report


def build_clean_dataset(
    csv_path: Path | None = None,
    output_path: Path | None = None,
    validate: bool = True,
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Carga, limpia y guarda el dataset. Devuelve ``(df, auditoría)``."""
    raw = load_covid_data(csv_path=csv_path, validate=validate)
    clean = clean_covid_data(raw)
    save_processed_data(clean, path=output_path)
    report = audit_cleaning(raw, clean)
    logger.info("Auditoría de limpieza: %s", report)
    return clean, report
