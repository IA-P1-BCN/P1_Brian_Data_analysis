# Design

## Context

El notebook `02_eda.ipynb` ya contiene los análisis y las figuras. El
informe debe destilarlos, no repetirlos. La audiencia es un CEO que quiere
tres mensajes claros y una recomendación, no un tutorial de pandas.

## Goals / Non-Goals

**Goals:**
- Un informe de 1–2 páginas con 3–5 hallazgos.
- Cifras trazables al notebook.
- README que permita reproducir el proyecto.
- Un gráfico Plotly interactivo.

**Non-Goals:**
- Artículo académico.
- Anexo con todos los gráficos.
- Dashboard Streamlit (nivel Experto).

## Decisions

### Decisión 1 · Un hallazgo, una cifra, una figura

- **Qué:** cada hallazgo tiene evidencia visual y numérica.
- **Por qué:** el CEO recuerda imágenes y cifras, no metodología.
- **Alternativas:** narrar todo el proceso.
- **Consecuencias:** el detalle técnico se queda en el notebook.

### Decisión 2 · Informe en Markdown, no PDF

- **Qué:** `reports/informe.md`.
- **Por qué:** se versiona, se revisa en la PR y se convierte a PDF si hace
  falta.
- **Alternativas:** Word o PDF binario (no se revisa bien en git).
- **Consecuencias:** el formato final se genera al entregar.

### Decisión 3 · Plotly solo para una pregunta

- **Qué:** un gráfico interactivo, no todos.
- **Por qué:** el resto se lee mejor en estático y el notebook no se llena
  de HTML.
- **Alternativas:** convertir todos los gráficos a Plotly.
- **Consecuencias:** se elige la pregunta donde el filtro por estado aporta.

### Decisión 4 · README como puerta de entrada

- **Qué:** origen, instalación, ejecución, estructura y resultados.
- **Por qué:** el evaluador empieza por el README.
- **Alternativas:** remitir al notebook.
- **Consecuencias:** hay que mantenerlo actualizado al cambiar el entorno.

## Risks / Trade-offs

- El informe puede quedarse largo; se recorta a 2 páginas.
- Las cifras pueden quedar obsoletas si cambia el dataset; se congelan con
  la fecha de descarga.
- Plotly añade peso al notebook; se usa solo una vez.
- El README puede duplicar el informe; se separan audiencias.
