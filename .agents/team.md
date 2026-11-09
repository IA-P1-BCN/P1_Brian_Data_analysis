# Equipo y reparto

## Persona

| Persona | GitHub | Rol |
|---|---|---|
| Brian Hañari | `@BrianStiv` | Dueño, desarrollador y revisor |

Proyecto individual. La persona aprueba las specs, revisa las PRs y decide
los recortes de alcance.

## Agentes

| Agente | Rol | Puede escribir |
|---|---|---|
| `spec-writer` | Especificar | `openspec/changes/**` |
| `data-engineer` | Implementar datos | `src/eda/**`, `tests/**` |
| `notebook-builder` | Narrar | `notebooks/**` |
| `eda-reviewer` | Revisar | nada (solo lectura) |
| `test-designer` | Probar | `tests/**` |
| `ai-scribe` | Trazar | `docs/ai-log.md` |

## Reparto por nivel

| Nivel | Foco | Criterio de cierre |
|---|---|---|
| N1 · Esencial | Cargar, perfilar, limpiar, describir | Notebook top-down con 3 univariados y 3 bivariados |
| N2 · Medio | Justificar, agregar, correlacionar, testear | Informe v1 y tests verdes |
| N3 · Avanzado | Normalizar, integrar, segmentar, automatizar | Ratios 100k, merge, plotly y pipeline |

## Regla de revisión

La persona revisa **todo** lo que produce un agente antes de mergear. Ningún
agente aprueba su propio trabajo ni archiva un change.
