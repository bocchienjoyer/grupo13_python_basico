# Assignment 3 – Visualización, mapas y dashboard

**Grupo 13** · Entrega: domingo 11 de octubre de 2026, 11:59 p. m.

## Estado

Estructura inicial preparada. Dataset, responsables, análisis y despliegue pendientes. Los notebooks contienen secciones de trabajo; todavía no son entregables terminados.

## Elección de datos

Pendiente elegir una opción:
- **A:** datos de población/ciudades del Assignment 1, enriquecidos con variables geográficas.
- **B:** tabla_final.csv del Assignment 2 o tasas_departamento.csv de la sesión 6; sin scraping ni API nuevos.
- **C:** dataset público sencillo con dimensión geográfica departamental.

El archivo datos/dataset.csv está vacío de forma intencional hasta tomar esa decisión. No modificar assignment_1/ ni assignment_2/.

## Archivos

- visualizacion.ipynb: tres gráficos Plotly, verificación de valores extremos y exportación de grafico.html.
- mapas.ipynb: cruce por ubigeo, reporte de no cruces, dos coropletas estáticas por cuantiles y mapa Folium con tooltip.
- app.py: plantilla del dashboard Streamlit.
- requirements.txt: dependencias base; ajustar según la implementación final.
- datos/: dataset y archivos geográficos.

## Pregunta

Pendiente.

## Datos y fuentes

Pendiente: fuente, periodo, unidad geográfica y columnas utilizadas.

## Dos hallazgos

1. Pendiente.
2. Pendiente.

## Limitaciones

Pendiente.

## Dashboard público

Pendiente de desplegar en Streamlit Community Cloud y verificar en incógnito.

## Ejecutar en local

Desde assignment_3/:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Antes de entregar

- [ ] Elegir y documentar el dataset.
- [ ] Completar ambos notebooks y ejecutarlos de principio a fin con resultados visibles, sin guardar las salidas pesadas de Folium.
- [ ] Exportar grafico.html desde visualizacion.ipynb.
- [ ] Completar filtros, métricas, gráficos, mapa y tabla del dashboard.
- [ ] Desplegar y verificar el enlace público en incógnito.
- [ ] Completar este README: pregunta, datos, dos hallazgos, limitaciones y enlace.
- [ ] Usar y cerrar los tres issues al terminar cada parte.
- [ ] Registrar participación de todos los integrantes mediante commits y pushes.
- [ ] Un solo integrante entrega los enlaces al dashboard y a assignment_3/, junto con grupo, dataset e integrantes.

La rúbrica suma 20 puntos: GitHub 3, visualización 6, mapas 5 y dashboard 6. El enunciado también contiene los rótulos contradictorios «19 puntos» y «Dashboard [5 pts]». Se incluyen en las listas de trabajo los requisitos adicionales de la rúbrica.
