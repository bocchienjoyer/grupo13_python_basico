# Assignment 3 – Lluvias y declaratorias de emergencia en el Perú

**Grupo 13 · Fundamentos de Python**

**Período de análisis:** 1 de enero al 31 de mayo de 2022.

**Datos:** opción B, tabla final de lluvias y decretos de emergencia por departamento (`datos/dataset.csv`, copia de `assignment_2/datos/tabla_final.csv`).

**Dashboard público:** pendiente de despliegue en Streamlit Community Cloud. Agregar el enlace cuando esté publicado.

## Contenido de la carpeta

| Archivo | Qué contiene |
|---|---|
| `visualizacion.ipynb` | Parte 1: gráficos interactivos con Plotly Express |
| `mapas.ipynb` | Parte 2: mapas coropléticos con GeoPandas y Folium |
| `app.py` | Parte 3: dashboard en Streamlit |
| `requirements.txt` | Librerías necesarias |
| `datos/dataset.csv` | Tabla final del Assignment 2 (25 departamentos) |
| `datos/departamentos_peru.geojson` | Límites departamentales del Perú |

## 1. Pregunta

¿Los departamentos donde más llovió fueron los que recibieron declaratorias de emergencia?

## 2. Datos

- **`dataset.csv`**: copia sin cambios de `assignment_2/datos/tabla_final.csv`. Tiene una fila por departamento (25) con: `ubigeo`, `departamento`, `declaratorias`, `prorrogas`, `capital`, `latitud`, `longitud`, `lluvia_total_mm` y `dias_lluvia_fuerte`.
- Las declaratorias y prórrogas provienen de los decretos de emergencia recopilados en el Assignment 2; la lluvia corresponde a la registrada en la **capital** de cada departamento durante la temporada asignada.
- **`departamentos_peru.geojson`**: geometrías departamentales. No incluye ubigeo, así que el dashboard empareja por nombre normalizado (sin tildes, en mayúsculas) y luego cruza el mapa por `ubigeo` leído como texto (`'01'`, no `1`). Los 25 departamentos cruzan; el reporte de cruce está en la pestaña **Mapa**.

## 3. Hallazgos

1. **Más lluvia no significó emergencia.** Loreto (1 581,8 mm y 25 días de lluvia fuerte) y Ucayali (1 288,8 mm y 20 días) fueron los departamentos más lluviosos, pero ninguno recibió declaratoria.
2. **Las 3 declaratorias cayeron en departamentos con lluvia moderada o baja.** Amazonas (436,5 mm), Ayacucho (485,1 mm) y Piura (89,2 mm) promedian 336,9 mm, por debajo del promedio nacional de 531,6 mm. Ninguno de los 12 departamentos con más de 700 mm tuvo declaratoria.

## 4. Limitaciones

- La lluvia se midió en la **capital** de cada departamento, no en todo su territorio. Una capital seca puede esconder zonas con lluvias intensas (por ejemplo, Lima figura con su capital Huacho).
- Solo hay **3 declaratorias** y **ninguna prórroga** en la temporada, demasiado pocas para hablar de una relación estadística entre lluvia y emergencias.
- Las declaratorias pueden responder a huaicos, desbordes o daños acumulados, que dependen de la pendiente, la vulnerabilidad y la infraestructura, no solo del total de lluvia.
- El GeoJSON no trae ubigeo; el cruce depende de que los nombres coincidan una vez normalizados.

## Cómo usar el dashboard

En la barra lateral puedes:
- elegir la variable del ranking y del mapa (lluvia acumulada, días de lluvia fuerte o declaratorias);
- seleccionar departamentos;
- limitar el rango de lluvia acumulada;
- mostrar solo los departamentos con declaratoria.

Las métricas, los gráficos, el mapa y la tabla se actualizan con cada filtro. La tabla filtrada se puede descargar en CSV.

## Correr en local

Desde la carpeta `assignment_3/`:

```bash
uv run streamlit run app.py
```

