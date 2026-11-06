---
name: sdd-workflow
description: Ciclo Spec-Driven Development con OpenSpec del proyecto EDA (proposal → spec → design → tasks → build → review → archive). Úsala al crear o editar cualquier archivo de openspec/, al pasar un change de estado o cuando alguien pida "la spec", "el plan" o "las tareas" de un issue.
---

# Spec-Driven Development con OpenSpec

## Dónde está todo

- Reglas del proyecto: `AGENTS.md` (manda sobre todo lo demás).
- Contexto y reglas de redacción: `openspec/config.yaml`.
- Specs vigentes: `openspec/specs/<capacidad>/spec.md`.
- Propuestas en curso: `openspec/changes/<change>/`.
- Plantilla de cambio: `python scripts/new_change.py <slug> --capability <cap>`.
- Issues y niveles: GitHub Project + milestones `N1`, `N2`, `N3`.

## Estructura de un change

```text
openspec/changes/<change>/
├── proposal.md              por qué y qué cambia
├── design.md                cómo se implementa
├── tasks.md                 tareas atómicas con su issue
└── specs/<capacidad>/spec.md requisitos y escenarios
```

## Estados

| Estado | Quién lo pone | Qué permite |
|---|---|---|
| `Borrador` | `spec-writer` o persona | Discutir y corregir |
| `Aprobada` | **Solo una persona** | Escribir `design.md` y `tasks.md` |
| `En construcción` | Quien implementa | Tocar código y notebooks |
| `En revisión` | Quien abre la PR | Revisión y CI |
| `Archivada` | Persona, tras cerrar issues | Mover la spec a `openspec/specs/` |

## Gates (no te los saltes)

| Para escribir… | Requisito |
|---|---|
| `proposal.md` | Existe el issue en el Project |
| `specs/<cap>/spec.md` | El issue tiene criterios de aceptación |
| `design.md` | `proposal.md` revisado por una persona |
| `tasks.md` | `design.md` existe |
| Código o notebook | `tasks.md` existe y la tarea está asignada |
| PR | `/sdd-review` pasado y `/verify` verde |
| `openspec archive` | Todos los issues del change cerrados |

## Cómo redactar una spec

Cada requisito usa **SHALL** o **MUST** y al menos un escenario **WHEN/THEN**:

```markdown
## ADDED Requirements

### Requirement: Fechas normalizadas
`load.py` SHALL convertir la columna `date` de entero `YYYYMMDD` a
`datetime64[ns]` sin pérdida de días.

#### Scenario: Fecha válida
- **WHEN** `date` vale `20200501`
- **THEN** la columna resultante es `2020-05-01 00:00:00`

#### Scenario: Fecha inválida
- **WHEN** `date` no tiene 8 dígitos o no existe en el calendario
- **THEN** la fila se marca como inválida y se informa del recuento
```

Reglas:

- Un requisito = una capacidad observable.
- Incluye el camino feliz, los errores y los límites.
- No mezcles requisitos con decisiones de implementación; eso va en `design.md`.
- Si falta un dato, escribe `<<PENDIENTE>>`; no lo inventes.

## Cómo redactar `tasks.md`

- Una tarea = un issue = una PR.
- Referencia el issue: `- [ ] N1-04 Implementar clean.py (#12)`.
- Incluye validación en cada bloque: `ruff`, `pytest`, notebook.
- No pongas tareas de varios niveles en el mismo bloque.

## Cómo archivar

```bash
npm run spec:validate
npx openspec archive <change>
```

Al archivar, la spec del change pasa a `openspec/specs/<capacidad>/` y el
change queda como histórico. **Solo una persona archiva.**

## Errores típicos

- Escribir `design.md` sin que la persona haya aprobado el `proposal.md`.
- Duplicar la misma regla en `openspec/specs/` y en el change.
- Crear un change por issue en vez de por épica.
- Archivar con issues abiertos.
- Cambiar el alcance sin actualizar la spec.
