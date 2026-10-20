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

st.title('Dashboard Operasional Layanan Kesehatan')
st.markdown("<h4 style='font-weight: bold; margin-bottom: 32px; margin-top: -16px'>Ringkasan Operasional Layanan Kesehatan </h3>", unsafe_allow_html=True)

st.divider()

filter1, filter2, filter3, filter4 = st.columns(4)
with filter1:
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    date_range = st.date_input(
        "Periode Waktu",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

with filter2:
    booking_status = st.multiselect(
        "Booking Status",
        sorted(df['Booking Status'].unique()),
        default=sorted(df['Booking Status'].unique())
    )

with filter3:
    vehicle = st.multiselect(
        "Jenis Kendaraan",
        sorted(df['Vehicle Type'].unique()),
        default=sorted(df['Vehicle Type'].unique())
    )

with filter4:
    paymemt = st.multiselect(
        "Metode Pembayaran",
        sorted(df['Payment Method'].unique()),
        default=sorted(df['Payment Method'].unique())
    )

st.divider()

df_filter = df[
    (df['Visit_Date'].dt.date >= min_date) &
    (df['Visit_Date'].dt.date <= max_date) &
    (df['Booking Status'].isin(booking_status)) &
    (df['City'].isin(vehicle)) &
    (df['Payment Method'].isin(paymemt))
].copy()

if df_filter.empty:
    st.warning("⚠️ Tidak ada data yang tersedia untuk kombinasi filter yang Anda pilih. Silakan sesuaikan kembali filter Anda di atas.")
    st.stop()

df_filter = df[
    (df['Visit_Date'].dt.date >= min_date) &
    (df['Visit_Date'].dt.date <= max_date) &
    (df['City'].isin(vehicle)) &
    (df['Payment Method'].isin(paymemt))
].copy()