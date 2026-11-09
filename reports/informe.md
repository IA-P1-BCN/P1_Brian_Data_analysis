# El COVID en EE. UU. (2020–2021): unos pocos estados concentran la mayor parte de los casos y las muertes

## Resumen ejecutivo

- **28,8 millones de casos y 515 mil muertes** se registraron en EE. UU. entre
  el 13 de enero de 2020 y el 7 de marzo de 2021.
- **Los 5 estados con más casos (California, Texas, Florida, Nueva York e
  Illinois) concentran el 38 % de los casos y el 38 % de las muertes**, aunque
  representan menos del 40 % de la población.
- **A más tests, más positivos detectados** (correlación 0,91), pero esto no
  significa más contagio: los estados grandes testean y reportan más.
- **La hipótesis de que mayor positividad implica mayor mortalidad no se
  sostiene**: la correlación entre positividad y tasa de mortalidad es
  prácticamente nula (-0,05).
- **El reporting cae en fin de semana**, sobre todo los domingos y lunes, lo
  que distorsiona la lectura diaria; la media móvil de 7 días es la forma
  correcta de seguir la tendencia.

## Contexto y datos

El análisis se basa en el **COVID Tracking Project** (Estados Unidos), serie
diaria por estado, con 20 780 registros y 56 columnas, del 13 de enero de 2020
al 7 de marzo de 2021. Es la última foto publicada por el proyecto, que cerró
en marzo de 2021: describe ese periodo, no la situación actual.

La fuente tiene limitaciones conocidas: son casos **reportados**, no reales; el
subregistro varía por estado; la definición de `totalTestResults` cambió a lo
largo del tiempo; y los fines de semana bajan el reporting. Por eso cada
comparación entre estados se presenta con su aviso.

## Qué hicimos

- Descargamos y validamos el dataset, y lo limpiamos: fechas a `datetime`,
  eliminación de duplicados por `(state, date)` y auditoría de calidad.
- Excluimos del análisis las 15 columnas con más del 80 % de nulos
  (`dataQualityGrade` y `grade` están vacías al 100 %).
- Calculamos métricas derivadas: positividad, tasa de mortalidad, casos
  diarios y media móvil de 7 días.
- Analizamos la distribución de casos y muertes, 3 relaciones bivariadas y
  la evolución temporal.

## Hallazgos

### 1. Concentración geográfica

California, Texas, Florida, Nueva York e Illinois acumulan el 38 % de los
casos y el 38 % de las muertes. La distribución es muy sesgada: unos pocos
estados están muy por encima de la mediana. Sin normalizar por población no se
puede afirmar que sean los "peores"; son, sobre todo, los más grandes.

### 2. Más tests, más positivos detectados

La correlación entre tests realizados y positivos acumulados es de 0,91. Esto
indica que el volumen de detección sigue al volumen de testing, no
necesariamente al nivel real de contagio. Comparar estados por casos absolutos
es engañoso.

### 3. Positividad y mortalidad no van de la mano

La correlación entre positividad (`positive / totalTestResults`) y tasa de
mortalidad (`death / positive`) es de -0,05: prácticamente nula. La hipótesis
inicial (mayor positividad → mayor mortalidad) **no se sostiene** con estos
datos. El acceso a tests y las diferencias de población atendida pesan más que
la proporción de positivos.

### 4. El reporting tiene ritmo semanal

La media de casos nuevos por día de la semana es más baja los domingos y
lunes que los días centrales de la semana. La serie diaria muestra varias
olas claras; la media móvil de 7 días es la lectura correcta de la tendencia.

## Recomendaciones

1. **Normalizar por población antes de comparar estados.** Cualquier ranking
   por counts debe acompañarse del ratio por 100k habitantes.
2. **Leer la tendencia con media móvil de 7 días**, no con el dato diario, y
   no sacar conclusiones de un solo día.
3. **No usar la positividad como proxy de gravedad.** Para evaluar el impacto
   hay que cruzar con hospitalizaciones y muertes normalizadas.

## Limitaciones

- Subregistro variable por estado y por semana.
- Cambios en la definición de `totalTestResults` a lo largo del periodo.
- Efecto fin de semana en el reporting.
- Comparabilidad limitada entre estados sin normalizar por población.
- `dataQualityGrade` está vacía al 100 %, así que no se puede evaluar la
  calidad declarada del dato.
- No se puede inferir causalidad de una serie temporal observacional.

## Próximos pasos

- Integrar la población por estado y calcular ratios por 100k (N3).
- Detectar y tratar los incrementos negativos y generar la auditoría completa.
- Segmentar por región y por olas temporales.
- Añadir un gráfico interactivo con Plotly para explorar por estado.

---

*Fuente: COVID Tracking Project · States Daily (2020-01-13 → 2021-03-07).
Análisis reproducible en `notebooks/02_eda.ipynb` y `notebooks/01_profiling.ipynb`.*
EOF
echo "written"