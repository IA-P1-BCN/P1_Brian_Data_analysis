"""Tests de la ingesta del dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.eda import load
from src.eda.load import (
    REQUIRED_COLUMNS,
    load_covid_data,
    validate_schema,
)

FIXTURE = Path(__file__).parent / "fixtures" / "covid_sample.csv"


def test_load_reads_local_file(tmp_path: Path) -> None:
    csv_path = tmp_path / "covid.csv"
    csv_path.write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")

    df = load_covid_data(csv_path=csv_path, validate=False)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 12
    assert set(REQUIRED_COLUMNS).issubset(df.columns)


def test_load_uses_cache_without_downloading(tmp_path: Path, monkeypatch) -> None:
    csv_path = tmp_path / "covid.csv"
    csv_path.write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")

    def falla(*args, **kwargs):  # pragma: no cover - solo se llama si hay bug
        raise AssertionError("no debería descargar si el fichero existe")

    monkeypatch.setattr(load, "download_covid_data", falla)

    df = load_covid_data(csv_path=csv_path, validate=False)

    assert len(df) == 12


def test_download_failure_leaves_no_partial_file(tmp_path: Path, monkeypatch) -> None:
    destino = tmp_path / "covid.csv"

    def url_rota(*args, **kwargs):
        from urllib.error import URLError

        raise URLError("sin red")

    monkeypatch.setattr(load, "urlopen", url_rota)

    with pytest.raises(RuntimeError, match="No se pudo descargar"):
        load.download_covid_data(destination=destino)

    assert not destino.exists()
    assert list(tmp_path.glob("*.part")) == []


def test_download_writes_file_atomically(tmp_path: Path, monkeypatch) -> None:
    destino = tmp_path / "covid.csv"
    origen = FIXTURE.read_bytes()

    class RespuestaFalsa:
        def __init__(self, payload: bytes) -> None:
            self._payload = payload
            self._leido = False

        def __enter__(self):
            return self

        def __exit__(self, *args) -> None:
            return None

        def read(self, size: int = -1) -> bytes:
            if self._leido:
                return b""
            self._leido = True
            return self._payload

    monkeypatch.setattr(load, "urlopen", lambda *a, **k: RespuestaFalsa(origen))

    ruta = load.download_covid_data(destination=destino)

    assert ruta == destino
    assert destino.read_bytes() == origen
    assert list(tmp_path.glob("*.part")) == []


def test_validate_schema_accepts_valid_dataset() -> None:
    df = pd.read_csv(FIXTURE)
    validate_schema(df, min_rows=5)


def test_validate_schema_reports_missing_columns() -> None:
    df = pd.read_csv(FIXTURE).drop(columns=["death", "totalTestResults"])

    with pytest.raises(ValueError, match="death, totalTestResults"):
        validate_schema(df, min_rows=5)


def test_validate_schema_reports_too_few_rows() -> None:
    df = pd.read_csv(FIXTURE)

    with pytest.raises(ValueError, match="filas"):
        validate_schema(df, min_rows=1_000)


def test_validate_schema_reports_too_few_columns() -> None:
    df = pd.read_csv(FIXTURE)[["date", "state", "positive", "death", "totalTestResults"]]

    with pytest.raises(ValueError, match="columnas"):
        validate_schema(df, min_rows=5, min_columns=8)
