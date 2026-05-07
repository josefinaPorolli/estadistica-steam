# Cálculo de probabilidades

Este reporte se realizó con el archivo `data.json` del repositorio. La muestra contiene **44 videojuegos**.

## Criterio usado

Como los datos corresponden a una muestra de videojuegos de Steam, las probabilidades se calculan como **probabilidades empíricas** o **frecuencias relativas**.

La fórmula general utilizada fue:

```text
P(A) = cantidad de casos favorables / cantidad total de casos
```

En este trabajo:

```text
n = 44
```

Se usaron las mismas recodificaciones empleadas en las tablas de contingencia y en las pruebas de independencia:

- **Reseña excelente**: juegos con categoría `Overwhelmingly Positive`.
- **Reseña no excelente**: el resto de categorías de reseñas.
- **Género Action**: juegos cuyo género principal es `Action`.
- **Otros géneros**: todos los géneros distintos de `Action`.
- **Multiplataforma**: juegos disponibles en Windows y al menos otra plataforma.
- **Solo Windows**: juegos disponibles solamente en Windows.

## 1. Probabilidades simples

Las probabilidades simples analizan la ocurrencia de un solo evento.

| Evento | Frecuencia | Fracción | Probabilidad | Porcentaje |
| --- | --- | --- | --- | --- |
| Reseña excelente | 18 | 18/44 | 0,4091 | 40,91% |
| Reseña no excelente | 26 | 26/44 | 0,5909 | 59,09% |
| Género Action | 29 | 29/44 | 0,6591 | 65,91% |
| Otros géneros | 15 | 15/44 | 0,3409 | 34,09% |
| Multiplataforma | 14 | 14/44 | 0,3182 | 31,82% |
| Solo Windows | 30 | 30/44 | 0,6818 | 68,18% |
| Completo Directo | 25 | 25/44 | 0,5682 | 56,82% |
| Early Access | 19 | 19/44 | 0,4318 | 43,18% |

### Interpretación

La probabilidad de seleccionar al azar un videojuego con reseña excelente es:

```text
P(Excelente) = 18/44 = 0,4091 = 40,91%
```

Esto significa que, dentro de la muestra, aproximadamente **4 de cada 10 videojuegos** tienen categoría de reseñas excelente.

También se observa que la categoría más frecuente de género es `Action`:

```text
P(Action) = 29/44 = 0,6591 = 65,91%
```

Por lo tanto, en esta muestra predominan los videojuegos de acción.

## 2. Probabilidades conjuntas

Las probabilidades conjuntas analizan la ocurrencia simultánea de dos eventos.

La fórmula utilizada fue:

```text
P(A ∩ B) = cantidad de casos que cumplen A y B / cantidad total de casos
```

El símbolo `∩` se lee como “intersección” y significa “ocurre A y ocurre B al mismo tiempo”.

### 2.1. Género principal y categoría de reseñas

| Evento conjunto | Frecuencia | Fracción | Probabilidad | Porcentaje |
| --- | --- | --- | --- | --- |
| Action ∩ Excelente | 11 | 11/44 | 0,2500 | 25,00% |
| Action ∩ No excelente | 18 | 18/44 | 0,4091 | 40,91% |
| Otros géneros ∩ Excelente | 7 | 7/44 | 0,1591 | 15,91% |
| Otros géneros ∩ No excelente | 8 | 8/44 | 0,1818 | 18,18% |

Lectura principal:

```text
P(Action ∩ Excelente) = 11/44 = 0,2500 = 25,00%
```

Esto significa que el **25,00%** de los videojuegos de la muestra son, simultáneamente, de género `Action` y tienen reseñas excelentes.

### 2.2. Soporte multiplataforma y categoría de reseñas

| Evento conjunto | Frecuencia | Fracción | Probabilidad | Porcentaje |
| --- | --- | --- | --- | --- |
| Multiplataforma ∩ Excelente | 8 | 8/44 | 0,1818 | 18,18% |
| Multiplataforma ∩ No excelente | 6 | 6/44 | 0,1364 | 13,64% |
| Solo Windows ∩ Excelente | 10 | 10/44 | 0,2273 | 22,73% |
| Solo Windows ∩ No excelente | 20 | 20/44 | 0,4545 | 45,45% |

Lectura principal:

```text
P(Multiplataforma ∩ Excelente) = 8/44 = 0,1818 = 18,18%
```

Esto significa que el **18,18%** de los videojuegos de la muestra son multiplataforma y tienen reseñas excelentes.

### 2.3. Estado de lanzamiento y categoría de reseñas

| Evento conjunto | Frecuencia | Fracción | Probabilidad | Porcentaje |
| --- | --- | --- | --- | --- |
| Completo Directo ∩ Excelente | 11 | 11/44 | 0,2500 | 25,00% |
| Completo Directo ∩ No excelente | 14 | 14/44 | 0,3182 | 31,82% |
| Early Access ∩ Excelente | 7 | 7/44 | 0,1591 | 15,91% |
| Early Access ∩ No excelente | 12 | 12/44 | 0,2727 | 27,27% |

Lectura principal:

```text
P(Early Access ∩ Excelente) = 7/44 = 0,1591 = 15,91%
```

Esto significa que el **15,91%** de los videojuegos de la muestra están en `Early Access` y tienen reseñas excelentes.

## 3. Probabilidades condicionales

Las probabilidades condicionales analizan la probabilidad de que ocurra un evento sabiendo que ya ocurrió otro.

La fórmula utilizada fue:

```text
P(A | B) = P(A ∩ B) / P(B)
```

También puede calcularse directamente con frecuencias:

```text
P(A | B) = cantidad de casos que cumplen A y B / cantidad de casos que cumplen B
```

El símbolo `|` se lee como “dado que”.

| Probabilidad condicional | Cálculo | Probabilidad | Porcentaje | Interpretación |
| --- | --- | --- | --- | --- |
| P(Excelente | Action) | 11/29 | 0,3793 | 37,93% | Probabilidad de reseña excelente sabiendo que el juego es de acción |
| P(Excelente | Otros géneros) | 7/15 | 0,4667 | 46,67% | Probabilidad de reseña excelente sabiendo que el juego no es de acción |
| P(Action | Excelente) | 11/18 | 0,6111 | 61,11% | Probabilidad de que el juego sea Action sabiendo que tiene reseña excelente |
| P(Multiplataforma | Excelente) | 8/18 | 0,4444 | 44,44% | Probabilidad de que el juego sea multiplataforma sabiendo que tiene reseña excelente |
| P(Excelente | Multiplataforma) | 8/14 | 0,5714 | 57,14% | Probabilidad de reseña excelente sabiendo que el juego es multiplataforma |
| P(Excelente | Solo Windows) | 10/30 | 0,3333 | 33,33% | Probabilidad de reseña excelente sabiendo que el juego es solo Windows |
| P(Excelente | Completo Directo) | 11/25 | 0,4400 | 44,00% | Probabilidad de reseña excelente sabiendo que el lanzamiento fue completo directo |
| P(Excelente | Early Access) | 7/19 | 0,3684 | 36,84% | Probabilidad de reseña excelente sabiendo que el juego está en Early Access |

### Interpretación

La comparación más relevante para el trabajo es:

```text
P(Excelente | Multiplataforma) = 8/14 = 57,14%
P(Excelente | Solo Windows) = 10/30 = 33,33%
```

Descriptivamente, los videojuegos multiplataforma tienen una mayor proporción de reseñas excelentes que los videojuegos solo disponibles en Windows. Sin embargo, en la prueba de independencia realizada anteriormente, esta diferencia no fue estadísticamente significativa al 5%.

## 4. Probabilidades complementarias

El complemento de un evento representa que ese evento no ocurre.

La fórmula utilizada fue:

```text
P(Aᶜ) = 1 - P(A)
```

Ejemplo:

```text
P(No excelente) = 1 - P(Excelente)
P(No excelente) = 1 - 18/44
P(No excelente) = 26/44 = 0,5909 = 59,09%
```

Por lo tanto, la probabilidad de seleccionar al azar un videojuego que no tenga reseña excelente es **59,09%**.

Otros complementos relevantes:

```text
P(No Action) = 1 - P(Action) = 15/44 = 34,09%
P(No multiplataforma) = 1 - P(Multiplataforma) = 30/44 = 68,18%
P(No Early Access) = 1 - P(Early Access) = 25/44 = 56,82%
```

## 5. Probabilidades de unión

La unión analiza la probabilidad de que ocurra al menos uno de dos eventos.

La fórmula utilizada fue:

```text
P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
```

El símbolo `∪` se lee como “unión” y significa “ocurre A, ocurre B, o ambos”.

| Evento de unión | Cálculo con frecuencias | Fracción | Probabilidad | Porcentaje |
| --- | --- | --- | --- | --- |
| P(Action ∪ Excelente) | (29 + 18 - 11)/44 | 36/44 | 0,8182 | 81,82% |
| P(Multiplataforma ∪ Excelente) | (14 + 18 - 8)/44 | 24/44 | 0,5455 | 54,55% |
| P(Early Access ∪ Excelente) | (19 + 18 - 7)/44 | 30/44 | 0,6818 | 68,18% |

### Interpretación

Por ejemplo:

```text
P(Action ∪ Excelente) = 36/44 = 0,8182 = 81,82%
```

Esto significa que el **81,82%** de los videojuegos de la muestra son de acción, tienen reseñas excelentes, o cumplen ambas condiciones.

## 6. Conclusión general

El cálculo de probabilidades es pertinente para este trabajo porque el dataset contiene variables categóricas y permite analizar frecuencias relativas, probabilidades conjuntas y probabilidades condicionales.

A partir de los datos se observa que:

- La probabilidad de que un videojuego tenga reseña excelente es **40,91%**.
- La probabilidad de que un videojuego sea de género `Action` es **65,91%**.
- La probabilidad de que un videojuego sea multiplataforma es **31,82%**.
- Entre los videojuegos multiplataforma, la probabilidad de reseña excelente es **57,14%**.
- Entre los videojuegos solo disponibles en Windows, la probabilidad de reseña excelente es **33,33%**.

Estos resultados son descriptivos. Sirven para interpretar la composición de la muestra, pero no implican por sí solos una relación estadísticamente significativa entre las variables. Para evaluar asociación entre variables se utilizan las pruebas de independencia, desarrolladas en el informe correspondiente.
