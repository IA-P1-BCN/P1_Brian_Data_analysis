"""Smoke tests de la infraestructura del proyecto."""

from pathlib import Path

from src.eda import __version__


def test_package_imports() -> None:
    assert __version__ == "0.1.0"


def test_repository_layout() -> None:
    root = Path(__file__).resolve().parents[1]
    for carpeta in ("data", "notebooks", "reports", "src", "tests", "openspec"):
        assert (root / carpeta).is_dir(), f"falta {carpeta}/"


def test_agents_infrastructure() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / "AGENTS.md").is_file()
    assert (root / ".agents" / "agents").is_dir()
    assert (root / ".agents" / "skills").is_dir()
    assert (root / ".opencode" / "agents").is_dir()
