# Design

## Context

La lógica ya vive en `src/eda/`, pero no hay tests ni un punto de entrada
único. La CI actual valida specs y agentes, pero no ejecuta el análisis. La
entrega final necesita un tag y una release.

## Goals / Non-Goals

**Goals:**
- Tests rápidos y sin red.
- Un comando de pipeline de raw a processed.
- CI que detecte notebooks rotos.
- Release `v1.0.0` reproducible.

**Non-Goals:**
- Despliegue en producción.
- Dashboard Streamlit.
- Orquestación con Airflow o similar.

## Decisions

### Decisión 1 · Pipeline como script, no como notebook

- **Qué:** `scripts/run_pipeline.py` llama a `src/eda/`.
- **Por qué:** se puede ejecutar en CI y en local sin Jupyter.
- **Alternativas:** ejecutar el notebook de limpieza (lento y frágil).
- **Consecuencias:** el notebook solo narra; el pipeline es la verdad.

### Decisión 2 · Tests con fixtures pequeños

- **Qué:** CSV de 10–20 filas en `tests/fixtures/`.
- **Por qué:** rápidos, deterministas y sin red.
- **Alternativas:** usar el CSV completo (lento y dependiente del entorno).
- **Consecuencias:** hay que mantener los fixtures.

### Decisión 3 · Notebooks en CI solo cuando toca

- **Qué:** job condicional a cambios en `notebooks/` o `src/`.
- **Por qué:** ejecutar notebooks en cada PR es lento.
- **Alternativas:** ejecutar siempre (5–10 min por PR).
- **Consecuencias:** una PR de docs no bloquea por un notebook.

### Decisión 4 · Release desde `main`

- **Qué:** tag `v1.0.0` sobre el merge de `develop` en `main`.
- **Por qué:** `main` es la entrega.
- **Alternativas:** tag sobre `develop` (no es lo entregado).
- **Consecuencias:** hay que cerrar el PR de `develop` antes.

## Risks / Trade-offs

- El pipeline puede tardar si descarga el CSV; la caché lo mitiga.
- Los tests con fixtures pueden no cubrir rarezas del dataset real; se
  complementan con la auditoría del notebook.
- La CI condicional puede dejar pasar un notebook roto si no se toca; el
  `/verify` local lo cubre.
- El tag es inmutable; si hay un fallo después, se saca `v1.0.1`.
