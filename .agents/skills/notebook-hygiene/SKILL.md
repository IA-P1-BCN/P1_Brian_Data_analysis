---
name: notebook-hygiene
description: Reglas de calidad para notebooks Jupyter del proyecto (ejecución top-down, imports arriba, Markdown antes de cada análisis, sin outputs versionados, determinismo y figuras guardadas). Úsala al crear, editar o revisar 01_profiling.ipynb y 02_eda.ipynb.
---

# Higiene de notebooks

Un notebook es **un informe ejecutable**, no un cuaderno de borrador.

## Reglas duras

1. **Ejecuta de arriba abajo.** Si una celda necesita que hayas ejecutado
   otra en otro orden, está mal.
2. **Imports arriba.** Todas las importaciones en la primera celda de código.
3. **Sin outputs versionados.** Los notebooks se commitean limpios.
   `nbstripout` o `jupyter nbconvert --ClearOutputPreprocessor.enabled=True`.
4. **Sin estado oculto.** Nada de variables que solo existen porque
   ejecutaste una celda antigua. Si borras una celda, borra sus efectos.
5. **Una idea por celda.** Celda de código + celda Markdown que la explica.
6. **Markdown antes del análisis**, no después. Estructura:
   - **Pregunta**: qué queremos saber.
   - **Método**: qué calculamos y por qué.
   - **Resultado**: qué se ve.
   - **Interpretación**: qué significa y qué no.
7. **Determinismo.** `random_state` fijo, orden de filas explícito y sin
   `head()` como única evidencia.
8. **Figuras guardadas** en `reports/figures/` con nombre descriptivo y
   `dpi=150`. En el notebook se muestran, no se confía en el archivo temporal.
9. **Rutas relativas al proyecto**, nunca `C:\...` ni `/home/...`.
10. **Última celda: conclusiones.** Tres o cuatro bullets con las respuestas
    a las preguntas de negocio.

## Estructura recomendada de `02_eda.ipynb`

```text
1. Título y contexto (Markdown)
2. Preguntas de negocio e hipótesis (Markdown)
3. Configuración e imports (código)
4. Carga de datos limpios (código)
5. Perfil general (shape, tipos, nulos)
6. Pregunta 1 · Univariado + interpretación
7. Pregunta 2 · Bivariado + interpretación
8. Pregunta 3 · Tendencia / segmento + interpretación
9. Features avanzadas (ratios 100k, media móvil, log)
10. Limitaciones (Markdown)
11. Conclusiones y próximos pasos (Markdown)
```

## Antes de cerrar la PR

```bash
jupyter nbconvert --to notebook --execute notebooks/01_profiling.ipynb \
  --output /tmp/01_profiling.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_eda.ipynb \
  --output /tmp/02_eda.ipynb
```

Si falla, la PR no está lista.

## Olores típicos

| Olor | Arreglo |
|---|---|
| `df = df.dropna()` y luego usas el `df` viejo | Reasigna o usa otro nombre |
| Celda que hace `plt.show()` sin título ni ejes | Añade título, ejes y unidades |
| `print(df)` para “ver” | Usa `display(df.head())` o una tabla Markdown |
| Lógica de limpieza en el notebook | Muévela a `src/eda/clean.py` |
| Número escrito a mano en el Markdown | Cálculo en celda + referencia |
| Output enorme | Filtra, agrega o muestra solo lo relevante |
| Celda comentada “por si acaso” | Bórrala; git ya guarda la historia |
