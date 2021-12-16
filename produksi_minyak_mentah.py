#################################################### IMPORT MODUL ####################################################
import numpy as np
import streamlit as st
import pandas as pd
import json 
import matplotlib.pyplot as plt
from matplotlib import cm
#################################################### IMPORTT MODUL ####################################################


#PANGGIL FILE
df = pd.read_csv("produksi_minyak_mentah.csv")


#################################################### TITLE ####################################################
st.set_page_config(layout="wide")       #this needs to be the first Streamlit command called
st.title("Statistik Produksi Jumlah Minyak Mentah Dunia")
#################################################### TITLE ####################################################


#OPEN JSON
with open("Downloads/kode_negara_lengkap.json") as f:
    data = json.load(f)

#MENGGANTI KODE NEGARA DENGAN NAMA NEGARA LENGKAP
konversi = {item['alpha-3'] : item['name'] for item in data}
df.loc[:, 'kode_negara'] = df['kode_negara'].map(konversi)

#MENGHILANGKAN DATA NaN
df.dropna(subset=["kode_negara"], inplace=True)


#################################################### SIDEBAR ####################################################
st.sidebar.title("Pengaturan")
st.sidebar.subheader("Pengaturan konfigurasi tampilan")

#USER INPUT ON CONTROL PANEL
#PILIH TAMPILAN
menu = st.sidebar.radio("",("General Info","Statistik"),)

#PILIH NEGARA
list_negara_unik = []
for negara_unik in df["kode_negara"].unique():
    list_negara_unik.append(negara_unik)
pilih_negara = st.sidebar.selectbox("Pilih negara", list_negara_unik)

#PILIH TAHUN
list_tahun = list()
for range_tahun in range(1971, 2016):
    list_tahun.append(range_tahun)
pilih_tahun = st.sidebar.selectbox("Tahun yang ingin ditampilkan", list_tahun)

#PILIHAN JUMLAH TAMPILAN DATA
n_tampil = st.sidebar.number_input("Jumlah negara pemroduksi minyak terbesar yang ingin ditampilkan", min_value=1, max_value=len(list_negara_unik), value=10)

#INFORMASI PRIBADI
st.sidebar.markdown('---')
st.sidebar.write('Muhammad Helmy Nabawi 12220054 | December 2021 helmynabawi@gmail.com')
#################################################### SIDEBAR ####################################################

#MEMBUAT DATAFRAME LENGKAP
sub_region = {item['name'] : item['sub-region'] for item in data}
region = {item['name'] : item['region'] for item in data}
alpha3 = {item['name'] : item['alpha-3'] for item in data}

list_sub_region = []
list_region = []
list_alpha3 = []

for name in df['kode_negara'] :
    for keys,values in sub_region.items():
        if name == keys :
            list_sub_region.append(values)
        else :
            continue

for name in df['kode_negara'] :
    for keys,values in region.items():
        if name == keys :
            list_region.append(values)
        else :
            continue

for name in df['kode_negara'] :
    for keys,values in alpha3.items():
        if name == keys :
            list_alpha3.append(values)
        else :
            continue
dict_df_lengkap = {'nama negara': df['kode_negara'], 'kode negara' : list_alpha3, 'region': list_region, 'subregion' : list_sub_region, 'tahun':df['tahun'], 'produksi': df['produksi']}
df_lengkap_frame = pd.DataFrame(dict_df_lengkap) 


#################################################### MENU GENERAL INFO ####################################################
def general_info():
    menu_variables = st.radio("",("Tabel Data", "Grafik"),)

    data_region = df_lengkap_frame.groupby("region",as_index=False)["produksi"].sum()
    data_subregion = df_lengkap_frame.groupby("subregion",as_index=False)["produksi"].sum()

######################## SUB MENU TABEL ########################     
    if menu_variables == "Tabel Data":
        st.write("Aplikasi Streamlit untuk menggambarkan Produksi Minyak Mentah tiap Negara di dunia dengan rentang waktu 1971–2016 Referensi API Streamlit: https://docs.streamlit.io/library/api-reference")
        st.subheader("DATA LENGKAP")
        st.write(f"Data ini terdiri dari {len(list_negara_unik)} negara")
        st.dataframe(df_lengkap_frame)
        
        left_col, right_col = st.columns(2)
        left_col.subheader("Rank Total Produksi Tiap **_SUBREGION_**")
        left_col.table(data_subregion.sort_values(by='produksi',ascending=False))

        right_col.subheader("Rank TOTAL PRODUKSI TIAP **_REGION_**")
        right_col.table(data_region.sort_values(by='produksi',ascending=False))
 ######################## SUB MENU TABEL ########################  

 ######################## SUB MENU GRAFIK ######################## 
    elif menu_variables == "Grafik":
        left_col, right_col = st.columns(2)
        cmap_name = 'tab10'
        cmap = cm.get_cmap(cmap_name)
        colors = cmap.colors[:len(data_region["region"])]
        fig, ax = plt.subplots()
        ax.barh(data_region["region"], data_region["produksi"], color = colors)
        ax.set_xticklabels(data_region["region"], rotation = 90)
        ax.set_xlabel("Region", fontsize=12)
        ax.set_ylabel("Produksi", fontsize=12)
        plt.tight_layout()
        left_col.subheader("Grafik Produksi Tiap Region")
        left_col.pyplot(fig)

        cmap_name1 = 'tab20'
        cmap1 = cm.get_cmap(cmap_name1)
        colors1 = cmap1.colors[:len(data_subregion["subregion"])]
        fig1, ax1 = plt.subplots()
        ax1.bar(data_subregion["subregion"], data_subregion["produksi"], color = colors1)
        ax1.set_xticklabels(data_subregion["subregion"], rotation = 90)
        ax1.set_xlabel("Subregion", fontsize=12)
        ax1.set_ylabel("Produksi", fontsize=12)
        plt.tight_layout()
        right_col.subheader("Grafik Produksi Tiap Subregion")
        right_col.pyplot(fig1)
######################## SUB MENU GRAFIK ######################## 


#################################################### MENU STATISTIK ####################################################
def menu_data():
    #PILIHAN MENU DI 'MENU STATISTIK'
    menu_variables = st.radio("",("Produksi Suatu Negara", "Produksi Negara per Tahun","Produksi Kumulatif Tiap Negara", "Negara yang Tidak Memproduksi"),)
    
    #MEMBAGI 2 KOLOM
    left_col, right_col = st.columns(2)

    #GROUPBY PRODUKSI KUMULATIF
    sum_prod = df_lengkap_frame.groupby(['nama negara','kode negara', 'region', 'subregion'], as_index=False)['produksi'].sum() 

    #MEMBUAT DATAFRAME BARU TANPA PRODUKSI = 0
    #Angka 2 dalam variabel menandakan data tanpa kolom produksi bernilai 0
    df2 = df_lengkap_frame.drop(df.index[df['produksi'] == 0])    #Menghilangkan rows di produksi = 0

 ######################## SUB MENU PRODUKSI SUATU NEGARA ######################## 
    if menu_variables == "Produksi Suatu Negara":
        #DATAFRAME NEGARA YANG DIPILIH
        prod_N_negara = df.loc[df["kode_negara"] == pilih_negara]

        #DESKRIPSI DATA
        with st.expander(f"Deskripsi Produksi Minyak Mentah Negara {pilih_negara}"):
            st.code(prod_N_negara.produksi.describe())
        st.subheader(f"Produksi Minyak Mentah {pilih_negara}")
        
        col1, col2 = st.columns(2)  #MEMBAGI 2 KOLOM

        with col1:
            col1.markdown(f'Tabel')
            col1.dataframe(prod_N_negara)

        with col2:
            col2.markdown(f"Grafik")
            list_tahun_grafik = list()
            list_produksi = list()
            for i in df.index:
                if df['kode_negara'][i] == pilih_negara:
                    list_tahun_grafik.append(df['tahun'][i])
                    list_produksi.append(df['produksi'][i])
                    
            cmap_name1 = 'tab20'
            cmap1 = cm.get_cmap(cmap_name1)
            colors = cmap1.colors[:len(list_tahun_grafik)]
            fig1, ax1 = plt.subplots()
            ax1.bar(list_tahun, list_produksi, color=colors)
            ax1.set_xticklabels(list_tahun_grafik, rotation = 90)
            ax1.set_xlabel("Tahun", fontsize=12)
            ax1.set_ylabel("Produksi", fontsize=12)
            plt.tight_layout()

            col2.pyplot(fig1)
######################## SUB MENU PRODUKSI SUATU NEGARA ######################## 

######################## SUB MENU PRODUKSI NEGARA PER TAHUN ########################  
    elif menu_variables == "Produksi Negara per Tahun":  

        #SORTING DARI TAHUN PILIHAN
        df_lengkap_frame_T = df_lengkap_frame.loc[df_lengkap_frame["tahun"] == pilih_tahun]
        df2_T = df2.loc[df2["tahun"] == pilih_tahun]
        #SORTING VALUES DAN LIMITASI ROWS
        sort_df_lengkap_frame_T = df_lengkap_frame_T.sort_values(by='produksi',ascending=False)
        df_lengkap_frame_T_B = sort_df_lengkap_frame_T[0:n_tampil]
        
        #DESKRIPSI DATA
        with st.expander(f"Deskripsi Produksi {n_tampil} Besar Negara Pada Tahun {pilih_tahun}"):
            st.code(df_lengkap_frame_T_B.produksi.describe())

        st.markdown(f"### Data Produksi Minyak Mentah Tahun {pilih_tahun}")
        st.dataframe(df_lengkap_frame_T)
        st.subheader(f"Grafik {n_tampil} Besar Negara dengan Produksi Minyak Mentah Terbesar pada Tahun {pilih_tahun} di Dunia")
        
        col1, col2 = st.columns(2)

        with col1:
            #GRAFIK
            cmap_name2 = 'tab20'
            cmap2 = cm.get_cmap(cmap_name2)
            colors = cmap2.colors[:len(df_lengkap_frame_T_B)]
            fig2, ax2 = plt.subplots()
            ax2.bar(df_lengkap_frame_T_B["nama negara"], df_lengkap_frame_T_B["produksi"], color=colors)
            ax2.set_xticklabels(df_lengkap_frame_T_B["nama negara"], rotation = 90)
            ax2.set_xlabel("Negara", fontsize=12)
            ax2.set_ylabel("Produksi", fontsize=12)
            plt.tight_layout()
            col1.pyplot(fig2)

        with col2:
            col2.markdown("**INFORMASI**")
            #PRODUKSI TERBESAR TAHUN (T)
            biggest_prod_T = df_lengkap_frame_T.groupby(['nama negara','kode negara', 'region', 'subregion','tahun'])['produksi'].sum()
            col2.markdown(f"**Negara dengan jumlah produksi terbesar pada tahun {pilih_tahun}: ** \n {biggest_prod_T.idxmax()} sebesar **_{biggest_prod_T.max()}_**")

            #PRODUKSI TERKECIL TAHUN (T)
            smallest_prod_T = df2_T.groupby(['nama negara','kode negara', 'region', 'subregion','tahun'])['produksi'].sum()
            col2.markdown(f"**Negara dengan jumlah produksi terkecil pada tahun {pilih_tahun}: ** \n {smallest_prod_T.idxmin()} sebesar **_{smallest_prod_T.min()}_**")
######################## SUB MENU PRODUKSI NEGARA PER TAHUN ########################  

######################## SUB MENU PRODUKSI KUMULATIF TIAP NEGARA ########################  
    elif menu_variables == "Produksi Kumulatif Tiap Negara":

        #SORT DATA KUMULATIF TERBESAR
        prod_kumulatif_sort = sum_prod.nlargest(n_tampil, 'produksi')

        #DESKRIPSI DATA
        with st.expander(f"Deskripsi Produksi Kumulatif {n_tampil} Besar Negara"):
            st.code(prod_kumulatif_sort.produksi.describe())

        st.subheader(f"Data Produksi Minyak Mentah *Kumulatif*  Tiap Negara")
        st.dataframe(sum_prod)

        st.subheader(f"Grafik {n_tampil} Besar Negara dengan Produksi Minyak Mentah *Kumulatif* Terbesar di Dunia") 

        col1, col2 = st.columns(2)

        with col1:
            #GRAFIK
            cmap_name3 = 'tab20'
            cmap3 = cm.get_cmap(cmap_name3)
            colors = cmap3.colors[:n_tampil]
            fig3, ax3 = plt.subplots()
            ax3.bar(prod_kumulatif_sort["nama negara"], prod_kumulatif_sort["produksi"], color=colors)
            ax3.set_xticklabels(prod_kumulatif_sort["nama negara"], rotation = 90)
            ax3.set_xlabel("Negara", fontsize=12)
            ax3.set_ylabel("Produksi Kumulatif", fontsize=12)
            plt.tight_layout()
            col1.pyplot(fig3)
            
        with col2:
            col2.markdown("**INFORMASI**")
            #PRODUKSI KUMULATIF 'TERBESAR'
            biggest_prod_kumulatif = df_lengkap_frame.groupby(['nama negara','kode negara', 'region', 'subregion'])['produksi'].sum() 
            col2.markdown(f"**Negara dengan Jumlah produksi Kumulatif Terbesar: ** \n {biggest_prod_kumulatif.idxmax()} sebesar **_{biggest_prod_kumulatif.max()}_**")
            
            #PRODUKSI KUMULATIF 'TERKECIL'
            smallest_prod_kumulatif = df2.groupby(['nama negara','kode negara', 'region', 'subregion'])['produksi'].sum()
            col2.markdown(f"**Negara dengan Jumlah Produksi Kumulatif Terkecil: ** \n {smallest_prod_kumulatif.idxmin()} sebesar **_{smallest_prod_kumulatif.min()}_**")
######################## SUB MENU PRODUKSI KUMULATIF TIAP NEGARA ########################  

######################## SUB MENU NEGARA YANG TIDAK PRODUKSI ########################   
    elif menu_variables == "Negara yang Tidak Memproduksi":

        #NEGARA DENGAN PRODUKSI KUMULATIF 0
        sum0 = sum_prod.loc[sum_prod["produksi"] == 0]
        st.subheader("Bukan Negara Pemroduksi Minyak Mentah")
        st.dataframe(sum0)
        st.markdown(f"Terdapat **_{len(sum0.index)}_** Negara yang Tidak Pernah Memproduksi Sama Sekali (produksi kumulatif = 0)")

        #NEGARA DENGAN PRODUKSI 0 DI TAHUN (T)
        st.header(" ")
        prod0 = df_lengkap_frame.loc[(df["produksi"] == 0) & (df["tahun"] == pilih_tahun)]
        prod0_T = prod0.loc[:,['nama negara','kode negara', 'region', 'subregion']]
        #prod00 = prod0[['kode_negara',"produksi"]]    #UNTUK MENAMPILKAN KOLOM KODE NEGARA & PRODUKSI
        st.subheader(f"Negara yang Tidak Memproduksi Minyak di tahun {pilih_tahun}")
        st.dataframe(prod0_T)
        st.markdown(f"Pada Tahun **_{pilih_tahun}_**, Terdapat **_{len(prod0_T.index)}_** Negara yang Tidak Berproduksi (Produksi = 0)")
######################## SUB MENU NEGARA YANG TIDAK PRODUKSI ######################## 
#################################################### MENU STATISTIK ####################################################


#MEMANGGIL FUNGSI
if menu == "General Info":
    general_info()
elif menu == "Statistik":
    menu_data()
