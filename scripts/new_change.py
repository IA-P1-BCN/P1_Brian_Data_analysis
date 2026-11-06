#!/usr/bin/env python3
"""Crea un change OpenSpec con la estructura y las plantillas oficiales.

Uso:
  python scripts/new_change.py add-limpieza-calidad --capability calidad-datos
  python scripts/new_change.py add-mi-change --capability analisis --title "Mi cambio"

El formato sigue las plantillas del esquema `spec-driven` de OpenSpec 1.14.
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHANGES = ROOT / "openspec" / "changes"

PROPOSAL = """# Proposal

## Why

<<PENDIENTE: issue y problema que resuelve>>

## What Changes

- <<PENDIENTE: comportamiento nuevo 1>>
- <<PENDIENTE: comportamiento nuevo 2>>

## Capabilities

### New Capabilities

- `{capability}`: <<PENDIENTE: una línea>>

### Modified Capabilities

Ninguna.

## Impact

<<PENDIENTE: código, datos, notebooks, tests y documentación afectados>>
"""

SPEC = """# Spec Delta

## Purpose

<<PENDIENTE: qué cubre esta capacidad, en una o dos frases (50+ caracteres)>>

## ADDED Requirements

### Requirement: <<PENDIENTE: nombre del requisito>>

<<PENDIENTE: qué debe hacer el sistema, con SHALL o MUST>>

#### Scenario: <<PENDIENTE: caso>>

- **WHEN** <<PENDIENTE: condición>>
- **THEN** <<PENDIENTE: resultado observable>>
"""

DESIGN = """# Design

## Context

<<PENDIENTE: estado actual y restricciones>>

## Goals / Non-Goals

**Goals:**
- <<PENDIENTE>>

**Non-Goals:**
- <<PENDIENTE>>

## Decisions

### Decisión 1 · <<PENDIENTE: título>>

- **Qué:** <<PENDIENTE>>
- **Por qué:** <<PENDIENTE>>
- **Alternativas:** <<PENDIENTE>>
- **Consecuencias:** <<PENDIENTE>>

## Risks / Trade-offs

- <<PENDIENTE>>
"""

TASKS = """# Tasks

## 1. Especificación

- [ ] 1.1 Revisar `proposal.md` y `specs/{capability}/spec.md`
- [ ] 1.2 Aprobar el change (persona)

## 2. Implementación

- [ ] 2.1 `N?-??` <<PENDIENTE: tarea con su issue>>
  - Criterio: <<PENDIENTE>>
  - Validación: `ruff check .` y `pytest -q`

## 3. Cierre

- [ ] 3.1 Ejecutar `/sdd-review`
- [ ] 3.2 Ejecutar `/verify`
- [ ] 3.3 Registrar en `docs/ai-log.md`
- [ ] 3.4 `openspec archive {slug}`
"""


def slugify(texto: str) -> str:
    texto = texto.strip().lower()
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    return texto.strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="nombre del change, p. ej. add-limpieza-calidad")
    parser.add_argument("--capability", required=True, help="capacidad, p. ej. calidad-datos")
    parser.add_argument("--title", default="", help="título legible (opcional)")
    args = parser.parse_args()

    slug = slugify(args.slug)
    capability = slugify(args.capability)
    destino = CHANGES / slug

    if destino.exists():
        print(f"Error: ya existe {destino.relative_to(ROOT)}")
        return 1

    (destino / "specs" / capability).mkdir(parents=True)
    (destino / "proposal.md").write_text(PROPOSAL.format(capability=capability), encoding="utf-8")
    (destino / "specs" / capability / "spec.md").write_text(SPEC, encoding="utf-8")
    (destino / "design.md").write_text(DESIGN, encoding="utf-8")
    (destino / "tasks.md").write_text(
        TASKS.format(slug=slug, capability=capability), encoding="utf-8"
    )
    (destino / ".openspec.yaml").write_text(
        f"schema: spec-driven\ncreated: {date.today().isoformat()}\n",
        encoding="utf-8",
    )
    titulo = args.title or slug
    (destino / "README.md").write_text(
        f"# {titulo}\n\nChange OpenSpec `{slug}` (capacidad `{capability}`).\n",
        encoding="utf-8",
    )

    print(f"Creado openspec/changes/{slug}/")
    print(f"  capability: {capability}")
    print("Siguiente paso: completar proposal.md y specs/<capacidad>/spec.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
