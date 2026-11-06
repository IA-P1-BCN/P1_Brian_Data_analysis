---
description: "Redacta la spec OpenSpec de un issue o change (delegando en spec-writer)"
---

<!-- GENERADO por scripts/sync_agents.py desde .agents/commands/sdd-spec.md. No editar a mano. -->

Redacta la especificación OpenSpec para: **$ARGUMENTS**.

1. Localiza el issue en GitHub (número, título, criterios de aceptación y
   milestone `N1`/`N2`/`N3`) y el change correspondiente en
   `openspec/changes/`.
2. Delega en el subagente `spec-writer` con el contexto del issue y las
   capacidades afectadas.
3. Pídele que escriba:
   - `openspec/changes/<change>/proposal.md`
   - `openspec/changes/<change>/specs/<capacidad>/spec.md`
4. Ejecuta `npm run spec:validate` y corrige los errores de formato.
5. Muéstrame:
   - rutas creadas;
   - resumen de requisitos;
   - lista de `<<PENDIENTE>>`;
   - decisiones que debo tomar antes de aprobar.

No escribas `design.md`, `tasks.md`, código ni notebooks. No marques el
change como aprobado: eso lo hago yo.
