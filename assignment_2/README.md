# **Temporada asignada**

### **Grupo 13**: 1 de enero al 31 de mayo de 2022

## **Requisitos para ejecutar los notebooks en otro ordenador**

Ejecutar desde la carpeta `assignment_2/`. Se necesita Python 3.10+ y Jupyter (`pip install notebook` o VS Code con extensión de Python).

Librerías de terceros usadas en los tres `ipynb` (`api_lluvias.ipynb`, `scraping_emergencias.ipynb`, `cruce_analisis.ipynb`):

| Librería | Se usa para |
|---|---|
| `pandas` | Tablas y CSV en los 3 notebooks (`read_html`, `read_csv`, `merge`, `groupby`) |
| `requests` | Descargar Wikipedia y APIs de Open-Meteo (`api_lluvias`), y fichas de gob.pe (`scraping_emergencias`) |
| `plotly` | Los 2 gráficos de `cruce_analisis` (`plotly.express`) |
| `selenium` | Scraping del buscador de gob.pe (`scraping_emergencias`) |
| `beautifulsoup4` | Extraer el título completo de cada norma (`scraping_emergencias`) |
| `lxml` | Requerida por `pd.read_html` para leer las tablas de Wikipedia (`api_lluvias`) |

Instalación en un solo comando:

```
pip install pandas requests plotly selenium beautifulsoup4 lxml jupyter
```

El resto de imports (`io`, `re`, `time`, `datetime`, `pathlib`, `unicodedata`, `os`) son librería estándar de Python, no se instalan.

Nota para `scraping_emergencias.ipynb`: además se necesita el navegador Chrome (o Edge con `SCRAPING_BROWSER=edge`) con su driver compatible, ya que Selenium abre el buscador de gob.pe.
