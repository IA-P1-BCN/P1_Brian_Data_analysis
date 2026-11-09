"""Tests de las features derivadas."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.eda.features import (
    add_all_features,
    add_base_features,
    add_daily_ma7,
    add_death_rate,
    add_per_capita,
    add_positivity,
    merge_population,
)

FIXTURE = Path(__file__).parent / "fixtures" / "covid_sample.csv"


def population_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "state": ["AK", "AL", "CA", "NY"],
            "population": [731545, 5024279, 39538223, 20201249],
        }
    )


def test_add_positivity_computes_ratio() -> None:
    df = pd.read_csv(FIXTURE)

    result = add_positivity(df)

    assert "positivity" in result.columns
    assert result["positivity"].between(0, 1).all()
    assert not result["positivity"].isna().all()


def test_add_positivity_is_nan_when_denominator_zero() -> None:
    df = pd.DataFrame({"positive": [10, 5], "totalTestResults": [0, 100]})

    result = add_positivity(df)

    assert pd.isna(result.loc[0, "positivity"])
    assert result.loc[1, "positivity"] == 0.05


def test_add_death_rate_computes_ratio() -> None:
    df = pd.read_csv(FIXTURE)

    result = add_death_rate(df)

    assert "death_rate" in result.columns
    assert result["death_rate"].between(0, 1).all()


def test_add_daily_ma7_groups_by_state() -> None:
    df = pd.read_csv(FIXTURE).sort_values(["state", "date"]).reset_index(drop=True)

    result = add_daily_ma7(df, window=3)

    assert "positiveIncrease_ma3" in result.columns
    # los 2 primeros días de cada estado son NaN con ventana completa de 3
    assert (
        result.groupby("state")["positiveIncrease_ma3"]
        .apply(lambda s: s.iloc[:2].isna().all())
        .all()
    )


def test_add_base_features_adds_three_columns() -> None:
    df = pd.read_csv(FIXTURE)

    result = add_base_features(df)

    assert {"positivity", "death_rate", "positiveIncrease_ma7"}.issubset(result.columns)


def test_merge_population_validates_and_adds_column(tmp_path: Path) -> None:
    df = pd.read_csv(FIXTURE)
    pop_path = tmp_path / "population.csv"
    population_frame().to_csv(pop_path, index=False)

    result = merge_population(df, population_path=pop_path)

    assert "population" in result.columns
    assert len(result) == len(df)
    assert set(result["state"]) == set(df["state"])


def test_merge_population_raises_on_missing_state(tmp_path: Path) -> None:
    df = pd.read_csv(FIXTURE)
    pop = population_frame().drop(index=0)  # falta AK
    pop_path = tmp_path / "population.csv"
    pop.to_csv(pop_path, index=False)

    with pytest.raises(ValueError, match="Faltan estados"):
        merge_population(df, population_path=pop_path)


def test_merge_population_raises_on_row_count_change(tmp_path: Path) -> None:
    df = pd.read_csv(FIXTURE)
    # duplica una fila de población para provocar many_to_one violation
    pop = pd.concat([population_frame(), population_frame().iloc[[0]]], ignore_index=True)
    pop_path = tmp_path / "population.csv"
    pop.to_csv(pop_path, index=False)

    with pytest.raises(ValueError):
        merge_population(df, population_path=pop_path)


def test_add_per_capita_computes_ratios() -> None:
    df = pd.read_csv(FIXTURE)
    df["population"] = 1_000_000

    result = add_per_capita(df)

    assert {"positive_per_100k", "death_per_100k", "tests_per_100k"}.issubset(result.columns)
    assert not result["positive_per_100k"].isna().all()
    assert not (result["positive_per_100k"] == float("inf")).any()


def test_add_per_capita_requires_population() -> None:
    df = pd.read_csv(FIXTURE)

    with pytest.raises(ValueError, match="population"):
        add_per_capita(df)


def test_add_all_features_without_population_keeps_base(tmp_path: Path) -> None:
    df = pd.read_csv(FIXTURE)

    result = add_all_features(df, population_path=tmp_path / "no_existe.csv")

    assert {"positivity", "death_rate", "positiveIncrease_ma7"}.issubset(result.columns)
    assert "population" not in result.columns


def test_add_all_features_with_population_adds_ratios(tmp_path: Path) -> None:
    df = pd.read_csv(FIXTURE)
    pop_path = tmp_path / "population.csv"
    population_frame().to_csv(pop_path, index=False)

    result = add_all_features(df, population_path=pop_path)

    assert "population" in result.columns
    assert "positive_per_100k" in result.columns
