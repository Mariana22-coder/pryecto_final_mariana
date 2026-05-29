
import streamlit as st
import pandas as pd

ruta_datos = "data/processed/entregas_limpio.csv"
df = pd.read_csv(ruta_datos)

import streamlit as st
import pandas as pd
import plotly.express as px

ruta_datos = "data/processed/entregas_limpio.csv"


@st.cache_data
def cargar_datos():
    return pd.read_csv(ruta_datos)


df = cargar_datos()

# 1. Sidebar

st.sidebar.title("filtros base para Facu")
st.sidebar.markdown("Modifica el campo pais para ver la operacion por pais")


# 2. Filtros (st.slider) de Country

min_Importe = float(df['Importe'].min())
max_Importe = float(df['Importe'].max())

# slider
rango_Importe = st.sidebar.slider(
    label="Selecciona el rango de COMISION:",
    min_value=min_Importe,
    max_value=max_Importe,
    value=(min_Importe, max_Importe))

df_filtrado = df[(df['Importe'] >= rango_Importe[0]) & (df['Importe'] <= rango_Importe[1])]


# ==========================================================
# VER ACA PORQUE ME QUEDA RARO
# ==========================================================
st.sidebar.markdown("# Panel de Control ")
st.sidebar.markdown("Modifica el rango de importes para actualizar los análisis y gráficos.")

# Filtro de rango basado en 'importe'
columna_filtro = "Importe"
min_val = float(df["Importe"].min())
max_val = float(df["Importe"].max())

rango_seleccionado = st.sidebar.slider(
    f"Filtrar por Rango de {"COMISION"}:",
    min_value=min_val,
    max_value=max_val,
    value=(min_val, max_val)
)

df_filtrado = df[
    (df["Importe"] >= rango_seleccionado[0]) &
    (df["Importe"] <= rango_seleccionado[1])
    ]

# 3. RESUMEN

st.markdown("<h1 style='color: #00FF00; font-weight: bold;'>FASE 2 ENTREGA PROYECTO</h1>", unsafe_allow_html=True)

st.markdown("### Resumen")
st.write(f"Mostrando *{len(df_filtrado)}* de *{len(df)}* registros totales.")

if not df_filtrado.empty:
    columnas_analisis = ["Importe", "Impuestos"]

    tab1, tab2 , tab3 = st.tabs([" Estadísticas de Importe", " Estadísticas de impuestos", "Detalle por pais"])

    with tab1:
        col_actual = "Importe"
        media = df_filtrado[col_actual].mean()
        mediana = df_filtrado[col_actual].median()
        v_min = df_filtrado[col_actual].min()
        v_max = df_filtrado[col_actual].max()
        rango_valores = v_max - v_min
        desviacion = df_filtrado[col_actual].std()
        q25 = df_filtrado[col_actual].quantile(0.25)
        q75 = df_filtrado[col_actual].quantile(0.75)

        c1, c2, c3 = st.columns(3)
        c1.metric("Media (Promedio)", f"${media:.2f}")
        c1.metric("Mediana (Q2)", f"${mediana:.2f}")
        c2.metric("Desviación Estándar", f"${desviacion:.2f}")
        c2.metric("Rango (Máx - Mín)", f"${rango_valores:.2f}")
        c3.markdown("*Cuartiles:*")
        c3.markdown(f"* *25% (Q1):* ${q25:.2f}\n* *50% (Q2):* ${mediana:.2f}\n* *75% (Q3):* ${q75:.2f}")

    with tab2:
        col_actual = "Impuestos"
        if col_actual in df_filtrado.columns:
            media = df_filtrado[col_actual].mean()
            mediana = df_filtrado[col_actual].median()
            v_min = df_filtrado[col_actual].min()
            v_max = df_filtrado[col_actual].max()
            rango_valores = v_max - v_min
            desviacion = df_filtrado[col_actual].std()
            q25 = df_filtrado[col_actual].quantile(0.25)
            q75 = df_filtrado[col_actual].quantile(0.75)

            c1, c2, c3 = st.columns(3)
            c1.metric("Media (Promedio)", f"${media:.2f}")
            c1.metric("Mediana (Q2)", f"${mediana:.2f}")
            c2.metric("Desviación Estándar", f"${desviacion:.2f}")
            c2.metric("Rango (Máx - Mín)", f"${rango_valores:.2f}")
            c3.markdown("*Cuartiles:*")
            c3.markdown(f"* *25% (Q1):* ${q25:.2f}\n* *50% (Q2):* ${mediana:.2f}\n* *75% (Q3):* ${q75:.2f}")


    with tab3:
        st.subheader(" Análisis por País")

        lista_paises = df_filtrado['country'].unique()
        pais_seleccionado = st.selectbox("Selecciona un país para ver sus registros:", lista_paises)


        df_pais = df_filtrado[df_filtrado['country'] == pais_seleccionado]

        st.dataframe(df_pais, use_container_width=True)


    # 4. GRÁFICOS
    st.markdown("---")
    st.markdown("<h1 style='color: #FF4B4B; font-weight: bold;'>VISTA GRAFICOS</h1>", unsafe_allow_html=True)

    # Gráfico 1: Relación entre Importe y Comisión por País
    st.subheader("Relación Importe vs Impuestos por País (country)")
    # Agrupamos para calcular los totales de dinero por país
    df_pais_dinero = df_filtrado.groupby("country")[["Importe", "Impuestos"]].sum().reset_index()

    fig1 = px.bar(
        df_pais_dinero,
        x="country",
        y=["Importe", "Impuestos"],
        title="Comparativa de Importes Generados y Impuestos Cobradas por País",
        barmode="group",
        labels={"value": "Importe ($)", "country": "País", "variable": "Concepto"},
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Estado por Adquirente x la Comisión
    st.subheader("Estado de Transacción (status) y Impuestos por Adquirente (acquirer)")
    df_acq_status = df_filtrado.groupby(["acquirer", "status"]).agg(
        Total_Impuestos=("Impuestos", "sum"),
        Cantidad=("Importe", "count")
    ).reset_index()

    fig2 = px.bar(
        df_acq_status,
        x="acquirer",
        y="Total_Impuestos",
        color="status",
        barmode="stack",
        title="Monto Acumulado de impuestos por Adquirente Segmentado por Estado",
        labels={"acquirer": "Adquirente", "Total_Impuestos": "Impuestos Total ($)", "status": "Estado"},
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("que tal profe?")

    if st.button ("ok"):
        st.write ("gracias profe")
    if st.button ("no okei"):
        st.write ("aahh mejoraar")

