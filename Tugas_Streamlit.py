import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title='Dashboard Operasional Layanan Kesehatan',
    page_icon="🏥",
    layout='wide'
)

@st.cache_data
def load_data():
    df = pd.read_csv('clean_uber_dataset.csv')
    return df

df = load_data()
st.write(df)

st.title('Dashboard Operasional Layanan Kesehatan')
st.markdown("<h4 style='font-weight: bold; margin-bottom: 32px; margin-top: -16px'>Ringkasan Operasional Layanan Kesehatan </h3>", unsafe_allow_html=True)

st.divider()