# Responsable: Grupo13
# A3 – Parte 3: Dashboard (Issue #21)
#
# Dashboard de lluvias y declaratorias de emergencia por departamento.
# Datos: datos/dataset.csv (tabla final del Assignment 2)
# Mapa:  datos/departamentos_peru.geojson
#
# Correr en local, desde la carpeta assignment_3/:
#     uv run streamlit run app.py

import json
import unicodedata
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Lluvias y emergencias en el Perú",
    page_icon="🌧️",
    layout="wide",
)

# Rutas relativas a este archivo: funcionan igual en la laptop y en la nube
CARPETA = Path(__file__).parent
RUTA_DATOS = CARPETA / "datos" / "dataset.csv"
RUTA_GEOJSON = CARPETA / "datos" / "departamentos_peru.geojson"

FUENTE = "Fuente: tabla final del Assignment 2 (grupo 13) — decretos de emergencia y lluvia registrada en la capital de cada departamento."

# Nombre que ve el usuario -> columna del dataset
VARIABLES = {
    "Lluvia acumulada (mm)": "lluvia_total_mm",
    "Días de lluvia fuerte": "dias_lluvia_fuerte",
    "Declaratorias de emergencia": "declaratorias",
}


# ---------------------------------------------------------------------------
# Carga de datos (con caché para que la app no se recargue en cada clic)
# ---------------------------------------------------------------------------
def normalizar(texto: str) -> str:
    """'Áncash' -> 'ANCASH'. Sirve para emparejar nombres con el GeoJSON."""
    sin_tildes = unicodedata.normalize("NFKD", str(texto))
    sin_tildes = "".join(c for c in sin_tildes if not unicodedata.combining(c))
    return sin_tildes.upper().strip()


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    # ubigeo como TEXTO para conservar el cero a la izquierda ('01', no 1)
    df = pd.read_csv(RUTA_DATOS, dtype={"ubigeo": str}, encoding="utf-8-sig")
    df["ubigeo"] = df["ubigeo"].str.zfill(2)
    df["con_declaratoria"] = df["declaratorias"].gt(0).map(
        {True: "Con declaratoria", False: "Sin declaratoria"}
    )
    return df


@st.cache_data
def cargar_geojson(df: pd.DataFrame):
    """Agrega el ubigeo del dataset a cada departamento del GeoJSON.

    El GeoJSON solo trae el nombre en mayúsculas y sin tildes, así que se
    empareja por nombre normalizado y luego el mapa se cruza por ubigeo.
    Devuelve el GeoJSON y la lista de lo que no cruzó en cada lado.
    """
    with open(RUTA_GEOJSON, encoding="utf-8") as f:
        geo = json.load(f)

    nombre_a_ubigeo = dict(zip(df["departamento"].map(normalizar), df["ubigeo"]))

    sin_datos = []  # está en el GeoJSON pero no en el dataset
    for feature in geo["features"]:
        nombre = normalizar(feature["properties"]["departamento"])
        ubigeo = nombre_a_ubigeo.get(nombre)
        feature["id"] = ubigeo
        if ubigeo is None:
            sin_datos.append(feature["properties"]["departamento"])

    ubigeos_geo = {f["id"] for f in geo["features"]}
    sin_geometria = df.loc[~df["ubigeo"].isin(ubigeos_geo), "departamento"].tolist()
    return geo, sin_datos, sin_geometria


df = cargar_datos()
geo, sin_datos, sin_geometria = cargar_geojson(df)

# ---------------------------------------------------------------------------
# Barra lateral: filtros
# ---------------------------------------------------------------------------
st.sidebar.header("Filtros")

etiqueta = st.sidebar.selectbox(
    "Variable para el ranking y el mapa",
    list(VARIABLES.keys()),
)
variable = VARIABLES[etiqueta]

departamentos = st.sidebar.multiselect(
    "Departamentos",
    options=sorted(df["departamento"]),
    default=sorted(df["departamento"]),
)

lluvia_min, lluvia_max = float(df["lluvia_total_mm"].min()), float(df["lluvia_total_mm"].max())
rango_lluvia = st.sidebar.slider(
    "Lluvia acumulada (mm)",
    min_value=lluvia_min,
    max_value=lluvia_max,
    value=(lluvia_min, lluvia_max),
    step=10.0,
)

solo_emergencia = st.sidebar.checkbox("Solo departamentos con declaratoria")

st.sidebar.caption(FUENTE)

filtrado = df[
    df["departamento"].isin(departamentos)
    & df["lluvia_total_mm"].between(*rango_lluvia)
]
if solo_emergencia:
    filtrado = filtrado[filtrado["declaratorias"] > 0]

# ---------------------------------------------------------------------------
# Encabezado y métricas
# ---------------------------------------------------------------------------
st.title("🌧️ Lluvias y declaratorias de emergencia en el Perú")
st.markdown(
    "¿Los departamentos donde más llovió fueron los que recibieron declaratorias "
    "de emergencia? Usa los filtros de la izquierda para explorar."
)
st.caption(
    "Período: 1 de enero al 31 de mayo de 2022. "
    "La precipitación corresponde a las capitales departamentales, "
    "no al promedio de cada departamento."
)

if filtrado.empty:
    st.warning("Ningún departamento cumple los filtros. Amplía el rango o la selección.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Departamentos mostrados", f"0 de {len(df)}")
    c2.metric("Declaratorias de emergencia", "0")
    c3.metric("Lluvia promedio", "—")
    c4.metric("Días de lluvia fuerte (total)", "0")
    st.info("Los gráficos, el mapa y la tabla están vacíos porque el filtro no dejó resultados.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Departamentos mostrados", f"{len(filtrado)} de {len(df)}")
c2.metric("Declaratorias de emergencia", int(filtrado["declaratorias"].sum()))
c3.metric("Lluvia promedio", f"{filtrado['lluvia_total_mm'].mean():,.1f} mm")
c4.metric("Días de lluvia fuerte (total)", int(filtrado["dias_lluvia_fuerte"].sum()))

st.divider()


# ---------------------------------------------------------------------------
# Títulos-conclusión (cambian según lo que quede después de filtrar)
# ---------------------------------------------------------------------------
def titulo_ranking(datos: pd.DataFrame) -> str:
    maximo = datos[variable].max()
    if maximo == 0:
        return f"Ningún departamento seleccionado registra {etiqueta.lower()}"
    lideres = datos.loc[datos[variable] == maximo, "departamento"].tolist()
    valor = f"{maximo:,.1f}" if variable == "lluvia_total_mm" else f"{maximo:,.0f}"
    if len(lideres) == 1:
        return f"{lideres[0]} lidera en {etiqueta.lower()} con {valor}"
    return f"{', '.join(lideres)} empatan en {etiqueta.lower()} ({valor} cada uno)"


def titulo_dispersion(datos: pd.DataFrame) -> str:
    mas_lluvia = datos.loc[datos["lluvia_total_mm"].idxmax()]
    nombre, mm = mas_lluvia["departamento"], mas_lluvia["lluvia_total_mm"]
    if mas_lluvia["declaratorias"] == 0:
        return f"Más lluvia no implica emergencia: {nombre} ({mm:,.0f} mm) no tuvo declaratoria"
    return f"{nombre}, el más lluvioso ({mm:,.0f} mm), sí tuvo declaratoria"


# ---------------------------------------------------------------------------
# Pestañas: ranking, dispersión, mapa y tabla
# ---------------------------------------------------------------------------
tab_ranking, tab_dispersion, tab_mapa, tab_tabla = st.tabs(
    ["📊 Ranking", "🔍 Lluvia vs. emergencias", "🗺️ Mapa", "📋 Datos"]
)

with tab_ranking:
    ordenado = filtrado.sort_values(variable, ascending=True)  # el mayor queda arriba
    fig_barras = px.bar(
        ordenado,
        x=variable,
        y="departamento",
        orientation="h",
        color="con_declaratoria",
        color_discrete_map={"Con declaratoria": "#d62728", "Sin declaratoria": "#1f77b4"},
        text=variable,
        labels={variable: etiqueta, "departamento": "", "con_declaratoria": ""},
        title=titulo_ranking(filtrado),
        height=max(350, 28 * len(ordenado)),
    )
    formato_barras = "%{text:,.1f}" if variable == "lluvia_total_mm" else "%{text:,.0f}"
    fig_barras.update_traces(texttemplate=formato_barras, textposition="outside")
    fig_barras.update_layout(yaxis={"categoryorder": "total ascending"}, legend_title_text="")
    st.plotly_chart(fig_barras, width="stretch")
    st.caption(FUENTE)

with tab_dispersion:
    fig_disp = px.scatter(
        filtrado,
        x="lluvia_total_mm",
        y="dias_lluvia_fuerte",
        color="con_declaratoria",
        color_discrete_map={"Con declaratoria": "#d62728", "Sin declaratoria": "#1f77b4"},
        hover_name="departamento",
        hover_data={"capital": True, "declaratorias": True, "con_declaratoria": False},
        labels={
            "lluvia_total_mm": "Lluvia acumulada en la capital (mm)",
            "dias_lluvia_fuerte": "Días de lluvia fuerte",
            "con_declaratoria": "",
        },
        title=titulo_dispersion(filtrado),
        height=500,
    )
    fig_disp.update_traces(marker={"size": 12, "line": {"width": 1, "color": "white"}})
    st.plotly_chart(fig_disp, width="stretch")
    st.caption(FUENTE)

with tab_mapa:
    fig_mapa = px.choropleth_map(
        filtrado,
        geojson=geo,
        locations="ubigeo",  # cruce por ubigeo como texto
        color=variable,
        hover_name="departamento",
        hover_data={"ubigeo": True, "capital": True, variable: ":,.1f"},
        color_continuous_scale="Blues",
        labels={variable: etiqueta},
        map_style="carto-positron",
        center={"lat": -9.2, "lon": -75.0},
        zoom=4,
        opacity=0.8,
        title=f"{etiqueta} por departamento",
        height=650,
    )
    fig_mapa.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    st.plotly_chart(fig_mapa, width="stretch")
    st.caption(FUENTE + " Geometrías: datos/departamentos_peru.geojson.")

    with st.expander("Reporte del cruce dataset ↔ GeoJSON"):
        st.write(f"Departamentos en el dataset: **{len(df)}** · en el GeoJSON: **{len(geo['features'])}**")
        if not sin_datos and not sin_geometria:
            st.success("Las 25 geometrías tienen ubigeo y datos asociados.")
        if sin_geometria:
            st.warning(f"Sin geometría en el GeoJSON: {', '.join(sin_geometria)}")
        if sin_datos:
            st.warning(f"En el GeoJSON pero sin datos: {', '.join(sin_datos)}")

with tab_tabla:
    columnas = ["ubigeo", "departamento", "capital", "lluvia_total_mm",
                "dias_lluvia_fuerte", "declaratorias", "prorrogas"]
    st.dataframe(
        filtrado[columnas].sort_values(variable, ascending=False),
        hide_index=True,
        width="stretch",
        column_config={
            "ubigeo": "Ubigeo",
            "departamento": "Departamento",
            "capital": "Capital",
            "lluvia_total_mm": st.column_config.NumberColumn("Lluvia (mm)", format="%.1f"),
            "dias_lluvia_fuerte": "Días lluvia fuerte",
            "declaratorias": "Declaratorias",
            "prorrogas": "Prórrogas",
        },
    )
    st.download_button(
        "Descargar tabla filtrada (CSV)",
        filtrado[columnas].to_csv(index=False).encode("utf-8"),
        file_name="lluvias_emergencias_filtrado.csv",
        mime="text/csv",
    )
    st.caption(FUENTE)