import pandas as pd
import streamlit as st
import plotly.express as px
import json

st.set_page_config(
    page_title='Dashboard Analisis Performa Uber',
    page_icon="🏥",
    layout='wide'
)

@st.cache_data
def load_data():
    df = pd.read_csv('clean_uber_dataset.csv', parse_dates=['Date'])
    return df

df = load_data()

st.title('Dashboard Analisis Performa Uber di India Tahun 2024')
st.markdown("<h4 style='font-weight: bold; margin-bottom: 32px; margin-top: -16px'>Ringkasan Analisis Performa Uber di India Tahun 2024</h3>", unsafe_allow_html=True)

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
    (df['Date'].dt.date >= min_date) &
    (df['Date'].dt.date <= max_date) &
    (df['Booking Status'].isin(booking_status)) &
    (df['Vehicle Type'].isin(vehicle)) &
    (df['Payment Method'].isin(paymemt))
].copy()

if df_filter.empty:
    st.warning("⚠️ Tidak ada data yang tersedia untuk kombinasi filter yang Anda pilih. Silakan sesuaikan kembali filter Anda di atas.")
    st.stop()

df_filter_percentage = df[
    (df['Date'].dt.date >= min_date) &
    (df['Date'].dt.date <= max_date) &
    (df['Vehicle Type'].isin(vehicle)) &
    (df['Payment Method'].isin(paymemt))
].copy()

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
total_transaksi= int(df_filter['Booking ID'].count())
avg_booking = round(float(df_filter['Booking Value'].mean()), 2)
avg_vtat = int(df_filter['Avg VTAT'].mean())
avg_ctat = int(df_filter['Avg CTAT'].mean())
avg_rating = round(float(df_filter['Driver Ratings'].mean()), 2)

batal_keywords = 'No Driver Found|Incomplete|Cancel'
kondisi_batal = df_filter_percentage['Booking Status'].str.contains(batal_keywords, case=False, na=False)
jumlah_batal = int(df_filter_percentage[kondisi_batal]['Booking ID'].count())
jumlah_kunjungan_tanpa_status = int(df_filter_percentage['Booking ID'].count())
if jumlah_kunjungan_tanpa_status > 0:
    percentage_batal = round((jumlah_batal / jumlah_kunjungan_tanpa_status) * 100, 2)
else:
    percentage_batal = 0.0

kpi1.metric(label="Total Transaksi", value=f'**{total_transaksi:,}**'.replace(".", ","))
kpi2.metric(label='Average Booking Value', value=f'₹ **{avg_booking:,}**'.replace(".", "."))
kpi3.metric(label='Persentase Perjalanan Incomplete', value=f'**{percentage_batal}%**')
kpi4.metric(label='Average Waktu Tunggu', value=f'**{avg_vtat:,} Min**')
kpi5.metric(label='Average Durasi Perjalanan', value=f'**{avg_ctat} Min**')
kpi6.metric(label='Average Driver Rating', value=f'**{avg_rating}**/5')

# tab1, tab2 = st.tabs(2)
# with

monthly = (
    df_filter.assign(Bulan=df_filter['Date'].dt.to_period('M').astype(str))
    .groupby('Bulan', as_index=False)['Booking ID'].count()
)
viz = px.line(
    monthly, 
    x='Bulan',
    y='Booking ID',
    title='Total Transaksi',
    markers=True
)
viz.update_layout(yaxis_title='Total Transaksi', xaxis_title='')
st.plotly_chart(viz, use_container_width=True)

left1, right1 = st.columns(2)
with left1:
    vehicle_type = (
        df_filter.groupby('Vehicle Type', as_index=False)['Booking ID']
        .count().sort_values('Booking ID', ascending=False)
    )
    viz = px.bar(
        vehicle_type,
        x='Vehicle Type',
        y='Booking ID',
        title='Top 5 Jenis Kendaraan yang Paling Sering di Booking',
        text_auto='.2s'
    )
    viz.update_layout(xaxis_title='Jenis Kendaraan', yaxis_title='Rata-rata Waktu Tunggu Terlama')
    st.plotly_chart(viz, use_container_width=True)

with right1:
    data = df_filter.copy()
    data = data[data['Payment Method'] != 'Unknown']
    payment_pie = (
        data.groupby('Payment Method', as_index=False)['Booking ID']
        .count().sort_values('Booking ID', ascending=True)
    )
    viz = px.pie(
        payment_pie,
        names='Payment Method',
        values='Booking ID',
        title='Jumlah Transaksi Berdasarkan Metode Pembayaran',
        hole=0.5
    )
    st.plotly_chart(viz, use_container_width=True)

left2, right2 = st.columns(2)
with left2:
    rute_bar = (
        df_filter.groupby('Rute', as_index=False)['Booking ID']
        .count().sort_values('Booking ID', ascending=True).tail()
    )
    viz = px.bar(
        rute_bar,
        x='Booking ID',
        y='Rute',
        orientation='h',
        title='Top 5 Rute yang Paling Sering di Booking',
        text_auto='.2s'
    )
    viz.update_layout(xaxis_title='Jumlah', yaxis_title='Rute')
    st.plotly_chart(viz, use_container_width=True)

with right2:
    status_pie = (
        df_filter.groupby('Booking Status', as_index=False)['Booking ID']
        .count().sort_values('Booking ID', ascending=True)
    )
    viz = px.pie(
        status_pie,
        names='Booking Status',
        values='Booking ID',
        title='Jumlah Transaksi Berdasarkan Booking Status',
        hole=0.5
    )
    st.plotly_chart(viz, use_container_width=True)

left3, right3 = st.columns(2)
with left3:
    pickup_bar = (
        df_filter.groupby('Pickup Location', as_index=False)['Booking ID']
        .count().sort_values('Booking ID', ascending=False).head()
    )
    viz = px.bar(
        pickup_bar,
        x='Pickup Location',
        y='Booking ID',
        title='Top 5 Pickup Location yang Paling Sering di Booking',
        text_auto='.2s'
    )
    viz.update_layout(xaxis_title='Wilayah', yaxis_title='Jumlah Booking')
    st.plotly_chart(viz, use_container_width=True)

with right3:
    drop_bar = (
        df_filter.groupby('Drop Location', as_index=False)['Booking ID']
        .count().sort_values('Booking ID', ascending=False).head()
    )
    viz = px.bar(
        drop_bar,
        x='Drop Location',
        y='Booking ID',
        title='Top 5 Drop Location yang Paling Sering di Booking',
        text_auto='.2s'
    )
    viz.update_layout(xaxis_title='Wilayah', yaxis_title='Jumlah Booking')
    st.plotly_chart(viz, use_container_width=True)

left4, right4 = st.columns(2)
with left4:
    data = df_filter.copy()
    data = data[data['Reason for cancelling by Customer'] != 'Unknown']
    alasan_cust = (
        data.groupby('Reason for cancelling by Customer', as_index=False)['Booking ID']
        .count().sort_values('Booking ID', ascending=True)
    )
    viz = px.bar(
        alasan_cust,
        x='Booking ID',
        y='Reason for cancelling by Customer',
        orientation='h',
        title='Top 5 Alasan Cancel by Customer',
        text_auto='.2s'
    )
    viz.update_layout(xaxis_title='Jumlah', yaxis_title='Alasan')
    st.plotly_chart(viz, use_container_width=True)

with right4:
    data = df_filter.copy()
    data = data[data['Driver Cancellation Reason'] != 'Unknown']
    alasan_driv = (
        data.groupby('Driver Cancellation Reason', as_index=False)['Booking ID']
        .count().sort_values('Booking ID', ascending=True)
    )
    viz = px.bar(
        alasan_driv,
        x='Booking ID',
        y='Driver Cancellation Reason',
        orientation='h',
        title='Top 5 Alasan Cancel by Driver',
        text_auto='.2s'
    )
    viz.update_layout(xaxis_title='Jumlah', yaxis_title='Alasan')
    st.plotly_chart(viz, use_container_width=True)

st.divider()
row = st.container(horizontal=True, horizontal_alignment="right")
row.subheader("Detail Dataset Uber India Tahun 2024")
csv = df_filter.to_csv(index=False).encode('utf-8')
row.download_button(
    label="Download Dataset",
    data=csv,
    mime="text/csv",
    file_name="Dataset_Operasional.csv"
)
st.write(df)