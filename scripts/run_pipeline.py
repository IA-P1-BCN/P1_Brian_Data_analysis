#!/usr/bin/env python3
"""Pipeline reproducible: carga, limpia y guarda el dataset procesado.

Uso:
    python scripts/run_pipeline.py
    python scripts/run_pipeline.py --force   # fuerza la descarga
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.eda.clean import build_clean_dataset  # noqa: E402
from src.eda.load import download_covid_data  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="fuerza la descarga del CSV crudo")
    parser.add_argument("--csv", type=Path, default=None, help="ruta al CSV crudo (opcional)")
    args = parser.parse_args()

    if args.force:
        try:
            download_covid_data()
        except Exception as exc:  # noqa: BLE001 - punto de entrada del CLI
            logger.error("No se pudo descargar el dataset: %s", exc)
            return 1

    try:
        clean, audit = build_clean_dataset(csv_path=args.csv, validate=True)
    except Exception as exc:  # noqa: BLE001 - punto de entrada del CLI
        logger.error("El pipeline falló: %s", exc)
        return 1

    logger.info("Pipeline completado: %s", audit)
    logger.info("Filas procesadas: %d", len(clean))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
