# Proposal

## Why

El proyecto arranca sin estructura, sin entorno reproducible y sin una capa de
trabajo con IA. Sin esto, cada análisis dependería de la máquina de quien lo
ejecuta y las specs no tendrían un ciclo verificable. Es el primer issue de
N1 y bloquea a todos los demás.

## What Changes

- Crear la estructura de carpetas (`data/`, `notebooks/`, `src/eda/`, `tests/`,
  `reports/`).
- Fijar las dependencias Python en `requirements.txt` y la configuración de
  `ruff`/`pytest` en `pyproject.toml`.
- Añadir la capa de agentes: `AGENTS.md`, `.agents/`, `.opencode/` y las
  skills del proyecto.
- Instalar OpenSpec como herramienta de specs (`package.json`) y crear
  `openspec/config.yaml`.
- Añadir la CI base: `ruff`, `pytest`, `openspec validate` y comprobación de
  que los agentes generados están al día.

## Capabilities

### New Capabilities

- `entorno`: entorno reproducible, estructura del repositorio y puertas de
  calidad automáticas.

### Modified Capabilities

Ninguna.

## Impact

- Raíz del repositorio, `.gitignore`, `README.md`.
- `pyproject.toml`, `requirements.txt`, `package.json`.
- `.github/workflows/ci.yml`.
- `AGENTS.md`, `.agents/`, `.opencode/`, `scripts/`.
