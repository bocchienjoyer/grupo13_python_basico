# Datos

Opción B: tabla final de lluvias y decretos de emergencia por departamento del assignment 2.

- `dataset.csv`: copia sin modificaciones de `assignment_2/datos/tabla_final.csv` (25 departamentos, 9 columnas).
- Leer con `pd.read_csv("datos/dataset.csv", dtype={"ubigeo": str})` para conservar los códigos de dos dígitos.
- Variables: ubigeo, departamento, declaratorias, prorrogas, capital, latitud, longitud, lluvia_total_mm y dias_lluvia_fuerte.
- Las lluvias corresponden a las capitales utilizadas en el assignment 2; no son promedios de todo el departamento.
- Añadir las geometrías oficiales para los mapas al desarrollar el issue de Mapas.
