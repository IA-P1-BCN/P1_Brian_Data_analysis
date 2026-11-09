# ADR-0001 · Infraestructura de IA para el EDA

- **Estado:** Aceptada
- **Fecha:** 2026-11-06
- **Contexto:** mini datathon de 6 días, una persona, nivel objetivo Avanzado.

## Decisión

Usar **OpenSpec CLI** como motor de especificaciones y una **capa de agentes
tipo n8n** encima:

- `openspec/` contiene `config.yaml`, `specs/` (vigentes) y `changes/`
  (propuestas por épica).
- `.agents/` es la fuente de subagentes, comandos, skills, ADRs y plantillas.
- `.opencode/` contiene la configuración de OpenCode y los ficheros generados
  desde `.agents/` por `scripts/sync_agents.py`.
- Las skills viven en `.agents/skills/` y las descubre OpenCode directamente.

## Por qué

1. **OpenSpec** da un ciclo verificable (`validate`, `archive`) y specs con
   requisitos y escenarios. Es evidencia objetiva de trabajo spec-driven.
2. **La capa de agentes** separa responsabilidades: especificar, implementar,
   narrar, revisar y trazar. Evita que un solo agente lo haga todo y se
   autoapruebe.
3. **Una sola fuente** (`.agents/`) evita duplicar prompts entre herramientas.
4. **Skills globales** (`pandas-pro`, `statistical-analysis`,
   `data-visualization`, …) cubren la parte técnica; las skills propias solo
   aportan el contexto del proyecto.

## Alternativas descartadas

| Alternativa | Por qué no |
|---|---|
| Solo SDD propio tipo n8n | No tiene `validate`/`archive` ni specs vigentes separadas de las propuestas. |
| Solo OpenSpec, sin agentes | Pierdes la separación de roles y la trazabilidad de la IA. |
| Un change por issue (26) | Demasiada ceremonia para 6 días; se solapan y duplican specs. |
| Un change por nivel (3) | Mezcla capacidades distintas y archiva demasiado de golpe. |

## Consecuencias

- Hay una dependencia de Node (`@fission-ai/openspec`) solo para specs; las
  dependencias Python siguen en `requirements.txt`.
- Los ficheros de `.opencode/agents/` y `.opencode/commands/` son generados:
  no se editan a mano.
- La CI comprueba `sync_agents.py --check` y `openspec validate`.
- Cuando un change se archiva, su spec pasa a `openspec/specs/<capacidad>/`.
