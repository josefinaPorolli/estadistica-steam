# Tablas de contingencia: frecuencias conjuntas, marginales y condicionales

Este reporte se realizó con el archivo `data.json` del repositorio. La muestra contiene **44 videojuegos**.

## Criterio usado

Para que las tablas sean más claras y compatibles con las pruebas de independencia, se usaron las mismas recodificaciones del informe de Chi-cuadrado:

- **Categoría de reseñas**: `Excelente` = `Overwhelmingly Positive`; `No excelente` = el resto de categorías.
- **Género principal**: `Action`; `Otros géneros` = todos los géneros que no son Action.
- **Soporte multiplataforma**: `Solo Windows`; `Multiplataforma` = juegos disponibles en Windows y al menos otra plataforma.

En todas las tablas, las frecuencias conjuntas muestran cuántos videojuegos pertenecen simultáneamente a dos categorías. Las marginales son los totales por fila y por columna. Las condicionales muestran porcentajes calculados dentro de una fila o columna.

## Tabla 1. Género principal vs categoría de reseñas

Variables cruzadas: **género principal recodificado** y **categoría de reseñas recodificada**.

### Frecuencias conjuntas y marginales

Las celdas internas son **frecuencias conjuntas absolutas**. La última fila y la última columna son las **frecuencias marginales**.

| genero_rec    |   Excelente |   No excelente |   Total |
|:--------------|------------:|---------------:|--------:|
| Action        |          11 |             18 |      29 |
| Otros géneros |           7 |              8 |      15 |
| Total         |          18 |             26 |      44 |


### Frecuencias condicionales por fila

Cada fila suma 100%. Se interpreta como la distribución de **categoría de reseñas recodificada** dentro de cada categoría de **género principal recodificado**.

| genero_rec    | Excelente   | No excelente   |
|:--------------|:------------|:---------------|
| Action        | 37.93%      | 62.07%         |
| Otros géneros | 46.67%      | 53.33%         |


### Frecuencias condicionales por columna

Cada columna suma 100%. Se interpreta como la distribución de **género principal recodificado** dentro de cada categoría de **categoría de reseñas recodificada**.

| genero_rec    | Excelente   | No excelente   |
|:--------------|:------------|:---------------|
| Action        | 61.11%      | 69.23%         |
| Otros géneros | 38.89%      | 30.77%         |


### Lectura breve

Entre los juegos de acción, el **37,93%** tiene reseñas excelentes y el **62,07%** no excelentes. En los otros géneros, el **46,67%** tiene reseñas excelentes y el **53,33%** no excelentes. La diferencia existe descriptivamente, pero no es fuerte; por eso en la prueba de independencia no se encontró asociación estadísticamente significativa.

## Tabla 2. Soporte multiplataforma vs categoría de reseñas

Variables cruzadas: **soporte de plataforma** y **categoría de reseñas recodificada**.

### Frecuencias conjuntas y marginales

Las celdas internas son **frecuencias conjuntas absolutas**. La última fila y la última columna son las **frecuencias marginales**.

| soporte_categoria   |   Excelente |   No excelente |   Total |
|:--------------------|------------:|---------------:|--------:|
| Multiplataforma     |           8 |              6 |      14 |
| Solo Windows        |          10 |             20 |      30 |
| Total               |          18 |             26 |      44 |


### Frecuencias condicionales por fila

Cada fila suma 100%. Se interpreta como la distribución de **categoría de reseñas recodificada** dentro de cada categoría de **soporte de plataforma**.

| soporte_categoria   | Excelente   | No excelente   |
|:--------------------|:------------|:---------------|
| Multiplataforma     | 57.14%      | 42.86%         |
| Solo Windows        | 33.33%      | 66.67%         |


### Frecuencias condicionales por columna

Cada columna suma 100%. Se interpreta como la distribución de **soporte de plataforma** dentro de cada categoría de **categoría de reseñas recodificada**.

| soporte_categoria   | Excelente   | No excelente   |
|:--------------------|:------------|:---------------|
| Multiplataforma     | 44.44%      | 23.08%         |
| Solo Windows        | 55.56%      | 76.92%         |


### Lectura breve

Entre los juegos multiplataforma, el **57,14%** tiene reseñas excelentes. Entre los juegos solo disponibles en Windows, el **33,33%** tiene reseñas excelentes. Descriptivamente, los multiplataforma presentan mayor proporción de reseñas excelentes, aunque la prueba de independencia no alcanzó significancia estadística al 5%.

## Tabla 3. Estado de lanzamiento vs categoría de reseñas

Variables cruzadas: **estado de lanzamiento** y **categoría de reseñas recodificada**.

### Frecuencias conjuntas y marginales

Las celdas internas son **frecuencias conjuntas absolutas**. La última fila y la última columna son las **frecuencias marginales**.

| estado_lanzamiento   |   Excelente |   No excelente |   Total |
|:---------------------|------------:|---------------:|--------:|
| Completo Directo     |          11 |             14 |      25 |
| Early Access         |           7 |             12 |      19 |
| Total                |          18 |             26 |      44 |


### Frecuencias condicionales por fila

Cada fila suma 100%. Se interpreta como la distribución de **categoría de reseñas recodificada** dentro de cada categoría de **estado de lanzamiento**.

| estado_lanzamiento   | Excelente   | No excelente   |
|:---------------------|:------------|:---------------|
| Completo Directo     | 44.00%      | 56.00%         |
| Early Access         | 36.84%      | 63.16%         |


### Frecuencias condicionales por columna

Cada columna suma 100%. Se interpreta como la distribución de **estado de lanzamiento** dentro de cada categoría de **categoría de reseñas recodificada**.

| estado_lanzamiento   | Excelente   | No excelente   |
|:---------------------|:------------|:---------------|
| Completo Directo     | 61.11%      | 53.85%         |
| Early Access         | 38.89%      | 46.15%         |


### Lectura breve

Entre los juegos con lanzamiento completo directo, el **44,00%** tiene reseñas excelentes. Entre los juegos en Early Access, el **36,84%** tiene reseñas excelentes. Las proporciones son bastante similares, por lo que descriptivamente no se observa una diferencia marcada.

## Conclusión general

Las tablas de contingencia permiten describir cómo se distribuyen conjuntamente las variables categóricas del conjunto de datos. En este caso, la mayor diferencia descriptiva aparece entre **soporte multiplataforma** y **categoría de reseñas**, porque los juegos multiplataforma presentan mayor proporción de reseñas excelentes que los juegos solo disponibles en Windows. Sin embargo, estas tablas describen frecuencias; para decidir si la asociación es estadísticamente significativa se debe consultar el informe de pruebas de independencia.
