"""Carga del dataset del COVID Tracking Project.

El fichero crudo se guarda en ``data/raw/`` y no se versiona. La función
``load_covid_data`` descarga solo cuando no hay copia local y valida el
esquema antes de devolver el ``DataFrame``.
"""

from __future__ import annotations

import logging
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw"

DEFAULT_CSV_NAME = "covid_tracking_states_daily.csv"
COVID_DATA_URL = (
    "https://raw.githubusercontent.com/COVID19Tracking/"
    "covid-tracking-data/master/data/states_daily_4pm_et.csv"
)

REQUIRED_COLUMNS: tuple[str, ...] = (
    "date",
    "state",
    "positive",
    "death",
    "totalTestResults",
)
MIN_ROWS = 1_000
MIN_COLUMNS = 8
DOWNLOAD_CHUNK_SIZE = 1 << 20

logger = logging.getLogger(__name__)


def download_covid_data(
    destination: Path | None = None,
    url: str = COVID_DATA_URL,
    timeout: float = 60.0,
) -> Path:
    """Descarga el CSV crudo de forma atómica y devuelve su ruta.

    Escribe primero en un fichero ``.part`` y solo lo renombra si la descarga
    termina bien. Si falla, no deja un fichero a medias.
    """
    target = Path(destination) if destination is not None else DATA_RAW / DEFAULT_CSV_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(target.suffix + ".part")

    try:
        with urlopen(url, timeout=timeout) as response, partial.open("wb") as handle:
            while chunk := response.read(DOWNLOAD_CHUNK_SIZE):
                handle.write(chunk)
        if partial.stat().st_size == 0:
            raise ValueError("la respuesta está vacía")
        partial.replace(target)
    except (OSError, URLError, ValueError) as exc:
        partial.unlink(missing_ok=True)
        raise RuntimeError(f"No se pudo descargar el dataset desde {url}: {exc}") from exc

    logger.info("Dataset descargado en %s", target)
    return target


def validate_schema(
    df: pd.DataFrame,
    min_rows: int = MIN_ROWS,
    min_columns: int = MIN_COLUMNS,
    required_columns: tuple[str, ...] = REQUIRED_COLUMNS,
) -> None:
    """Comprueba que el dataset tiene el tamaño y las columnas mínimas.

    Lanza ``ValueError`` con la lista completa de problemas encontrados.
    """
    problemas: list[str] = []

    faltantes = [column for column in required_columns if column not in df.columns]
    if faltantes:
        problemas.append(f"faltan columnas obligatorias: {', '.join(faltantes)}")

    if len(df) < min_rows:
        problemas.append(f"hay {len(df)} filas y se exigen al menos {min_rows}")

    if df.shape[1] < min_columns:
        problemas.append(f"hay {df.shape[1]} columnas y se exigen al menos {min_columns}")

    if problemas:
        raise ValueError("Dataset inválido: " + "; ".join(problemas))


def load_covid_data(
    csv_path: Path | None = None,
    url: str = COVID_DATA_URL,
    force_download: bool = False,
    validate: bool = True,
) -> pd.DataFrame:
    """Carga el dataset, descargándolo solo si no existe la copia local.

    ``force_download=True`` ignora la caché y vuelve a descargar. No modifica
    nunca el contenido de ``data/raw/`` salvo para crear la copia que falta.
    """
    path = Path(csv_path) if csv_path is not None else DATA_RAW / DEFAULT_CSV_NAME

    if force_download or not path.exists():
        path = download_covid_data(path, url=url)

    try:
        df = pd.read_csv(path, dtype={"state": "string", "fips": "string"})
    except pd.errors.EmptyDataError as exc:
        raise RuntimeError(f"El fichero {path} está vacío") from exc

    if validate:
        validate_schema(df)

    return df
