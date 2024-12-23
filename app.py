import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Judul Aplikasi
st.title("Aplikasi Visualisasi Data Stunting")

# Unggah File CSV
uploaded_file = st.file_uploader("Pilih file CSV", type=["csv"])

if uploaded_file is not None:
    # Membaca data dari file yang diunggah
    data = pd.read_csv(uploaded_file)

    # Tampilkan data secara tabel
    st.write("Tabel Data:")
    st.write(data)

    # Langkah 1: Normalisasi Nama Kecamatan (Jika Ada Kesalahan Penulisan)
    data['KECAMATAN'] = data['KECAMATAN'].str.strip()  # Hilangkan spasi di depan/belakang jika ada
    # st.write("Data Setelah Normalisasi:")
    # st.write(data)

    # Langkah 2: Mengelompokkan Data Berdasarkan Kecamatan
    # Misalnya, menghitung jumlah data per kecamatan (agregasi) 
    data_grouped = data.groupby('KECAMATAN').size().reset_index(name='jumlah')

    # Tampilkan Data Setelah Dikelompokkan
    st.write("Data yang Dikelompokkan Berdasarkan Kecamatan:")
    st.write(data_grouped)

    # Pilih kolom untuk visualisasi
    columns = ["Pilih Kolom"]+ data.columns.tolist()
    selected_x = st.selectbox("Pilih kolom X untuk plot", columns)
    selected_y = st.selectbox("Pilih kolom Y untuk plot", columns)

    # Periksa apakah pengguna telah memilih kolom yang valid
    if selected_x == "Pilih Kolom" or selected_y == "Pilih Kolom":
        st.warning("Silakan pilih kolom X dan Y yang valid untuk melanjutkan.")
    
    else:
     # Tangani Kasus Error dengan Try-Except
        try:
            # Periksa apakah kolom X dan Y sama
            if selected_x == selected_y:
                st.warning("Kolom X dan Y tidak boleh sama. Silakan pilih kolom yang berbeda untuk X dan Y.")
            else:
                data_agg = data.groupby([selected_x])[selected_y].sum().reset_index()
                st.table(data_agg)
                st.write(f"Plot Pie antara {selected_x} dan {selected_y}")
                fig, ax = plt.subplots()

                # Pastikan data Y adalah numerik dan tidak memiliki nilai negatif
                if data[selected_y].dtype == 'object':
                    raise ValueError("Kolom Y harus berupa numerik untuk visualisasi ini.")

                # Pastikan semua nilai di kolom Y adalah non-negatif
                if (data[selected_y] < 0).any():
                    raise ValueError("Kolom Y harus memiliki nilai non-negatif.")
                
                
                
                # Visualisasi Pie Chart
                ax.pie(data_agg[selected_y], labels=data_agg[selected_x], autopct='%1.1f%%', startangle=90)
                ax.axis('equal')    # Pastikan pie chart berbentuk lingkaran
                # Tampilkan visualisasi
                st.pyplot(fig)

                # Plot bar
                st.write("Barplot Kolom Terpilih Terhadap Kasus Stunting")
                fig, ax = plt.subplots(figsize=(10,6))
                ax.bar(data_agg[selected_x], data_agg[selected_y], color='red',
                    alpha=0.25)
                ax.grid()
                st.pyplot(fig)

        except ValueError as e:
            # Tampilkan pesan peringatan yang jelas ke pengguna
            st.warning(f"Terjadi kesalahan: {str(e)}")
        except Exception as e:
            # Tampilkan peringatan untuk kesalahan lain yang tidak terduga
            st.warning(f"Kesalahan tak terduga: {str(e)}")
    
     # Pilihan Kecamatan
    kecamatan_terpilih = st.selectbox("Pilih Kecamatan:", ["Pilih Kolom"]+ data['KECAMATAN'].unique().tolist())
    
    if kecamatan_terpilih == "Pilih Kolom":
        st.warning("Silakan pilih kolom untuk melanjutkan.")
    
    else:

          # Filter data berdasarkan kecamatan yang dipilih
        data_filtered = data[data['KECAMATAN'] == kecamatan_terpilih]

  
        # Pilihan Kolom X (misalnya Desa/Kelurahan)
        kolom_x = 'Desa_Kelurahan'  # Misalnya, nama kolom desa atau kelurahan
        # Tampilkan data dalam bentuk tabel
        st.write("Data Kasus Stunting per Desa/Kelurahan")
        st.table(data_filtered[[kolom_x, 'Stunting1805']])
        st.write("Barplot Kolom Terpilih Terhadap Kasus Stunting")
        fig, ax = plt.subplots(figsize=(10,6))
        ax.barh(data_filtered[kolom_x], data_filtered['Stunting1805'], color='red',
            alpha=0.25)
        ax.grid()
        st.pyplot(fig)

     # Pilihan Variabel Y
        # Daftar variabel Y yang tersedia, di mana masing-masing variabel memiliki 3 kolom terkait
        opsi_y = {
            'BPJS/JKN': ['JKN_BPJS_Ya', 'JKN_BPJS_Tidak', 'JKN_BPJS_Belum_ada_data'],
            'Air Bersih': ['AirBersih_Ya', 'AirBersih_Tidak', 'AirBersih_Belum_ada_data'],
            'Kecacingan': ['Kecacingan_Ya', 'Kecacingan_Tidak', 'Kecacingan_Belum_ada_data'],
            'Jamban Sehat': ['JambanSehat_Ya', 'JambanSehat_Tidak', 'JambanSehat_Belum_ada_data'],
            'Imunisasi': ['Imunisasi_Ya', 'Imunisasi_Tidak', 'Imunisasi_Belum_ada_data'],
            'Merokok (Keluarga)': ['MerokokKeluarga_Ya', 'MerokokKeluarga_Tidak', 'MerokokKeluarga_Belum_ada_data'],
            'Riwayat Ibu Hamil': ['RiwayatIbuHamil_Ya', 'RiwayatIbuHamil_Tidak', 'RiwayatIbuHamil_Belum_ada_data'],
            'Penyakit Penyerta': ['PenyakitPenyerta_Ya', 'PenyakitPenyerta_Tidak', 'PenyakitPenyerta_Belum_ada_data']
        }

        # Memilih variabel Y
        variabel_y = st.selectbox("Pilih Variabel Y:", ["Pilih Kolom"]+ list(opsi_y.keys()))
        
        if variabel_y == "Pilih Kolom":
            st.warning("Silakan pilih variabel untuk melanjutkan.")
        
        else:
    
            # Mendapatkan kolom Y yang sesuai (ada 3 kolom untuk setiap variabel Y)
            kolom_y = opsi_y[variabel_y]

            # Tampilkan data filtered
            st.write(f"Data Kecamatan {kecamatan_terpilih}:")
            st.write(data_filtered[[kolom_x] + kolom_y])

            # Langkah 4: Visualisasi Bar Chart Horizontal
            st.write(f"Visualisasi {variabel_y} Berdasarkan Desa/Kelurahan di Kecamatan {kecamatan_terpilih}:")

            fig, ax = plt.subplots()
            # Membuat bar horizontal untuk setiap kolom Y (ya, tidak, belum ada data)
            ax.barh(data_filtered[kolom_x], data_filtered[kolom_y[0]], color='green', label=f'{variabel_y} Ya', height=0.4)
            ax.barh(data_filtered[kolom_x], data_filtered[kolom_y[1]], left=data_filtered[kolom_y[0]], color='red', label=f'{variabel_y} Tidak', height=0.4)
            ax.barh(data_filtered[kolom_x], data_filtered[kolom_y[2]], left=data_filtered[kolom_y[0]] + data_filtered[kolom_y[1]], color='gray', label=f'{variabel_y} Belum Ada Data', height=0.4)

            ax.set_xlabel('Jumlah')
            ax.set_title(f'Jumlah {variabel_y} di Kecamatan {kecamatan_terpilih} Berdasarkan Desa/Kelurahan')
            ax.legend()

            # Menampilkan visualisasi
            st.pyplot(fig)
