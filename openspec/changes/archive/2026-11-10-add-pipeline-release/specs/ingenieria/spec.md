# Spec Delta

## Purpose

Garantizar que el análisis se puede reproducir de principio a fin con un
comando, que los cambios no rompen la limpieza ni las features, y que la
entrega queda versionada y verificada.

## ADDED Requirements

### Requirement: Tests de limpieza y features

El repositorio SHALL incluir tests de `clean.py` y `features.py` que cubran
fechas, duplicados, nulos, negativos, ratios y merge de población.

#### Scenario: Test de limpieza

- **WHEN** se ejecuta `pytest tests/test_clean.py`
- **THEN** todos los tests pasan y cubren al menos los caminos de error
  documentados

#### Scenario: Test de features

- **WHEN** se ejecuta `pytest tests/test_features.py`
- **THEN** se verifica que los ratios no son `inf` y que el merge no pierde
  estados

### Requirement: Pipeline reproducible

`scripts/run_pipeline.py` SHALL ejecutar carga, limpieza y features y SHALL
escribir `data/processed/covid_clean.csv` sin pasos manuales.

#### Scenario: Ejecución completa

- **WHEN** se ejecuta `python scripts/run_pipeline.py`
- **THEN** el CSV procesado se regenera y el comando termina con código 0

#### Scenario: Datos ausentes

- **WHEN** no hay CSV en `data/raw/` y no hay red
- **THEN** el pipeline falla con un mensaje accionable y no deja un CSV a
  medias

### Requirement: CI completa

La CI SHALL ejecutar `ruff`, `pytest`, `openspec validate --all`, la
comprobación de agentes y la ejecución de los notebooks en las PRs que
toquen `notebooks/` o `src/`.

#### Scenario: PR con notebook roto

- **WHEN** una PR modifica un notebook y no ejecuta de arriba abajo
- **THEN** el job de notebooks falla y la PR queda bloqueada

#### Scenario: PR solo de documentación

- **WHEN** una PR solo cambia `docs/` o `README.md`
- **THEN** los jobs de tests y notebooks se omiten o pasan sin ejecutar
  análisis pesado

### Requirement: Release versionado

El proyecto SHALL publicar un tag `v1.0.0` con el informe, el README y el
notebook ejecutado.

#### Scenario: Release

- **WHEN** se crea el tag `v1.0.0`
- **THEN** la release en GitHub incluye el resumen del informe y el enlace
  al notebook
