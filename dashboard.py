import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "dteday": "tanggal",
        "casual": "pengguna_casual",
        "registered": "pengguna_terdaftar",
        "cnt": "jumlah_sewa"
    }, inplace=True)
    
    return daily_rentals_df

def create_workingday_rentals_df(df):
    # Mengelompokkan data berdasarkan workingday dan menghitung total sewa 
    workingday_rentals_df = df.groupby('workingday')['cnt'].mean().reset_index()
    
    # Mengganti nama kolom dalam bahasa Indonesia
    workingday_rentals_df.rename(columns={
        "workingday": "hari_kerja",
        "cnt": "jumlah_sewa"
    }, inplace=True)
    
    return workingday_rentals_df

def create_weather_rentals_df(df):
    # Mengelompokkan data berdasarkan weathersit dan menghitung total sewa 
    weather_rentals_df = df.groupby('weathersit')['cnt'].mean().reset_index()
    
    # Mengganti nama kolom dalam bahasa Indonesia
    weather_rentals_df.rename(columns={
        "weathersit": "cuaca",
        "cnt": "jumlah_sewa"
    }, inplace=True)
    
    return weather_rentals_df

def create_season_rentals_df(df):
    # Mengelompokkan data berdasarkan season dan menghitung total sewa 
    season_rentals_df = df.groupby('season')['cnt'].mean().reset_index()
    
    # Mengganti nama kolom dalam bahasa Indonesia
    season_rentals_df.rename(columns={
        "season": "musim",
        "cnt": "jumlah_sewa"
    }, inplace=True)
    
    return season_rentals_df


#mengakses dataframe
all_df = pd.read_csv("main_data.csv")

all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
#mengubah tipe data menjadi datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan gambar
    st.image("https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRm1yxLUz1TEEiu-0Xr1L6c-QNwh9pJ_tpqGnHn80f6UU4jxEMu")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))]
daily_rentals_df = create_daily_rentals_df(main_df)
workingday_rentals_df = create_workingday_rentals_df(main_df)
weather_rentals_df = create_weather_rentals_df(main_df)
season_rentals_df = create_season_rentals_df(main_df)


st.header('Bike Sharing :bike:')

st.subheader('Sewa Harian')

col1, col2, col3 = st.columns(3)

with col1:
    # Menggunakan create_daily_rentals_df 
    total_rented = daily_rentals_df.jumlah_sewa.sum()
    st.metric("Total sewa", value=total_rented)

with col2:
    # Menggunakan create_daily_rentals_df 
    total_member = daily_rentals_df.pengguna_terdaftar.sum()
    st.metric("Oleh Pengguna Terdaftar", value=total_member)

with col3:
    # Menggunakan create_daily_rentals_df 
    total_casual = daily_rentals_df.pengguna_casual.sum()
    st.metric("Oleh Pengguna Belum Terdaftar", value=total_casual)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rentals_df["tanggal"],
    daily_rentals_df["jumlah_sewa"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

    
st.title("Analisis Jumlah Sewa Sepeda")
st.subheader("Pengaruh Hari Kerja terhadap Jumlah Sewa")

colors = ["#D3D3D3", "#72BCD4"]
# Visualisasi untuk Hari Kerja
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='hari_kerja', y='jumlah_sewa', data=workingday_rentals_df, palette=colors,errorbar=None)
ax.set_title('Jumlah Sewa Sepeda Berdasarkan Hari Kerja')
ax.set_xlabel(None)
plt.xticks(ticks=[0, 1], labels=['Hari Libur', 'Hari Kerja'])
ax.set_ylabel('Rata-Rata Jumlah Sewa Sepeda')
plt.legend(title='Keterangan', loc='upper right', bbox_to_anchor=(1.47, 1), labels=['Hari Libur (Sabtu, Minggu, dan Hari Besar)', 'Hari Kerja (Senin-Jumat)'])
st.pyplot(fig)

st.subheader("Pengaruh Cuaca terhadap Jumlah Sewa")

colors2 = ["#72BCD4", "#D3D3D3","#D3D3D3","#D3D3D3"]
# Visualisasi untuk Cuaca
fig_weather, ax_weather = plt.subplots(figsize=(8, 6))
sns.barplot(x='cuaca', y='jumlah_sewa', data=weather_rentals_df, palette=colors2, ax=ax_weather)
ax_weather.set_title('Jumlah Sewa Sepeda Berdasarkan Cuaca')
plt.xticks(ticks=[0,1,2,3], labels=['Cerah', 'Berawan', 'Hujan/Salju Ringan', 'Hujan Lebat/Guntur'])
ax_weather.set_ylabel('Jumlah Sewa Sepeda')
ax_weather.set_xlabel(None)
st.pyplot(fig_weather)

st.subheader("Pengaruh Musim terhadap Jumlah Sewa")
# Visualisasi untuk Musim
fig_season, ax_season = plt.subplots(figsize=(8, 6))
sns.barplot(x='musim', y='jumlah_sewa', data=season_rentals_df, palette='pastel', ax=ax_season, errorbar=None)
ax_season.set_title('Jumlah Sewa Sepeda Berdasarkan Musim')
plt.xticks(ticks=[0,1,2,3], labels=['Semi', 'Panas', 'Gugur', 'Salju'])
ax_season.set_ylabel('Jumlah Sewa Sepeda')
ax_season.set_xlabel(None)
st.pyplot(fig_season)



