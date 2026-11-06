# .agents/ · Capa de trabajo con agentes

Fuente única de lo que es común a todas las herramientas de IA del proyecto.
OpenCode lee las copias generadas en `.opencode/` y las skills de
`.agents/skills/`.

## Qué hay y quién lo lee

| Pieza | Fuente (editar aquí) | OpenCode lee |
|---|---|---|
| Reglas del proyecto | `AGENTS.md` | `AGENTS.md` |
| Subagentes | `.agents/agents/<nombre>.md` + metadatos en `scripts/sync_agents.py` | `.opencode/agents/` (generado) |
| Comandos | `.agents/commands/<nombre>.md` + metadatos en `scripts/sync_agents.py` | `.opencode/commands/` (generado) |
| Skills | `.agents/skills/<nombre>/SKILL.md` | `.agents/skills/` (descubiertas) |
| Permisos | — | `.opencode/opencode.jsonc` |
| Equipo y reparto | `.agents/team.md` | bajo demanda |
| Decisiones de arquitectura | `.agents/decisions/` | bajo demanda |
| Plantilla de la bitácora | `.agents/templates/ai-log-entry.md` | bajo demanda |

## Regla de oro

> Se edita la **fuente**, nunca lo generado.

Los ficheros de `.opencode/agents/` y `.opencode/commands/` llevan una marca
`GENERADO` en la cabecera. Si los editas a mano, el siguiente
`python scripts/sync_agents.py` los sobrescribe.

## Cómo regenerar

```bash
python scripts/sync_agents.py           # regenera .opencode/agents y .opencode/commands
python scripts/sync_agents.py --check   # falla si hay diferencias (lo usa la CI)
python scripts/validate_agent_infra.py  # comprueba coherencia de toda la capa
```

## Añadir un subagente

1. Crea `.agents/agents/<nombre>.md` con el cuerpo del prompt.
2. Añade su entrada en el diccionario `AGENTS` de `scripts/sync_agents.py`
   (descripción y permisos).
3. Ejecuta `python scripts/sync_agents.py`.
4. Añade el subagente a la tabla de `AGENTS.md` si es relevante.

## Añadir un comando

1. Crea `.agents/commands/<nombre>.md` con el cuerpo del comando.
2. Añade su entrada en `COMMANDS` de `scripts/sync_agents.py`.
3. Ejecuta `python scripts/sync_agents.py`.

## Añadir una skill

1. Crea `.agents/skills/<nombre>/SKILL.md` con frontmatter `name` y
   `description`. La descripción es lo que usa el agente para decidir cuándo
   cargarla: sé concreto.
2. Añade referencias o scripts en la misma carpeta si hacen falta.
3. No hace falta regenerar nada: OpenCode descubre `.agents/skills/`.

## Skills externas

Las skills globales instaladas (`pandas-pro`, `statistical-analysis`, …)
viven también en `.agents/skills/` y se registran en `skills-lock.json` con su
origen y hash. No se editan a mano: si se actualizan, se hace desde el
instalador de skills.

Las skills propias del proyecto (`sdd-workflow`, `dominio-covid`,
`eda-convenciones`, `revision-eda`, `trazabilidad-ia`) sí se editan aquí.
