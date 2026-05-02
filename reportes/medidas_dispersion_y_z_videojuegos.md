# Medidas de dispersión y puntuaciones Z

Cálculos agrupados por estado de lanzamiento. Se usó **varianza y desviación estándar muestral** (`n-1`).

## Medidas de dispersión

| Estado           | Variable                    |   n | Mínimo    | Máximo       | Rango        | Q1        | Q3         | RIQ        | Varianza muestral   | Desv. estándar muestral   |   Coef. variación % |
|:-----------------|:----------------------------|----:|:----------|:-------------|:-------------|:----------|:-----------|:-----------|:--------------------|:--------------------------|--------------------:|
| Completo Directo | Precio base (USD)           |  25 | 0.00      | 59.99        | 59.99        | 14.99     | 39.99      | 25.00      | 381.78              | 19.54                     |               57.82 |
| Completo Directo | % reseñas positivas         |  25 | 76.20     | 98.70        | 22.50        | 87.20     | 97.00      | 9.80       | 38.97               | 6.24                      |                6.81 |
| Completo Directo | Pico histórico concurrentes |  25 | 2,264.00  | 1,862,531.00 | 1,860,267.00 | 95,655.00 | 458,709.00 | 363,054.00 | 187,846,289,756.31  | 433,412.38                |              126.95 |
| Completo Directo | Jugadores promedio          |  25 | 87.00     | 1,373,891.00 | 1,373,804.00 | 6,349.00  | 33,391.00  | 27,042.00  | 73,538,707,506.26   | 271,180.21                |              335.85 |
| Early Access     | Precio base (USD)           |  19 | 0.00      | 49.99        | 49.99        | 19.99     | 29.99      | 10.00      | 144.42              | 12.02                     |               48.09 |
| Early Access     | % reseñas positivas         |  19 | 29.60     | 98.40        | 68.80        | 79.80     | 96.85      | 17.05      | 301.41              | 17.36                     |               20.39 |
| Early Access     | Pico histórico concurrentes |  19 | 15,263.00 | 2,101,867.00 | 2,086,604.00 | 49,295.00 | 256,194.00 | 206,899.00 | 224,432,245,445.00  | 473,742.81                |              171.32 |
| Early Access     | Jugadores promedio          |  19 | 211.00    | 115,537.00   | 115,326.00   | 5,484.00  | 28,362.50  | 22,878.50  | 665,217,035.56      | 25,791.80                 |              115.02 |

## Puntuaciones Z por videojuego

### Completo Directo

| Videojuego                                  |   Z Precio |   Z % positivas |   Z Pico histórico |   Z Jugadores promedio |
|:--------------------------------------------|-----------:|----------------:|-------------------:|-----------------------:|
| Counter-Strike 2                            |      -1.73 |           -0.79 |               3.51 |                   4.77 |
| Grand Theft Auto V Legacy                   |      -1.73 |           -0.68 |               0.05 |                   0.02 |
| The Witcher 3: Wild Hunt                    |       0.32 |            0.72 |              -0.55 |                  -0.24 |
| Cyberpunk 2077                              |       1.34 |           -1.16 |               1.65 |                  -0.17 |
| Hollow Knight                               |      -0.96 |            0.86 |              -0.57 |                  -0.27 |
| Elden Ring                                  |       1.34 |            0.2  |               1.41 |                  -0.18 |
| Red Dead Redemption 2                       |       1.34 |            0.09 |              -0.56 |                  -0.2  |
| Terraria                                    |      -1.22 |            0.94 |               0.34 |                  -0.21 |
| Stardew Valley                              |      -0.96 |            1.08 |              -0.24 |                  -0.12 |
| Portal 2                                    |      -1.22 |            1.13 |              -0.56 |                  -0.29 |
| HELLDIVERS™ 2                               |       0.32 |           -2.47 |               0.27 |                  -0.12 |
| Monster Hunter: World                       |      -0.19 |           -0.58 |              -0.02 |                  -0.26 |
| Sekiro™: Shadows Die Twice                  |       1.34 |            0.59 |              -0.5  |                  -0.29 |
| The Elder Scrolls V: Skyrim Special Edition |       0.32 |            0.06 |              -0.63 |                  -0.21 |
| Fallout 4                                   |      -0.71 |           -1.37 |               0.3  |                  -0.25 |
| DOOM Eternal                                |       0.32 |           -0.07 |              -0.55 |                  -0.29 |
| Baldur's Gate 3                             |       1.34 |            0.83 |               1.23 |                  -0.14 |
| Rust                                        |       0.32 |           -0.71 |              -0.18 |                   0.22 |
| Subnautica                                  |      -0.19 |            0.86 |              -0.67 |                  -0.27 |
| Factorio                                    |       0.06 |            0.86 |              -0.51 |                  -0.23 |
| Hades                                       |      -0.45 |            1.05 |              -0.66 |                  -0.28 |
| Ghostrunner 2                               |       0.32 |           -1.75 |              -0.78 |                  -0.3  |
| Assetto Corsa Competizione                  |       0.32 |            0.14 |              -0.76 |                  -0.28 |
| The Binding of Isaac: Rebirth               |      -0.96 |            0.91 |              -0.62 |                  -0.22 |
| Sid Meier's Civilization VI                 |       1.34 |           -0.76 |              -0.41 |                  -0.19 |

### Early Access

| Videojuego             |   Z Precio |   Z % positivas |   Z Pico histórico |   Z Jugadores promedio |
|:-----------------------|-----------:|----------------:|-------------------:|-----------------------:|
| Palworld               |       0.42 |            0.52 |               3.85 |                  -0.24 |
| Manor Lords            |       1.25 |            0.07 |              -0.22 |                  -0.7  |
| Valheim                |      -0.42 |            0.53 |               0.48 |                   0.14 |
| Phasmophobia           |      -0.42 |            0.61 |              -0.35 |                  -0.3  |
| Project Zomboid        |      -0.42 |            0.52 |              -0.45 |                   0.29 |
| Enshrouded             |       0.42 |            0.07 |              -0.25 |                  -0.12 |
| BeamNG.drive           |      -0    |            0.71 |              -0.5  |                   0.2  |
| Bellwright             |       0.42 |           -0.26 |              -0.55 |                  -0.74 |
| Dyson Sphere Program   |      -0.42 |            0.72 |              -0.46 |                  -0.75 |
| Kerbal Space Program 2 |       2.08 |           -3.2  |              -0.53 |                  -0.86 |
| Infection Free Zone    |      -0    |           -0.35 |              -0.54 |                  -0.84 |
| ARK: Survival Ascended |       1.66 |           -1.5  |              -0.38 |                   0.05 |
| Far Far West           |      -0.42 |            0.73 |              -0.52 |                   0.26 |
| Windrose               |       0.42 |            0.14 |              -0.11 |                   3.61 |
| Path of Exile 2        |       0.42 |           -0.87 |               0.64 |                  -0.56 |
| VRChat                 |      -2.08 |           -0.55 |              -0.42 |                   0.84 |
| Lethal Company         |      -1.25 |            0.69 |              -0.08 |                  -0.61 |
| Schedule 1             |      -0.42 |            0.76 |               0.39 |                  -0.07 |
| R.E.P.O.               |      -1.25 |            0.65 |              -0.01 |                   0.4  |

