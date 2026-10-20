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