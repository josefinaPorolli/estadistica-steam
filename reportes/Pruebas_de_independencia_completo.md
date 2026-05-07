# Pruebas de independencia

## Objetivo

El objetivo de esta sección es analizar si existe asociación estadística entre algunas variables categóricas del conjunto de videojuegos de Steam. Para ello se utiliza la prueba Chi-cuadrado de independencia.

Una prueba de independencia permite evaluar si dos variables cualitativas están relacionadas entre sí o si, por el contrario, se comportan de manera independiente. En este trabajo se analiza si ciertas características de los videojuegos, como el género, el soporte multiplataforma o el estado de lanzamiento, están asociadas con la categoría de reseñas recibida.

## Variables utilizadas

El conjunto de datos contiene 44 videojuegos. Para realizar las pruebas de independencia se consideraron variables categóricas, ya que este tipo de prueba requiere trabajar con frecuencias organizadas en tablas de contingencia.

Las variables categóricas disponibles son:

- `categoria_resenas`
- `genero_principal`
- `soporte_multiplataforma`
- `estado_lanzamiento`

Sin embargo, algunas categorías tienen frecuencias muy bajas. Por ejemplo, en `categoria_resenas` aparecen categorías como `Mixed`, `Mostly Negative` y `Mostly Positive` con muy pocos casos. Lo mismo ocurre con algunos géneros como `Casual`, `Strategy` o `Simulation`.

Por este motivo, para obtener pruebas más interpretables, se agruparon algunas categorías.

## Recodificación de variables

### Categoría de reseñas

Se transformó la variable `categoria_resenas` en una variable binaria:

| Categoría original | Categoría recodificada |
|---|---|
| Overwhelmingly Positive | Excelente |
| Very Positive, Mostly Positive, Mixed, Mostly Negative | No excelente |

La idea es diferenciar los juegos con reseñas extremadamente positivas de los demás.

### Género principal

Como el género `Action` concentra la mayor cantidad de videojuegos, se recodificó la variable `genero_principal` de la siguiente manera:

| Categoría original | Categoría recodificada |
|---|---|
| Action | Action |
| RPG, Indie, Adventure, Racing, Casual, Strategy, Simulation | Otros géneros |

### Soporte multiplataforma

La variable `soporte_multiplataforma` se recodificó en dos categorías:

| Soporte original | Categoría recodificada |
|---|---|
| Windows | Solo Windows |
| Windows + Mac, Windows + Linux, Windows + Mac + Linux | Multiplataforma |

## Hipótesis generales

Para cada prueba se plantean las siguientes hipótesis:

**Hipótesis nula (H₀):** las variables analizadas son independientes.

**Hipótesis alternativa (H₁):** las variables analizadas no son independientes, es decir, existe asociación entre ellas.

Se trabaja con un nivel de significancia:

\[
\alpha = 0,05
\]

Criterio de decisión:

- Si el valor p es menor o igual que 0,05, se rechaza H₀.
- Si el valor p es mayor que 0,05, no se rechaza H₀.

---

# Prueba 1: Género principal y categoría de reseñas

## Planteo

Se busca analizar si el género principal del videojuego está asociado con la categoría de reseñas.

En particular, se compara si los juegos de género `Action` tienen una proporción diferente de reseñas excelentes respecto de los demás géneros.

## Tabla de contingencia

| Género agrupado | Excelente | No excelente | Total |
|---|---:|---:|---:|
| Action | 11 | 18 | 29 |
| Otros géneros | 7 | 8 | 15 |
| Total | 18 | 26 | 44 |

## Frecuencias esperadas

| Género agrupado | Excelente | No excelente |
|---|---:|---:|
| Action | 11,86 | 17,14 |
| Otros géneros | 6,14 | 8,86 |

## Resultado de la prueba

| Medida | Valor |
|---|---:|
| Estadístico Chi-cuadrado | 0,3121 |
| Grados de libertad | 1 |
| Valor p | 0,5764 |
| Nivel de significancia | 0,05 |

## Decisión

Como el valor p = 0,5764 es mayor que 0,05, no se rechaza la hipótesis nula.

## Conclusión

No existe evidencia estadística suficiente para afirmar que el género principal agrupado esté asociado con la categoría de reseñas. En esta muestra, no se puede concluir que los juegos de acción tengan una proporción significativamente diferente de reseñas excelentes respecto de los demás géneros.

---

# Prueba 2: Soporte multiplataforma y categoría de reseñas

## Planteo

Se busca analizar si el soporte multiplataforma de un videojuego está asociado con la categoría de reseñas.

La pregunta de investigación es si los juegos disponibles en más de una plataforma tienden a tener una proporción diferente de reseñas excelentes en comparación con los juegos disponibles solamente en Windows.

## Tabla de contingencia

| Soporte agrupado | Excelente | No excelente | Total |
|---|---:|---:|---:|
| Multiplataforma | 8 | 6 | 14 |
| Solo Windows | 10 | 20 | 30 |
| Total | 18 | 26 | 44 |

## Frecuencias esperadas

| Soporte agrupado | Excelente | No excelente |
|---|---:|---:|
| Multiplataforma | 5,73 | 8,27 |
| Solo Windows | 12,27 | 17,73 |

## Resultado de la prueba

| Medida | Valor |
|---|---:|
| Estadístico Chi-cuadrado | 2,2385 |
| Grados de libertad | 1 |
| Valor p | 0,1346 |
| Nivel de significancia | 0,05 |

## Decisión

Como el valor p = 0,1346 es mayor que 0,05, no se rechaza la hipótesis nula.

## Conclusión

No existe evidencia estadística suficiente para afirmar que el soporte multiplataforma esté asociado con la categoría de reseñas. Aunque en la muestra los juegos multiplataforma presentan una mayor proporción de reseñas excelentes, la diferencia no es estadísticamente significativa al 5%.

---

# Prueba 3: Estado de lanzamiento y categoría de reseñas

## Planteo

Se busca analizar si el estado de lanzamiento del videojuego está asociado con la categoría de reseñas.

La pregunta de investigación es si los juegos lanzados como `Early Access` tienen una proporción diferente de reseñas excelentes respecto de los juegos con lanzamiento completo directo.

## Tabla de contingencia

| Estado de lanzamiento | Excelente | No excelente | Total |
|---|---:|---:|---:|
| Completo Directo | 11 | 14 | 25 |
| Early Access | 7 | 12 | 19 |
| Total | 18 | 26 | 44 |

## Frecuencias esperadas

| Estado de lanzamiento | Excelente | No excelente |
|---|---:|---:|
| Completo Directo | 10,23 | 14,77 |
| Early Access | 7,77 | 11,23 |

## Resultado de la prueba

| Medida | Valor |
|---|---:|
| Estadístico Chi-cuadrado | 0,2288 |
| Grados de libertad | 1 |
| Valor p | 0,6324 |
| Nivel de significancia | 0,05 |

## Decisión

Como el valor p = 0,6324 es mayor que 0,05, no se rechaza la hipótesis nula.

## Conclusión

No existe evidencia estadística suficiente para afirmar que el estado de lanzamiento esté asociado con la categoría de reseñas. En esta muestra, no se puede concluir que los juegos en `Early Access` tengan una proporción significativamente diferente de reseñas excelentes respecto de los juegos con lanzamiento completo directo.

---

# Conclusión general

Se realizaron tres pruebas Chi-cuadrado de independencia para analizar posibles asociaciones entre variables categóricas del conjunto de videojuegos de Steam.

Las pruebas realizadas fueron:

1. Género principal agrupado y categoría de reseñas.
2. Soporte multiplataforma y categoría de reseñas.
3. Estado de lanzamiento y categoría de reseñas.

En los tres casos, los valores p fueron mayores que 0,05. Por lo tanto, no se rechazó la hipótesis nula de independencia en ninguna de las pruebas.

Esto significa que, con los datos disponibles, no se encontró evidencia estadística suficiente para afirmar que la categoría de reseñas esté asociada con el género principal, el soporte multiplataforma o el estado de lanzamiento del videojuego.

Es importante aclarar que la muestra utilizada es relativamente pequeña, ya que contiene 44 videojuegos. Además, algunas categorías originales tenían muy pocos casos, por lo que fue necesario agrupar variables para que las pruebas fueran más adecuadas e interpretables.

