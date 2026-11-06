#!/usr/bin/env python3
"""Genera .opencode/agents y .opencode/commands desde .agents/.

Fuente:
  .agents/agents/<nombre>.md    cuerpo del subagente
  .agents/commands/<nombre>.md  cuerpo del comando
  AGENTS / COMMANDS (abajo)     descripción y permisos

Destino (no editar a mano):
  .opencode/agents/
  .opencode/commands/

Uso:
  python scripts/sync_agents.py           # regenera
  python scripts/sync_agents.py --check   # sale con 1 si algo está desactualizado
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS_SRC = ROOT / ".agents" / "agents"
COMMANDS_SRC = ROOT / ".agents" / "commands"
AGENTS_DST = ROOT / ".opencode" / "agents"
COMMANDS_DST = ROOT / ".opencode" / "commands"

MARCA = "<!-- GENERADO por scripts/sync_agents.py desde {fuente}. No editar a mano. -->"

# --- Subagentes -----------------------------------------------------------------------------
AGENTS: dict[str, dict] = {
    "spec-writer": {
        "description": (
            "Redacta specs OpenSpec (proposal.md y specs/<capacidad>/spec.md) a partir de un issue. "
            "Úsalo para crear o actualizar la especificación de un change. Nunca aprueba ni implementa."
        ),
        "permission": {"edit": "ask", "bash": "deny", "webfetch": "deny"},
    },
    "data-engineer": {
        "description": (
            "Implementa carga, limpieza y features en src/eda/ y sus tests. "
            "Úsalo para tocar load.py, clean.py, features.py o tests/. No escribe notebooks ni informes."
        ),
        "permission": {"edit": "ask", "bash": "ask", "webfetch": "ask"},
    },
    "eda-analyst": {
        "description": (
            "Construye los notebooks 01_profiling.ipynb y 02_eda.ipynb con análisis reproducible. "
            "Úsalo para perfilado, univariado, bivariado, tendencias y conclusiones. "
            "No escribe la lógica de limpieza."
        ),
        "permission": {"edit": "ask", "bash": "ask", "webfetch": "deny"},
    },
    "viz-designer": {
        "description": (
            "Diseña y construye las funciones de visualización y las figuras del EDA. "
            "Úsalo para src/eda/viz.py y reports/figures/. No cambia el análisis."
        ),
        "permission": {"edit": "ask", "bash": "ask", "webfetch": "deny"},
    },
    "report-writer": {
        "description": (
            "Redacta el informe ejecutivo y el README a partir del notebook y las figuras. "
            "Úsalo para reports/informe.md y README.md. No toca código ni datos."
        ),
        "permission": {"edit": "ask", "bash": "deny", "webfetch": "deny"},
    },
    "eda-reviewer": {
        "description": (
            "Revisa (solo lectura) un change o una PR: spec, reproducibilidad, estadística, "
            "visualización e informe. Devuelve veredicto y hallazgos."
        ),
        "permission": {"edit": "deny", "bash": "deny", "webfetch": "deny"},
    },
    "ai-scribe": {
        "description": (
            "Añade entradas a docs/ai-log.md con modelo, prompts, errores y decisiones. "
            "Úsalo al cerrar una tarea hecha con IA."
        ),
        "permission": {"edit": "ask", "bash": "deny", "webfetch": "deny"},
    },
}

# --- Comandos -------------------------------------------------------------------------------
COMMANDS: dict[str, dict] = {
    "sdd-spec": {
        "description": "Redacta la spec OpenSpec de un issue o change (delegando en spec-writer)",
    },
    "sdd-plan": {
        "description": "Escribe el diseño técnico de un change con spec aprobada",
    },
    "sdd-tasks": {
        "description": "Descompone el diseño de un change en tareas atómicas",
    },
    "sdd-build": {
        "description": "Implementa una tarea de un change delegando en el subagente adecuado",
    },
    "sdd-review": {
        "description": "Revisa un change o una PR antes de mergear",
    },
    "bitacora": {
        "description": "Registra en docs/ai-log.md lo hecho con IA (delegando en ai-scribe)",
    },
    "verify": {
        "description": "Verifica el repositorio (ruff, pytest, notebooks, OpenSpec y agentes)",
    },
}


def yaml_quote(texto: str) -> str:
    """Devuelve un escalar YAML entre comillas dobles y escapado."""
    return '"' + texto.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_agent(nombre: str, meta: dict) -> str:
    cuerpo = (AGENTS_SRC / f"{nombre}.md").read_text(encoding="utf-8").strip()
    lineas = [
        "---",
        f"description: {yaml_quote(meta['description'])}",
        "mode: subagent",
        "permission:",
    ]
    for clave, valor in meta["permission"].items():
        lineas.append(f"  {clave}: {valor}")
    lineas.append("---")
    lineas.append("")
    lineas.append(MARCA.format(fuente=f".agents/agents/{nombre}.md"))
    lineas.append("")
    lineas.append(cuerpo)
    lineas.append("")
    return "\n".join(lineas)


def render_command(nombre: str, meta: dict) -> str:
    cuerpo = (COMMANDS_SRC / f"{nombre}.md").read_text(encoding="utf-8").strip()
    # El cuerpo fuente puede traer su propio frontmatter; lo descartamos.
    if cuerpo.startswith("---"):
        partes = cuerpo.split("---", 2)
        if len(partes) == 3:
            cuerpo = partes[2].strip()
    lineas = [
        "---",
        f"description: {yaml_quote(meta['description'])}",
        "---",
        "",
        MARCA.format(fuente=f".agents/commands/{nombre}.md"),
        "",
        cuerpo,
        "",
    ]
    return "\n".join(lineas)


def build_files() -> dict[Path, str]:
    """Devuelve el contenido esperado de cada fichero generado."""
    archivos: dict[Path, str] = {}
    for nombre, meta in AGENTS.items():
        archivos[AGENTS_DST / f"{nombre}.md"] = render_agent(nombre, meta)
    for nombre, meta in COMMANDS.items():
        archivos[COMMANDS_DST / f"{nombre}.md"] = render_command(nombre, meta)
    return archivos


def validate_metadata() -> list[str]:
    """Comprueba que fuentes y metadatos coinciden."""
    errores: list[str] = []
    fuentes_agents = {p.stem for p in AGENTS_SRC.glob("*.md")}
    fuentes_commands = {p.stem for p in COMMANDS_SRC.glob("*.md")}

    for nombre in sorted(fuentes_agents - set(AGENTS)):
        errores.append(f".agents/agents/{nombre}.md no tiene entrada en AGENTS")
    for nombre in sorted(set(AGENTS) - fuentes_agents):
        errores.append(f"AGENTS['{nombre}'] no tiene .agents/agents/{nombre}.md")

    for nombre in sorted(fuentes_commands - set(COMMANDS)):
        errores.append(f".agents/commands/{nombre}.md no tiene entrada en COMMANDS")
    for nombre in sorted(set(COMMANDS) - fuentes_commands):
        errores.append(f"COMMANDS['{nombre}'] no tiene .agents/commands/{nombre}.md")

    return errores


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="no escribe; sale con 1 si hay ficheros desactualizados",
    )
    args = parser.parse_args()

    errores = validate_metadata()
    if errores:
        print("Metadatos incoherentes:", file=sys.stderr)
        for error in errores:
            print(f"  - {error}", file=sys.stderr)
        return 1

    archivos = build_files()

    if args.check:
        desactualizados = [
            ruta
            for ruta, contenido in archivos.items()
            if not ruta.exists() or ruta.read_text(encoding="utf-8") != contenido
        ]
        if desactualizados:
            print("Ficheros generados desactualizados:", file=sys.stderr)
            for ruta in desactualizados:
                print(f"  - {ruta.relative_to(ROOT)}", file=sys.stderr)
            print("Ejecuta: python scripts/sync_agents.py", file=sys.stderr)
            return 1
        print(f"OK: {len(archivos)} ficheros generados al día")
        return 0

    for ruta, contenido in archivos.items():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(contenido, encoding="utf-8")
        print(f"escrito {ruta.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
