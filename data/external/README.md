# Segunda fuente: población por estado

`population.csv` contiene la población por estado/territorio de EE. UU. y se
usa para calcular ratios por 100k habitantes.

| Columna | Tipo | Significado |
|---|---|---|
| `state` | texto | Abreviatura de dos letras |
| `population` | entero | Población del estado o territorio |

## Fuente

- **50 estados + DC**: U.S. Census Bureau, población 2014 (dataset público de
  Plotly, `2014_usa_states.csv`). Se usa como aproximación de la población del
  periodo 2020-2021.
- **Territorios (PR, GU, VI, AS, MP)**: estimaciones del Censo 2020.

## Advertencia

La población es de 2014 (estados) y 2020 (territorios), no del mismo año. Los
ratios por 100k son válidos para **comparar** estados, pero las cifras
absolutas por 100k deben leerse con esta reserva. La fuente y el año se
documentan aquí para que sea discutible.
EOF
