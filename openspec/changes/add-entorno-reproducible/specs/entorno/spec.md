# Spec Delta

## Purpose

Garantizar que cualquier persona (o agente) pueda clonar el repositorio,
instalar las dependencias y ejecutar el análisis y las comprobaciones de
calidad de la misma forma, sin depender de su máquina.

## ADDED Requirements

### Requirement: Entorno Python reproducible

El repositorio SHALL declarar todas las dependencias Python en
`requirements.txt` con versiones compatibles y SHALL documentar la creación
del entorno virtual en el README.

#### Scenario: Instalación desde cero

- **WHEN** una persona clona el repositorio y ejecuta
  `python -m venv .venv && pip install -r requirements.txt`
- **THEN** puede importar `pandas`, `numpy`, `matplotlib`, `seaborn`,
  `plotly`, `pytest` y `ruff` sin instalar nada más

#### Scenario: Dependencia ausente

- **WHEN** un notebook importa un paquete que no está en `requirements.txt`
- **THEN** la CI falla y la PR no se puede mergear

### Requirement: Estructura del repositorio

El repositorio SHALL separar datos crudos, datos procesados, lógica
reutilizable, notebooks, figuras, tests y documentación en carpetas
explícitas.

#### Scenario: Separación de responsabilidades

- **WHEN** se añade una función de limpieza
- **THEN** vive en `src/eda/` y no en una celda del notebook

#### Scenario: Datos crudos protegidos

- **WHEN** se ejecuta el pipeline
- **THEN** `data/raw/` no se modifica y los CSV crudos no se versionan

### Requirement: Puertas de calidad automáticas

La CI SHALL ejecutar `ruff check`, `pytest`, `openspec validate --all` y la
comprobación de que `.opencode/agents` y `.opencode/commands` están
generados desde `.agents/`.

#### Scenario: PR con estilo incorrecto

- **WHEN** una PR introduce un error de `ruff`
- **THEN** el job de lint falla y la PR queda bloqueada

#### Scenario: Agentes desactualizados

- **WHEN** se edita `.agents/agents/spec-writer.md` y no se ejecuta
  `python scripts/sync_agents.py`
- **THEN** el job de infraestructura falla con la lista de ficheros
  desactualizados

### Requirement: Capa de agentes versionada

El repositorio SHALL incluir `AGENTS.md`, los subagentes, los comandos y las
skills del proyecto, con una única fuente editable en `.agents/`.

#### Scenario: Regeneración de agentes

- **WHEN** se ejecuta `python scripts/sync_agents.py`
- **THEN** `.opencode/agents/` y `.opencode/commands/` se regeneran y
  `python scripts/validate_agent_infra.py` termina con código 0
