"""Tests de la limpieza básica."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.eda.clean import (
    audit_cleaning,
    build_clean_dataset,
    clean_covid_data,
    drop_invalid_dates,
    parse_date_column,
    remove_duplicates,
    save_processed_data,
)

FIXTURE = Path(__file__).parent / "fixtures" / "covid_sample.csv"


def make_frame(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def test_parse_date_column_converts_yyyymmdd() -> None:
    df = make_frame([{"state": "AK", "date": 20200501}])

    result = parse_date_column(df)

    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert result.loc[0, "date"] == pd.Timestamp("2020-05-01")


def test_parse_date_column_marks_impossible_dates_as_nat() -> None:
    df = make_frame([{"state": "AK", "date": 20201301}])

    result = parse_date_column(df)

    assert pd.isna(result.loc[0, "date"])


def test_parse_date_column_is_idempotent() -> None:
    df = make_frame([{"state": "AK", "date": 20200501}])

    once = parse_date_column(df)
    twice = parse_date_column(once)

    pd.testing.assert_frame_equal(once, twice)


def test_drop_invalid_dates_removes_nat_rows() -> None:
    df = make_frame(
        [
            {"state": "AK", "date": pd.Timestamp("2020-05-01")},
            {"state": "AK", "date": pd.NaT},
        ]
    )

    result = drop_invalid_dates(df)

    assert len(result) == 1
    assert result.index.tolist() == [0]


def test_remove_duplicates_keeps_latest_date_modified() -> None:
    df = make_frame(
        [
            {"state": "AK", "date": 20200501, "value": 1, "dateModified": "2020-05-01T10:00:00Z"},
            {"state": "AK", "date": 20200501, "value": 2, "dateModified": "2020-05-02T10:00:00Z"},
            {"state": "AK", "date": 20200502, "value": 3, "dateModified": "2020-05-02T11:00:00Z"},
        ]
    )

    result = remove_duplicates(df)

    assert len(result) == 2
    assert result.loc[result["date"] == 20200501, "value"].item() == 2


def test_remove_duplicates_without_metadata_keeps_last() -> None:
    df = make_frame(
        [
            {"state": "AK", "date": 20200501, "value": 1},
            {"state": "AK", "date": 20200501, "value": 2},
        ]
    )

    result = remove_duplicates(df)

    assert len(result) == 1
    assert result.loc[0, "value"] == 2


def test_clean_covid_data_does_not_mutate_input() -> None:
    df = pd.read_csv(FIXTURE)
    original = df.copy(deep=True)

    clean_covid_data(df)

    pd.testing.assert_frame_equal(df, original)


def test_clean_covid_data_removes_invalid_and_duplicates() -> None:
    df = make_frame(
        [
            {"state": "AK", "date": 20200501, "value": 1},
            {"state": "AK", "date": 20200501, "value": 2},
            {"state": "AK", "date": 20201301, "value": 3},
        ]
    )

    result = clean_covid_data(df)

    assert len(result) == 1
    assert result.loc[0, "value"] == 2


def test_audit_cleaning_reports_counts() -> None:
    raw = make_frame(
        [
            {"state": "AK", "date": 20200501, "value": 1},
            {"state": "AK", "date": 20200501, "value": 2},
            {"state": "AK", "date": 20201301, "value": 3},
        ]
    )
    clean = clean_covid_data(raw)

    report = audit_cleaning(raw, clean)

    assert report["rows_in"] == 3
    assert report["rows_out"] == 1
    assert report["invalid_dates"] == 1
    assert report["duplicates"] == 1


def test_save_processed_data_writes_csv(tmp_path: Path) -> None:
    df = pd.read_csv(FIXTURE)
    target = tmp_path / "nested" / "clean.csv"

    result = save_processed_data(df, path=target)

    assert result == target
    assert target.is_file()
    assert len(pd.read_csv(target)) == len(df)


def test_build_clean_dataset_end_to_end(tmp_path: Path) -> None:
    output = tmp_path / "covid_clean.csv"

    clean, report = build_clean_dataset(csv_path=FIXTURE, output_path=output, validate=False)

    assert output.is_file()
    assert len(clean) == 12
    assert report["rows_in"] == 12
    assert report["rows_out"] == 12
    assert pd.api.types.is_datetime64_any_dtype(clean["date"])


@pytest.mark.parametrize("estado", ["AK", "AL", "CA", "NY"])
def test_fixture_has_expected_states(estado: str) -> None:
    df = pd.read_csv(FIXTURE)

    assert estado in set(df["state"])
