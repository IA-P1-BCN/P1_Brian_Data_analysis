#!/usr/bin/env python3
"""Comprueba la coherencia de la infraestructura de IA del proyecto.

Verifica:
  - que .agents/agents y .agents/commands coinciden con los metadatos;
  - que los ficheros generados en .opencode/ están al día;
  - que cada skill tiene frontmatter con name y description;
  - que existen AGENTS.md, openspec/config.yaml y docs/ai-log.md.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from sync_agents import (  # noqa: E402
    AGENTS,
    COMMANDS,
    build_files,
    validate_metadata,
)

SKILLS = ROOT / ".agents" / "skills"
REQUIRED = [
    ROOT / "AGENTS.md",
    ROOT / "openspec" / "config.yaml",
    ROOT / "docs" / "ai-log.md",
    ROOT / ".opencode" / "opencode.jsonc",
]


def check_required() -> list[str]:
    return [
        f"falta {ruta.relative_to(ROOT)}"
        for ruta in REQUIRED
        if not ruta.exists()
    ]


def check_skills() -> list[str]:
    errores: list[str] = []
    if not SKILLS.exists():
        return [".agents/skills/ no existe"]

    for carpeta in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        ruta = carpeta / "SKILL.md"
        if not ruta.exists():
            errores.append(f"{carpeta.name}: falta SKILL.md")
            continue

        texto = ruta.read_text(encoding="utf-8")
        if not texto.startswith("---"):
            errores.append(f"{carpeta.name}: falta frontmatter")
            continue

        partes = texto.split("---", 2)
        if len(partes) < 3:
            errores.append(f"{carpeta.name}: frontmatter mal cerrado")
            continue

        frontmatter = partes[1]
        for clave in ("name", "description"):
            if not re.search(rf"^{clave}:", frontmatter, re.MULTILINE):
                errores.append(f"{carpeta.name}: falta '{clave}' en frontmatter")

        match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
        if match:
            nombre = match.group(1).strip().strip("\"'")
            if nombre != carpeta.name:
                errores.append(
                    f"{carpeta.name}: name='{nombre}' no coincide con la carpeta"
                )

    return errores


def check_generated() -> list[str]:
    errores: list[str] = []
    for ruta, contenido in build_files().items():
        if not ruta.exists():
            errores.append(f"falta {ruta.relative_to(ROOT)} (ejecuta sync_agents.py)")
        elif ruta.read_text(encoding="utf-8") != contenido:
            errores.append(f"desactualizado {ruta.relative_to(ROOT)}")
    return errores


def main() -> int:
    errores: list[str] = []
    errores += check_required()
    errores += check_skills()
    errores += validate_metadata()
    errores += check_generated()

    if errores:
        print("Infraestructura de IA con problemas:", file=sys.stderr)
        for error in errores:
            print(f"  - {error}", file=sys.stderr)
        return 1

    total_skills = sum(1 for p in SKILLS.iterdir() if p.is_dir())
    print("OK: infraestructura de IA coherente")
    print(f"  subagentes: {len(AGENTS)}")
    print(f"  comandos:   {len(COMMANDS)}")
    print(f"  skills:     {total_skills}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
