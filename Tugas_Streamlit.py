import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title='Dashboard Operasional Layanan Kesehatan',
    page_icon="🏥",
    layout='wide'
)

df = pd.read_csv('clean_uber_dataset.csv')
st.write(df)