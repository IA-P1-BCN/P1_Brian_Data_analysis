# ingesta Specification

## Purpose
Cargar el dataset del COVID Tracking Project de forma reproducible, con
caché local, validación de esquema y un diccionario que permita interpretar
cada columna sin ambigüedad.

## Requirements

### Requirement: Descarga con caché

`load.py` SHALL descargar el dataset solo si no existe en `data/raw/` y
SHALL reutilizar la copia local en ejecuciones posteriores.

#### Scenario: Primera ejecución

- **WHEN** `data/raw/` no contiene el CSV
- **THEN** `load_covid_data()` lo descarga, lo guarda y devuelve un
  `DataFrame` con los datos

#### Scenario: Ejecución posterior

- **WHEN** el CSV ya existe en `data/raw/`
- **THEN** `load_covid_data()` lo lee del disco y no hace ninguna petición
  de red

#### Scenario: Fallo de red sin caché

- **WHEN** no hay CSV local y la descarga falla
- **THEN** se lanza una excepción con la URL y la causa, sin crear un
  fichero vacío

### Requirement: Validación de esquema

`load.py` SHALL validar que el dataset tiene al menos 1000 filas, al menos
8 columnas y las columnas clave `date`, `state`, `positive`, `death` y
`totalTestResults`.

#### Scenario: Dataset válido

- **WHEN** el CSV tiene 1000 o más filas y las columnas clave
- **THEN** la carga termina y devuelve el `DataFrame`

#### Scenario: Dataset incompleto

- **WHEN** falta una columna clave o hay menos de 1000 filas
- **THEN** se lanza un `ValueError` con el detalle de lo que falta

### Requirement: Datos crudos inmutables

La carga SHALL ser de solo lectura sobre `data/raw/` y SHALL no modificar el
fichero descargado.

#### Scenario: Reejecución

- **WHEN** se llama dos veces a `load_covid_data()`
- **THEN** el hash del CSV en `data/raw/` no cambia

### Requirement: Diccionario de datos

El repositorio SHALL documentar en `docs/data_dictionary.md` el significado,
tipo y unidad de cada columna usada en el análisis.

#### Scenario: Columna documentada

- **WHEN** un notebook usa `hospitalizedCurrently`
- **THEN** el diccionario explica qué mide, su unidad y sus limitaciones
