## Estimacion de parametros

Basado en el commit 2ba2a6d.

### A. Variable: Porcentaje de resenas positivas (%)

- Media estimada Early Access (EA): 85.14%
- Media estimada Completo Directo (CD): 91.63%
- Estimacion puntual (diferencia): los juegos de Completo Directo superan en promedio a los Early Access por 6.49 puntos porcentuales.
- Intervalo de confianza (95%): el intervalo para la diferencia de medias es de [-15.16% , 2.18%].
- Interpretacion: como el intervalo contiene al cero, la diferencia observada en la muestra podria deberse a la variabilidad (azar) y no asegura que en toda la plataforma Steam la diferencia real siga esta tendencia.

### B. Variable: Jugadores promedio

- Media estimada EA: 22,424 jugadores simultaneos diarios en promedio.
- Media estimada CD: 80,744 jugadores simultaneos diarios en promedio.

### C. Variable: Pico historico de concurrentes (CCU)

- Media estimada EA: 276,530 jugadores maximos simultaneos.
- Media estimada CD: 341,400 jugadores maximos simultaneos.

## Pruebas de hipotesis

Dado que el objetivo general es "evaluar si este tipo de lanzamiento influye positiva o negativamente...", se aplican pruebas estadisticas t de Welch (ideales para varianzas y tamanos de muestra desiguales) para las tres variables principales.

- Nivel de significancia fijado: 0.05 (5%)

### Prueba 1: Valoracion de los usuarios (% de resenas positivas)

- Hipotesis nula (H0): el tipo de lanzamiento NO influye en el porcentaje de resenas positivas (ea = cd).
- Hipotesis alternativa (H1): el tipo de lanzamiento influye en el porcentaje de resenas positivas (ea ≠ cd).
- Resultados:
  - Valor t = -1.55
  - Valor p = 0.134
- Decision: como p > 0.05, no se rechaza la H0.
- Conclusion: no hay evidencia estadistica suficiente para afirmar que el lanzamiento en Early Access afecte (positiva o negativamente) la valoracion porcentual final del juego comparado con un lanzamiento directo.

### Prueba 2: Cantidad de jugadores promedio

- Hipotesis nula (H0): el tipo de lanzamiento NO influye en la cantidad de jugadores promedio.
- Resultados:
  - Valor t = -1.07
  - Valor p = 0.295
- Decision: como p > 0.05, no se rechaza la H0.
- Conclusion: la enorme diferencia en las medias (22 mil vs 80 mil) esta muy influenciada por valores extremos en el grupo CD (como Counter-Strike 2 con 1.3 millones). Estadisticamente, la variabilidad es tan grande que el formato de lanzamiento no predice una mayor retencion promedio.

### Prueba 3: Pico historico de concurrentes

- Hipotesis nula (H0): el tipo de lanzamiento NO influye en el pico maximo de jugadores.
- Resultados:
  - Valor t = -0.46
  - Valor p = 0.643
- Decision: como p > 0.05, no se rechaza la H0.
- Conclusion: no existe relacion estadisticamente comprobable entre haber pasado por un periodo de Early Access y el pico maximo de jugadores que el titulo lograra en su historia.
