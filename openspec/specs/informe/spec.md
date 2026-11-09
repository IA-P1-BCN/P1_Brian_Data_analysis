# informe Specification

## Purpose
Comunicar los hallazgos del EDA a una audiencia no técnica con evidencia
trazable, y dejar el repositorio documentado para que cualquiera pueda
reproducir el análisis.

## Requirements

### Requirement: Informe ejecutivo

`reports/informe.md` SHALL tener entre 1 y 2 páginas y SHALL estar escrito
en español para una audiencia no técnica.

#### Scenario: Lectura ejecutiva

- **WHEN** un directivo lee solo el resumen ejecutivo
- **THEN** entiende los 3 hallazgos principales, su magnitud y la
  recomendación

#### Scenario: Extensión

- **WHEN** se cuenta el contenido del informe
- **THEN** no supera las 2 páginas equivalentes

### Requirement: Cifras trazables

Cada cifra del informe SHALL proceder de una celda del notebook o de una
figura de `reports/figures/`.

#### Scenario: Cifra sin evidencia

- **WHEN** una cifra no se puede localizar en el notebook
- **THEN** se elimina del informe o se marca `<<PENDIENTE>>`

### Requirement: Limitaciones

El informe SHALL incluir una sección de limitaciones que explique el
subregistro, los cambios de reporting, el efecto fin de semana y la
comparabilidad entre estados.

#### Scenario: Afirmación con límite

- **WHEN** se presenta una comparación entre estados
- **THEN** se indica si está normalizada por población y qué no se puede
  concluir

### Requirement: README reproducible

`README.md` SHALL documentar el origen de los datos, la instalación, la
ejecución y la estructura del repositorio.

#### Scenario: Persona nueva

- **WHEN** alguien clona el repositorio y sigue el README
- **THEN** puede instalar dependencias y ejecutar el notebook principal

### Requirement: Gráfico interactivo

El proyecto SHALL incluir al menos un gráfico interactivo con Plotly que
responda a una pregunta de negocio.

#### Scenario: Interacción

- **WHEN** se abre el gráfico en el notebook
- **THEN** se puede hacer zoom, consultar valores y filtrar por estado o
  periodo
