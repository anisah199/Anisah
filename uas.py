import json 
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

df_csv = pd.read_csv('produksi_minyak_mentah.csv') #dataframe
with open("kode_negara_lengkap.json") as f : 
    file_json = json.load(f) 
df_json = pd.DataFrame.from_dict(file_json, orient='columns')

st.set_page_config(page_title='Produksi Minyak Berbagai Negara Tahun 1971-2015',
                   layout='wide')
st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.image('https://ditsti.itb.ac.id/wp-content/uploads/2020/09/logo_itb_128.png' )
      
title = '<p style="font-family: sans-serif; font-size: 40px; text-align: left;"><b>Produksi Minyak Mentah Negara di Dunia Tahun 1971-2015</b></p>'
st.markdown(title, unsafe_allow_html=True)

st.markdown(
        """
        <style>
        .reportview-container {
            background: url("https://www.pinsentmasons.com/-/media/images/cards/oil-rig-sunset.jpg?la=en-gb")
        }
    .sidebar .sidebar-content {
            background: url("https://wallpaperaccess.com/full/2959083.jpg")
        }
        </style>
        """,
        unsafe_allow_html=True
    )

#hapus yang gakepake dulu 

list_unused_kode= [] #list yang perlu dihapus 

for i in list(df_csv['kode_negara']): 
    if i not in list (df_json['alpha-3']): 
        list_unused_kode.append(i)  

for i in list_unused_kode: 
    df_csv = df_csv[df_csv.kode_negara != i]

new_list_KodeNegara =[] #data kepake semua
for i in list(df_csv['kode_negara']): 
    new_list_KodeNegara.append(i) #list kode_negara

list_NamaNegara = []
for i in range(len(new_list_KodeNegara)):
    for j in range(len(list(df_json['alpha-3']))):
        if list(df_json['alpha-3'])[j] == new_list_KodeNegara[i]:
            list_NamaNegara.append(list(df_json['name'])[j])

list_produksi = []
for i in range(len(list(df_csv['produksi']))): 
    list_produksi.append(list(df_csv['produksi'])[i])

list_tahun = []
for i in range(len(list(df_csv['tahun']))): 
    list_tahun.append(list(df_csv['tahun'])[i])

list_tahun_kumulatif = [] #tahun yang ga ngulang --> buat select box
for i in list(df_csv['tahun']):
    if i not in list_tahun_kumulatif: 
        list_tahun_kumulatif.append(i)

df_a = pd.DataFrame(list(zip(list_NamaNegara, new_list_KodeNegara, list_tahun, list_produksi)), columns=[
                         'Nama Negara','Kode Negara', 'Tahun', 'Produksi'])
            
list_NamaNegara_kumulatif_all= []

for i in list(df_a['Nama Negara']):
    if i not in list_NamaNegara_kumulatif_all:
            list_NamaNegara_kumulatif_all.append(i)

list_pilihanuser = ['Grafik Jumlah Produksi Minyak Mentah tiap Tahun' ,'Grafik Jumlah Produksi Minyak Mentah Terbesar','Grafik Jumlah Produksi Minyak Mentah Kumulatif', 'Data Lengkap Produksi Minyak Mentah Berbagai Negara']
pilihan_user =st.sidebar.radio('Pilih Menu:', list_pilihanuser)
if pilihan_user == list_pilihanuser [0]:
    pilihan_user = 1
elif pilihan_user == list_pilihanuser [1]:
    pilihan_user = 2
elif pilihan_user == list_pilihanuser [2]:
    pilihan_user = 3
elif pilihan_user == list_pilihanuser [3]:
    pilihan_user = 4

#a --> butuh data frame isi: nama negara, tahun, produksi
if pilihan_user == 1 : 
    st.title('Grafik Jumlah Produksi Minyak Mentah tiap Tahun')

    nama = st.selectbox("Daftar Negara", list_NamaNegara_kumulatif_all)
    df_a_print = df_a.loc[df_a['Nama Negara'] == nama]

    df_a_print.plot(x='Tahun', y='Produksi', title= "Grafik Jumlah Produksi Minyak Mentah terhadap Waktu (tahun) dari Suatu Negara", color='darkgoldenrod', linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='gold', markersize=10)

    grafik_a = plt.show()
    st.pyplot(grafik_a)

#b --> butuh data frame isi: nama negara, tahun, produksi (sama kaya poin a jadi bisa pake df_a)
if pilihan_user == 2 : 
    st.title('Grafik Jumlah Produksi Minyak Mentah Terbesar')

#tahun_b= int(input("Produksi pada Tahun berapa:"))
    tahun_b = st.selectbox("Produksi pada Tahun Berapa", list_tahun_kumulatif)
    tahun_b = int(tahun_b)
    banyak_b = st.slider('Jumlah negara yang ditampilkan: ', 1, 137)
    banyak_b = int(banyak_b)

    df_b = df_a.loc[df_a['Tahun'] == tahun_b]
    df_b_sort = df_b.sort_values(by=['Produksi'], ascending=False)
    df_b_print = df_b_sort[:banyak_b]
    df_b_print.plot.bar(x='Nama Negara', y='Produksi', title = "Grafik Jumlah Produksi terbesar" , width = 0.8, color = ['goldenrod', 'goldenrod', 'gold'])

    grafik_b = plt.show()
    st.pyplot(grafik_b)

#c butuh data frame isi: nama negara (tidak diulang), kumulatif produksi
if pilihan_user == 3 : 
    st.title('Grafik Jumlah Produksi Minyak Mentah Kumulatif')

    banyak_c = st.slider('Jumlah negara yang ditampilkan: ', 1, 150)
    banyak_c = int(banyak_c)

    list_produksi_kumulatif_all = [] #masih bingung
    for i in list_NamaNegara_kumulatif_all:
        df_sum_c = df_a.loc[df_a['Nama Negara'] == i, 'Produksi'].sum()
        list_produksi_kumulatif_all.append(df_sum_c)
            
    df_c = pd.DataFrame(list(zip(list_NamaNegara_kumulatif_all, list_produksi_kumulatif_all)), columns=['Nama Negara', 'Produksi Kumulatif']) #udah kumulatif
    df_c_sort= df_c.sort_values(by=['Produksi Kumulatif'], ascending=False).head(banyak_c) #ngurutin

    df_c_sort.plot.bar(x='Nama Negara', y='Produksi Kumulatif', title = "Grafik Produksi Jumlah Kumulatif Terbesar", width = 0.8, color = ['goldenrod', 'goldenrod', 'gold'])
    grafik_c = plt.show()
    st.pyplot(grafik_c)

#d'
#keperluan data, butuh data frame isi: kode negara, nama negara, region, sub-region, tahun, produksi
if pilihan_user == 4 : 
    st.title('Data Lengkap Produksi Minyak Mentah Berbagai Negara')

    list_Region = []
    list_SubRegion = []
    for i in range(len(new_list_KodeNegara)):
        for j in range(len(list(df_json['alpha-3']))):
            if list(df_json['alpha-3'])[j] == new_list_KodeNegara[i]:
                list_Region.append(list(df_json['region'])[j])
                list_SubRegion.append(list(df_json['sub-region'])[j])

    df_d = pd.DataFrame(list(zip(list_NamaNegara, new_list_KodeNegara, list_Region, list_SubRegion, list_tahun, list_produksi)), columns=[
                         'Nama Negara','Kode Negara', 'Region', 'Sub-Region', 'Tahun', 'Produksi'])
    tahun_d = st.slider('Produksi pada Tahun Berapa', 1971, 2015)
    tahun_d = int(tahun_d)

    #terbesar
    st.title('Data Lengkap Produksi Minyak Mentah Terbesar')

    df_d_t = df_d.loc[df_d['Tahun'] == tahun_d]
    df_d_sort_Produksi = df_d_t.sort_values(by=['Produksi'], ascending=False)
    df_d_print_Negara = df_d_sort_Produksi[:1].iloc[0]['Nama Negara']
    df_d_print_Kode = df_d_sort_Produksi[:1].iloc[0]['Kode Negara']
    df_d_print_Region = df_d_sort_Produksi[:1].iloc[0]['Region']
    df_d_print_subRegion = df_d_sort_Produksi[:1].iloc[0]['Sub-Region']
    df_d_print_Produksi = df_d_sort_Produksi[:1].iloc[0]['Produksi']

    df_d_sort_Produksi_all = df_d.sort_values(by=['Produksi'], ascending=False)
    df_d_print_Negara_all = df_d_sort_Produksi_all[:1].iloc[0]['Nama Negara']
    df_d_print_Kode_all = df_d_sort_Produksi_all[:1].iloc[0]['Kode Negara']
    df_d_print_Region_all = df_d_sort_Produksi_all[:1].iloc[0]['Region']
    df_d_print_subRegion_all = df_d_sort_Produksi_all[:1].iloc[0]['Sub-Region']
    df_d_print_Produksi_all = df_d_sort_Produksi_all[:1].iloc[0]['Produksi']
    df_d_print_Tahun_all = df_d_sort_Produksi_all[:1].iloc[0]['Tahun']

    col1, col2 = st.columns(2)

    with col1:
        st.header(f'Data Produksi Terbesar Tahun {tahun_d}')
        st.subheader('Data Negara Terkait')
        st.write('Nama Negara:', df_d_print_Negara, '\n')
        st.write('Kode Negara:', df_d_print_Kode, '\n')
        st.write('Region:', df_d_print_Region, '\n' )
        st.write('Sub Region:', df_d_print_subRegion, '\n' )
        st.write('Jumlah Produksi:', df_d_print_Produksi, '\n')
        

    with col2:
        st.header('Data Produksi Terbesar Keseluruhan Tahun')
        st.subheader('Data Negara Terkait')
        st.write('Nama Negara:', df_d_print_Negara_all, '\n')
        st.write('Kode Negara:', df_d_print_Kode_all, '\n')
        st.write('Region:', df_d_print_Region_all, '\n')
        st.write('Sub Region:', df_d_print_subRegion_all, '\n')
        st.write('Jumlah Produksi:', df_d_print_Produksi_all, '\n')
        st.write('Produksi Terbesar terjadi pada Tahun', df_d_print_Tahun_all, '\n')
     

    #terkecil (tidak nol)

    st.title('Data Lengkap Produksi Minyak Mentah Terkecil')
    df_d_t = df_d.loc[df_d['Tahun'] == tahun_d]
    df_d_t_min = df_d_t[df_d_t.Produksi != 0]
    df_d_sort_Produksi_min = df_d_t_min.sort_values(by=['Produksi'], ascending=True)
    df_d_print_Negara_min = df_d_sort_Produksi_min [:1].iloc[0]['Nama Negara']
    df_d_print_Kode_min = df_d_sort_Produksi_min [:1].iloc[0]['Kode Negara']
    df_d_print_Region_min = df_d_sort_Produksi_min [:1].iloc[0]['Region']
    df_d_print_subRegion_min = df_d_sort_Produksi_min [:1].iloc[0]['Sub-Region']
    df_d_print_Produksi_min = df_d_sort_Produksi_min [:1].iloc[0]['Produksi']

    df_d_min = df_d[df_d.Produksi != 0]
    df_d_sort_Produksi_all_min = df_d_min.sort_values(by=['Produksi'], ascending=True)
    df_d_print_Negara_all_min = df_d_sort_Produksi_all_min[:1].iloc[0]['Nama Negara']
    df_d_print_Kode_all_min = df_d_sort_Produksi_all_min[:1].iloc[0]['Kode Negara']
    df_d_print_Region_all_min = df_d_sort_Produksi_all_min[:1].iloc[0]['Region']
    df_d_print_subRegion_all_min = df_d_sort_Produksi_all_min[:1].iloc[0]['Sub-Region']
    df_d_print_Produksi_all_min = df_d_sort_Produksi_all_min[:1].iloc[0]['Produksi']
    df_d_print_Tahun_all_min = df_d_sort_Produksi_all_min[:1].iloc[0]['Tahun']

    col1, col2 = st.columns(2)

    with col1:
        st.header(f'Data Produksi Tekecil Tahun {tahun_d}')
        st.subheader('Data Negara Terkait')
        st.write('Nama Negara:', df_d_print_Negara_min, '\n')
        st.write('Kode Negara:', df_d_print_Kode_min, '\n')
        st.write('Region:', df_d_print_Region_min, '\n')
        st.write('Sub Region:', df_d_print_subRegion_min, '\n')
        st.write('Jumlah Produksi:', df_d_print_Produksi_min, '\n')
        

    with col2:
        st.header('Data Produksi Tekecil Keseluruhan Tahun')
        st.subheader('Data Negara Terkait')
        st.write('Nama Negara:', df_d_print_Negara_all_min, '\n')
        st.write('Kode Negara:', df_d_print_Kode_all_min, '\n')
        st.write('Region:', df_d_print_Region_all_min, '\n')
        st.write('Sub Region:', 'Sub Region:', df_d_print_subRegion_all_min, '\n')
        st.write('Jumlah Produksi:', df_d_print_Produksi_all_min, '\n')
        st.write('Produksi Terkecil terjadi pada Tahun', df_d_print_Tahun_all_min, '\n')
        
    #kumulatif (perlu  list kode, region, sub-region yang kumulatif terus buat df dengan list kumulatif semua )
    
    list_nama_kumulatif= []
    for i in list(df_d['Nama Negara']):
        if i not in list_nama_kumulatif:
                list_nama_kumulatif.append(i)

    list_kode_kumulatif= []
    for i in list(df_d['Kode Negara']):
        if i not in list_kode_kumulatif:
                list_kode_kumulatif.append(i)

    list_region_kumulatif= []
    for i in list(df_d['Region']):
        if i not in list_region_kumulatif:
                list_region_kumulatif.append(i)

    list_subregion_kumulatif= []
    for i in list(df_d['Sub-Region']):
        if i not in list_subregion_kumulatif:
                list_subregion_kumulatif.append(i)
    
    list_produksi_kumulatif = [] 
    for i in list_NamaNegara_kumulatif_all:
        df_sum_d = df_d.loc[df_a['Nama Negara'] == i, 'Produksi'].sum()
        list_produksi_kumulatif.append(df_sum_d)

    df_d2 = pd.DataFrame(list(zip(list_nama_kumulatif, list_kode_kumulatif, list_region_kumulatif, list_subregion_kumulatif, list_produksi_kumulatif)), columns=[
                             'Nama Negara','Kode Negara', 'Region', 'Sub-Region','Produksi Kumulatif'])   

    #kumulatif terbesar 
    df_d2_sort_k_max = df_d.sort_values(by=['Produksi Kumulatif'], ascending=False)
    #kumulatif terkecil
    df_d2_sort_k_min = df_d.sort_values(by=['Produksi Kumulatif'], ascending=True)
    
    col1, col2 = st.columns(2)

    with col1:
        st.header(f'Data Produksi Kumulatif Terbesar')
        st.subheader('Data Negara Terkait')
        st.write('Nama Negara:',df_d2_sort_k_max[:1].iloc[0]['Nama Negara'], '\n')
        st.write('Kode Negara:', df_d2_sort_k_max[:1].iloc[0]['Kode Negara'], '\n')
        st.write('Region:', df_d2_sort_k_max[:1].iloc[0]['Region'], '\n')
        st.write('Sub Region:', df_d2_sort_k_max[:1].iloc[0]['Sub-Region'], '\n')
        st.write('Jumlah Produksi:', df_d2_sort_k_max[:1].iloc[0]['Jumlah Produksi'],'\n')
        

    with col2:
        st.header('Data Produksi Kumulatif Terkecil')
        st.subheader('Data Negara Terkait')
        st.write('Nama Negara:', df_d2_sort_k_min[:1].iloc[0]['Nama Negara'], '\n')
        st.write('Kode Negara:', df_d2_sort_k_min[:1].iloc[0]['Kode Negara'], '\n')
        st.write('Region:', df_d2_sort_k_min[:1].iloc[0]['Region'], '\n')
        st.write('Sub Region:', 'Sub Region:', df_d2_sort_k_min[:1].iloc[0]['Sub-Region'], '\n')
        st.write('Jumlah Produksi:', df_d2_sort_k_min[:1].iloc[0]['Jumlah Produksi'], '\n')
        
    #produksi nol
    st.title('Data Lengkap Produksi Nol Minyak Mentah')
    #tahun pilihan user
    df_d_0 = df_d.loc[df_d['Tahun'] == tahun_d]
    df_d_nol = df_d_0[df_d_0.Produksi == 0]
    list_Negara_nol =[]
    list_Kode_nol = []
    list_Region_nol =[]
    list_SubRegion_nol =[]

    for i in range(len(df_d_nol)):
        for j in range(len(df_json)):
            if list(df_d_nol['Kode Negara'])[i] == list(df_json['alpha-3'])[j]:
                list_Negara_nol.append(list(df_d_nol['Nama Negara'])[i])
                list_Kode_nol.append(list(df_d_nol['Kode Negara'])[i])
                list_Region_nol.append(list(df_d_nol['Region'])[i])
                list_SubRegion_nol.append(list(df_d_nol['Sub-Region'])[i])

    df_produksinol = pd.DataFrame(list(zip(list_Negara_nol, list_Kode_nol, list_Region_nol, list_SubRegion_nol)), columns=[
                            'Nama Negara','Kode Negara', 'Region', 'Sub-Region'])
                
  
    st.title(f'Produksi Nol pada Tahun {tahun_d}')
    st.caption('Di bawah ini terdapat tabel yang menunjukkan informasi mengenai negara dengan **_produksi minyak nol_** :arrow_down::arrow_down:')
    st.dataframe(df_produksinol)

    #keseluruhan tahun
    df_d_nol_all = df_d[df_d.Produksi == 0]
    list_Negara_nol_all =[]
    list_Kode_nol_all = []
    list_Region_nol_all =[]
    list_SubRegion_nol_all =[]
    list_tahun_nol_all =[]

    for i in range(len(df_d_nol_all)):
        for j in range(len(df_json)):
            if list(df_d_nol_all['Kode Negara'])[i] == list(df_json['alpha-3'])[j]:
                list_Negara_nol_all.append(list(df_d_nol_all['Nama Negara'])[i])
                list_Kode_nol_all.append(list(df_d_nol_all['Kode Negara'])[i])
                list_Region_nol_all.append(list(df_d_nol_all['Region'])[i])
                list_SubRegion_nol_all.append(list(df_d_nol_all['Sub-Region'])[i])
                list_tahun_nol_all.append(list(df_d_nol_all['Tahun'])[i])

    df_produksinol_all = pd.DataFrame(list(zip(list_Negara_nol_all, list_Kode_nol_all, list_Region_nol_all, list_SubRegion_nol_all, list_tahun_nol_all)), columns=[
                            'Nama Negara','Kode Negara', 'Region', 'Sub-Region','Tahun'])

    #print('Produksi Nol Keseluruhan Tahun')
    st.title('Produksi Nol pada keseluruhan Tahun')
    st.caption('Di bawah ini terdapat tabel yang menunjukkan informasi mengenai negara dengan **_produksi minyak nol_ pada keseluruhan tahun** :arrow_down::arrow_down:')
    st.dataframe(df_produksinol_all)
