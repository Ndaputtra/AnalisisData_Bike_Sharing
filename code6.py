import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Menyiapkan Dashboard
st.title("Dashboard Analisis Penyewaan Sepeda")
st.markdown("""
Selamat datang di dashboard interaktif ini. Kami akan menganalisis pola penyewaan sepeda berdasarkan beberapa faktor seperti cuaca, bulan, hari kerja, dan kategori pelanggan.
Data yang digunakan berasal dari dataset penyewaan sepeda di kota tertentu dalam rentang waktu dua tahun: 2011 dan 2012.
""")

# Step 1: Load Dataset dari file lokal
DATA_URL = "Data/day.csv"  # Sesuaikan path dataset
day_data = pd.read_csv(DATA_URL)

# Step 2: Data Wrangling
day_data['year'] = day_data['yr'].apply(lambda x: '2011' if x == 0 else '2012')
day_data['month'] = pd.to_datetime(day_data['dteday']).dt.month_name()
day_data['dteday'] = pd.to_datetime(day_data['dteday'])
day_data['Total'] = day_data['casual'] + day_data['registered']

# Sidebar untuk filter data
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", ['2011', '2012'], index=0)
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", day_data['weathersit'].unique())

# Filter berdasarkan input pengguna
filtered_data = day_data[(day_data['year'] == selected_year) & (day_data['weathersit'].isin(selected_weather))] if selected_weather else day_data[day_data['year'] == selected_year]

# Output keterangan jumlah data yang ditampilkan
st.write(f"Menampilkan data penyewaan sepeda untuk tahun **{selected_year}** dengan total data **{filtered_data.shape[0]}** observasi.")

# Step 3: Analisis Pengaruh Cuaca dan Bulan terhadap Permintaan Penyewaan Sepeda
st.header("Pengaruh Cuaca dan Bulan terhadap Permintaan Penyewaan Sepeda")
st.markdown("""
Pada bagian ini, Anda dapat melihat bagaimana faktor cuaca dan bulan memengaruhi jumlah penyewaan sepeda.
""")

# Memberikan label untuk kondisi cuaca
weather_labels = {1: "Cerah", 2: "Berawan/Mendung", 3: "Hujan/Salju Ringan", 4: "Hujan Deras/Saling Buruk"}
filtered_data['weathersit_label'] = filtered_data['weathersit'].map(weather_labels)

# Membuat palet warna yang menarik
palette = sns.color_palette("Set2")

# Membuat plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='month', y='cnt', hue='weathersit_label', data=filtered_data, palette=palette, ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_title('Pengaruh Cuaca dan Bulan terhadap Penyewaan Sepeda')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
st.pyplot(fig)
st.markdown("""
**Insight:** 
- Cuaca yang lebih baik, seperti cerah atau sedikit berawan, cenderung meningkatkan jumlah penyewaan sepeda. 
- Selain itu, permintaan bervariasi tergantung pada bulan; misalnya, bulan-bulan yang lebih hangat cenderung memiliki lebih banyak penyewaan.
""")

# Step 4: Perbandingan Pelanggan Harian vs Terdaftar
st.header("Perbandingan Pelanggan Harian vs Terdaftar")
st.markdown("""
Berikut adalah perbandingan antara jumlah pelanggan harian (casual) dengan pelanggan terdaftar (registered).
""")
labels = ['Pelanggan Harian', 'Pelanggan Terdaftar']
sizes = [filtered_data['casual'].sum(), filtered_data['registered'].sum()]

# Membuat plot
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(sizes, explode=(0.1, 0), labels=labels, autopct='%1.1f%%', shadow=True, startangle=140, colors=palette)
ax.axis('equal')
st.pyplot(fig)
st.markdown("""
**Insight:** Jumlah pelanggan terdaftar jauh lebih besar dibandingkan pelanggan harian, yang mengindikasikan bahwa banyak pengguna reguler yang menggunakan sepeda secara berulang sebagai moda transportasi.
""")

# Step 5: Pengaruh Hari Kerja dan Akhir Pekan terhadap Penyewaan
st.header("Pengaruh Hari Kerja dan Akhir Pekan terhadap Penyewaan Sepeda")
st.markdown("""
Apakah penyewaan sepeda lebih banyak terjadi pada hari kerja atau akhir pekan? Grafik berikut menunjukkan pengaruh hari kerja dan akhir pekan terhadap jumlah penyewaan sepeda.
""")

# Membuat plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weekday', y='cnt', hue='workingday', data=filtered_data, palette="coolwarm", ax=ax)
ax.set_title('Pengaruh Hari Kerja dan Akhir Pekan terhadap Penyewaan Sepeda')
ax.set_xlabel('Hari dalam Minggu')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.legend(title="Working Day", labels=["Akhir Pekan", "Hari Kerja"])
st.pyplot(fig)
st.markdown("""
**Insight:** Penyewaan sepeda cenderung lebih tinggi pada hari kerja, yang menunjukkan bahwa sepeda sering digunakan untuk keperluan transportasi sehari-hari, seperti pergi bekerja.
""")

# Step 6: Simpan Hasil
if st.button("Simpan Data yang Dibersihkan"):
    filtered_data.to_csv('bike_sharing_cleaned.csv', index=False)
    st.success("Data berhasil disimpan sebagai 'bike_sharing_cleaned.csv'")

# Step 7: Kesimpulan Akhir
st.header("Kesimpulan")
st.markdown("""
Berdasarkan analisis yang telah dilakukan, berikut adalah kesimpulan utama yang dapat diambil:
- **Cuaca**: Cuaca yang lebih baik mempengaruhi permintaan penyewaan sepeda secara positif. Bulan-bulan dengan cuaca lebih hangat cenderung memiliki permintaan yang lebih tinggi.
- **Pelanggan**: Pelanggan terdaftar mendominasi penyewaan sepeda, menunjukkan bahwa sepeda mungkin digunakan sebagai transportasi reguler oleh mereka.
- **Hari Kerja vs Akhir Pekan**: Lebih banyak penyewaan terjadi pada hari kerja, yang bisa menunjukkan bahwa sepeda lebih sering digunakan untuk bekerja daripada sekedar rekreasi.

Dashboard ini membantu Anda memahami pola penyewaan sepeda yang dipengaruhi oleh berbagai faktor. Terima kasih telah menggunakan dashboard ini untuk analisis data penyewaan sepeda!
""")
