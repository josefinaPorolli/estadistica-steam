# Informe final

## Portada

**Titulo del proyecto:** _[Completar titulo]_  
**Autores:** _[Completar autores]_  
**Catedra:** Estadistica Aplicada II  
**Institucion:** _[Completar institucion]_  
**Fecha de presentacion:** _[Mes y anio]_

---

## Tabla de contenidos

1. Resumen .................................................. p. __
2. Introduccion ............................................. p. __
3. Metodologia y resultados ................................ p. __
   3.1 Descripcion de la base y variables .................. p. __
   3.2 Medidas resumen y dispersion ........................ p. __
   3.3 Frecuencias por variable ............................ p. __
   3.4 Tablas de contingencia y probabilidades ............. p. __
   3.5 Pruebas de independencia ............................ p. __
   3.6 Estimacion de parametros y pruebas t ................ p. __
   3.7 Dispersogramas bivariados ........................... p. __
4. Conclusiones y recomendaciones .......................... p. __
5. Bibliografia ............................................ p. __
6. Anexos .................................................. p. __

---

## Resumen

Se analizo una muestra de 44 videojuegos de Steam (19 en Early Access y 25 con lanzamiento Completo Directo) para evaluar si el tipo de lanzamiento se asocio con la valoracion de usuarios y la actividad de jugadores. Se aplicaron medidas de tendencia central, dispersion, asimetria y apuntamiento, junto con frecuencias y visualizaciones. Se construyeron tablas de contingencia y se calcularon probabilidades simples, conjuntas y condicionales con recodificaciones de categorias. Se realizaron pruebas Chi-cuadrado de independencia para genero principal, soporte multiplataforma y estado de lanzamiento, y pruebas t de Welch para comparar medias de porcentaje de resenas positivas, jugadores promedio y pico historico de concurrentes. Los resultados no mostraron evidencia estadistica suficiente para asociar categoria de resenas con genero, soporte o estado de lanzamiento (p > 0.05). En las pruebas t, tampoco se detectaron diferencias significativas entre Early Access y Completo Directo para las tres variables cuantitativas. Se concluyo que, en esta muestra, el tipo de lanzamiento no explico diferencias estadisticamente significativas en valoraciones ni en niveles de actividad, aunque la presencia de valores extremos y el tamano muestral limitaron la potencia del analisis.

---

## Introduccion

El estudio tuvo como objetivo evaluar si el tipo de lanzamiento (Early Access vs Completo Directo) se relaciono con la percepcion de los usuarios y con indicadores de actividad en Steam. El trabajo se realizo sobre un conjunto de 44 videojuegos recopilados en el repositorio, con variables cuantitativas y cualitativas. Se analizaron precio base, porcentaje de resenas positivas, jugadores promedio, pico historico de concurrentes, categoria de resenas, genero principal y soporte multiplataforma. Para asegurar comparabilidad y poder aplicar pruebas de independencia, algunas categorias fueron recodificadas (por ejemplo, reseña excelente vs no excelente). La principal limitacion fue el tamano muestral y la presencia de valores extremos en algunos juegos, lo que incremento la variabilidad y redujo la capacidad para detectar diferencias.

---

## Metodologia y resultados

### 3.1 Descripcion de la base y variables

La base se compuso de 44 videojuegos de Steam: 19 en Early Access y 25 con lanzamiento completo directo. Se consideraron:

- Variables cuantitativas: precio base (USD), porcentaje de resenas positivas, jugadores promedio y pico historico de concurrentes.
- Variables cualitativas: categoria de resenas, genero principal, soporte multiplataforma y estado de lanzamiento.

### 3.2 Medidas resumen y dispersion

Se calcularon medidas de tendencia central y posicion por grupo, junto con medidas de dispersion (varianza muestral, desviacion estandar, rango, RIQ y coeficiente de variacion). En general, las variables de actividad (jugadores promedio y pico historico) mostraron alta variabilidad y fuerte asimetria, especialmente en Completo Directo, debido a valores extremos.

- Ver detalle en [reportes/medidas_resumen.md](medidas_resumen.md) y [reportes/medidas_dispersion_y_z_videojuegos.md](medidas_dispersion_y_z_videojuegos.md).
- Asimetria y apuntamiento por grupo en [reportes/asimetria_y_apuntamiento.md](asimetria_y_apuntamiento.md).

### 3.3 Frecuencias por variable

Se elaboraron tablas de frecuencias y visualizaciones por variable y por estado de lanzamiento:

- Precio base: [reportes/variables/precio_base_usd.md](variables/precio_base_usd.md)
- Porcentaje de resenas positivas: [reportes/variables/porcentaje_resenas_positivas.md](variables/porcentaje_resenas_positivas.md)
- Categoria de resenas: [reportes/variables/categoria_resenas.md](variables/categoria_resenas.md)
- Pico historico de concurrentes: [reportes/variables/pico_historico_concurrentes.md](variables/pico_historico_concurrentes.md)
- Jugadores promedio: [reportes/variables/jugadores_promedio.md](variables/jugadores_promedio.md)
- Soporte multiplataforma: [reportes/variables/soporte_multiplataforma.md](variables/soporte_multiplataforma.md)
- Genero principal: [reportes/variables/genero_principal.md](variables/genero_principal.md)

### 3.4 Tablas de contingencia y probabilidades

Se realizaron recodificaciones para evaluar asociaciones con categoria de resenas (Excelente vs No excelente). Se construyeron tablas de contingencia con frecuencias conjuntas, marginales y condicionales, y se calcularon probabilidades simples, conjuntas y condicionales sobre la muestra.

- Tablas de contingencia: [reportes/Tablas_de_contingencia.md](Tablas_de_contingencia.md)
- Calculo de probabilidades: [reportes/Calculo_de_probabilidades_completo.md](Calculo_de_probabilidades_completo.md)

### 3.5 Pruebas de independencia

Se aplico Chi-cuadrado de independencia entre:

- Genero principal recodificado y categoria de resenas.
- Soporte multiplataforma y categoria de resenas.
- Estado de lanzamiento y categoria de resenas.

En los tres casos los valores p fueron mayores que 0.05, por lo que no se rechazo la hipotesis nula de independencia.

- Detalle en [reportes/Pruebas_de_independencia_completo.md](Pruebas_de_independencia_completo.md).

### 3.6 Estimacion de parametros y pruebas t

Se estimaron medias por grupo y se aplicaron pruebas t de Welch para comparar Early Access y Completo Directo en:

- Porcentaje de resenas positivas.
- Jugadores promedio.
- Pico historico de concurrentes.

Ninguna prueba resulto significativa al 5% (p > 0.05). La diferencia en jugadores promedio se vio afectada por valores extremos en Completo Directo.

- Detalle en [reportes/variables/parametros_hipotesis.md](variables/parametros_hipotesis.md).

### 3.7 Dispersogramas bivariados

Se generaron dispersogramas entre pares de variables cuantitativas, separando Early Access y Completo Directo. Estos graficos mostraron alta dispersion y concentracion de valores bajos, con outliers notorios en picos historicos y jugadores promedio.

- Ver graficos en [reportes/dispersogramas.md](dispersogramas.md).

---

## Conclusiones y recomendaciones

### Conclusiones

- No se encontro evidencia estadistica suficiente para afirmar que el tipo de lanzamiento influya en el porcentaje de resenas positivas, jugadores promedio o pico historico de concurrentes.
- Las pruebas de independencia no mostraron asociacion significativa entre categoria de reseñas y genero, soporte multiplataforma o estado de lanzamiento.
- La muestra presento alta variabilidad y outliers, especialmente en variables de actividad, lo que condiciono la interpretacion.

### Recomendaciones

- Ampliar el tamano muestral para incrementar potencia estadistica.
- Incorporar variables adicionales (por ejemplo, antiguedad del juego, precio con descuento, etiquetas de genero secundario).
- Separar analisis por rangos de popularidad para reducir el efecto de valores extremos.
- Repetir pruebas con recodificaciones alternativas en categorias poco frecuentes.

---

## Bibliografia

- _[Completar fuentes del dataset y referencias externas si las hubiera]_

---

## Anexos

- Base de datos y archivos de trabajo (no procesados).
- Tablas y graficos completos por variable.
- Formulas utilizadas en los calculos.

Ver indices en [reportes/index.md](index.md).
