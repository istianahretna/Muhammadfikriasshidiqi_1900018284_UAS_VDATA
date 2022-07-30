import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
# Streamlit page configuration 
st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

st.title(":traffic_light: Penindakan Pelanggaran Lalu Lintas dan Angkutan")


df = pd.read_excel(
    io="data_penindakan_pelanggaran_lalu_lintas_dan_angkutan_jalan_tahun_2021.xlsx",
    engine="openpyxl",
   sheet_name="Sheet1",
    usecols="A:J",
    nrows=43,
)

st.sidebar.header("Silahkan Filter Data Disini :")
# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
wilayah = st.sidebar.multiselect(
    "Select the wilayah:",
    options=df["wilayah"].unique(),
    default=df["wilayah"].unique()
)

bap_tilang = st.sidebar.multiselect(
    "Select the bap_tilang:",
    options=df["bap_tilang"].unique(),
    default=df["bap_tilang"].unique(),
)

stop_operasi = st.sidebar.multiselect(
    "Select the stop_operasi:",
    options=df["stop_operasi"].unique(),
    default=df["stop_operasi"].unique()
)

df_selection = df.query(
    "wilayah == @wilayah & bap_tilang ==@bap_tilang & stop_operasi == @stop_operasi"
)


Bulan = st.sidebar.multiselect(
    "Filter Bulan:",
    options=df["bulan"].unique(),
    default=df["bulan"].unique(),
)

df_selection = df.query(
    " bulan ==@Bulan "
)


st.dataframe(df_selection) # view dataframe on page
pie_chart = px.pie(df,
                    title="<b>BAP Tilang Terhadap Wilayah</b>",
                    values= 'bap_tilang',
                    names= 'wilayah')

st.plotly_chart(pie_chart)

data_penindakan_pelanggaran_lalu_lintas = (
    df_selection.groupby(by=["wilayah"]).sum()[["bap_tilang"]].sort_values(by="bap_tilang")
)
fig_pelanggaran_lalu_lintas = px.bar(
    data_penindakan_pelanggaran_lalu_lintas,
    x="bap_tilang",
    y=data_penindakan_pelanggaran_lalu_lintas.index,
    orientation="h",
    title="<b>BAP Tilang Berdasarkan Wilayah</b>",
    color_discrete_sequence=["#0083B8"] * len(data_penindakan_pelanggaran_lalu_lintas),
    template="plotly_white",
)
fig_pelanggaran_lalu_lintas.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_pelanggaran_lalu_lintas, use_container_width=True)