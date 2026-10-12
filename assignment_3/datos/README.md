# Datos

Opción B: tabla final de lluvias y decretos de emergencia por departamento del assignment 2.

- `dataset.csv`: copia sin modificaciones de `assignment_2/datos/tabla_final.csv` (25 departamentos, 9 columnas).
- Leer con `pd.read_csv("datos/dataset.csv", dtype={"ubigeo": str})` para conservar los códigos de dos dígitos.
- Variables: ubigeo, departamento, declaratorias, prorrogas, capital, latitud, longitud, lluvia_total_mm y dias_lluvia_fuerte.
- Las lluvias corresponden a las capitales utilizadas en el assignment 2; no son promedios de todo el departamento.
- `departamentos_peru.geojson`: geometrías oficiales de los 25 departamentos, copia sin modificaciones de `data/07-mapas/departamentos_peru.geojson` del repositorio del curso (se descarga con `uv run python scripts/fetch_data.py 07-mapas`).
- Columnas del GeoJSON: `departamento` (en mayúsculas y sin tildes, por ejemplo `ANCASH`) y `geometry`, en EPSG:4326. No trae ubigeo: `mapas.ipynb` se lo asigna a partir del nombre y luego cruza con `dataset.csv` por ubigeo.
