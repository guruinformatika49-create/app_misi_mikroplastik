import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import io

# --- 0. KONFIGURASI DAN INIALISASI SESSION STATE ---

# Konfigurasi Streamlit
st.set_page_config(
    page_title="Data Driven Trash Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Template DataFrame SMART
DEFAULT_SMART_DF = pd.DataFrame({
    'Komponen SMART': ['S – Specific', 'M – Measurable', 'A – Achievable', 'R – Relevant', 'T – Time-bound'],
    'Pertanyaan Panduan': [
        'Apa tepatnya yang akan dilakukan?', 
        'Bagaimana cara mengukur keberhasilannya?', 
        'Apakah mungkin dilakukan dengan sumber daya yang ada?', 
        'Apa hubungan solusi ini dengan masalah? Mengapa penting?', 
        'Kapan target ini harus tercapai?'
    ],
    'Jawabanmu': ['Tulis di sini...', 'Tulis di sini...', 'Tulis di sini...', 'Tulis di sini...', 'Tulis di sini...']
})

# Inisialisasi Session State Global
if 'report_submitted' not in st.session_state: st.session_state.report_submitted = False
if 'final_solusi' not in st.session_state: st.session_state.final_solusi = ""
if 'final_jenis' not in st.session_state: st.session_state.final_jenis = ""
if 'final_nama' not in st.session_state: st.session_state.final_nama = ""
if 'uploaded_df' not in st.session_state: st.session_state.uploaded_df = None
if 'current_nama_siswa' not in st.session_state: st.session_state.current_nama_siswa = ""
if 'analisis_run' not in st.session_state: st.session_state.analisis_run = False
if 'kriteria_1' not in st.session_state: st.session_state.kriteria_1 = False
if 'kriteria_2' not in st.session_state: st.session_state.kriteria_2 = False
if 'solusi_aksi_nyata' not in st.session_state: st.session_state.solusi_aksi_nyata = ""
if 'dominan_jenis' not in st.session_state: st.session_state.dominan_jenis = ""
# Kunci baru untuk menyimpan data editor secara manual
if 'smart_data_temp' not in st.session_state: st.session_state.smart_data_temp = DEFAULT_SMART_DF.copy()


# --- 1. FUNGSI CALLBACK ---

def run_analisis_callback():
    """Callback untuk tombol Run Analisis. Reset state form dan data editor."""
    
    if st.session_state.uploaded_df is not None and st.session_state.current_nama_siswa:
        # Set status analisis dan reset form
        st.session_state.analisis_run = True
        st.session_state.report_submitted = False
        st.session_state.kriteria_1 = False
        st.session_state.kriteria_2 = False
        st.session_state.solusi_aksi_nyata = ""
        
        # PENTING: Reset smart_data_temp (kunci tempat data edit disimpan)
        st.session_state.smart_data_temp = DEFAULT_SMART_DF.copy() 
        
        st.rerun()
    else:
        st.error("Gagal menjalankan analisis. Pastikan file Excel sudah diunggah dan nama kelompok terisi.")

def submit_report_callback():
    """Callback function untuk tombol Selesaikan Laporan. Mengambil data dari smart_data_temp."""
    
    # Ambil data dari kunci yang sekarang menampung hasil edit
    df_smart = st.session_state.smart_data_temp 
    jawaban_smart = df_smart['Jawabanmu'].tolist()
    aksi_nyata = st.session_state.solusi_aksi_nyata
    k1_check = st.session_state.kriteria_1
    k2_check = st.session_state.kriteria_2
    
    # 1. Validasi Input
    if any(j == 'Tulis di sini...' or not j for j in jawaban_smart) or not aksi_nyata:
        st.error("❌ **ERROR:** Mohon lengkapi **SEMUA** kolom 'Jawabanmu' di tabel SMART dan kolom Aksi Nyata.")
        return
        
    if not k1_check or not k2_check:
        st.error("❌ **ERROR:** Mohon centang kedua kriteria Laporan Aksi (Specific dan Measurable) sebelum menyelesaikan laporan.")
        return
    
    # 2. Proses dan Simpan Data jika Validasi Lolos
    solusi_input_final = (
        f"**Tujuan SMART:**\n"
        f"- S (Specific): {jawaban_smart[0]}\n"
        f"- M (Measurable): {jawaban_smart[1]}\n"
        f"- A (Achievable): {jawaban_smart[2]}\n"
        f"- R (Relevant): {jawaban_smart[3]}\n"
        f"- T (Time-bound): {jawaban_smart[4]}\n\n"
        f"**Rencana Aksi Nyata (5 Poin):**\n{aksi_nyata}"
    )
        
    # Set Final State
    st.session_state.report_submitted = True
    st.session_state.final_solusi = solusi_input_final
    st.session_state.final_jenis = st.session_state.dominan_jenis
    st.session_state.final_nama = st.session_state.current_nama_siswa

    st.rerun() 

# --- FUNGSI PENDUKUNG LAINNYA ---

def generate_feedback(jenis_dominan_str):
    fakta_1, fakta_2, rekomendasi, img_query = "", "", "", ""

    if "Botol PET" in jenis_dominan_str:
        fakta_1 = "Fakta Mengkhawatirkan: Botol PET membutuhkan waktu sekitar 450 tahun untuk terurai. Sebagian besar botol hanya digunakan sekali!"
        fakta_2 = "Jutaan ton botol PET berakhir di lautan setiap tahun. Mereka terfragmentasi menjadi mikroplastik yang memasuki rantai makanan kita."
        rekomendasi = "Rekomendasi Penanganan: Wajibkan penggunaan botol minum (tumbler) isi ulang di seluruh area sekolah (guru dan siswa)."
        img_query = "Reusable water bottle vs single use plastic bottle"
    elif "Bungkus Snack" in jenis_dominan_str or "Plastik Film" in jenis_dominan_str:
        fakta_1 = "Fakta Mengkhawatirkan: Bungkus berlapis (multilayer) seperti bungkus snack hampir tidak mungkin didaur ulang secara ekonomis."
        fakta_2 = "Bungkus ini langsung menjadi residu yang menumpuk di TPA atau dibakar, menghasilkan gas beracun yang membahayakan kesehatan paru-paru."
        rekomendasi = "Rekomendasi Penanganan: Dorong siswa membawa bekal makanan ringan dari rumah dalam wadah yang dapat dipakai ulang (tupperware)."
        img_query = "Multilayer plastic packaging"
    elif "Sedotan" in jenis_dominan_str:
        fakta_1 = "Fakta Mengkhawatirkan: Meskipun ringan, sedotan adalah penyumbang mikroplastik berbahaya yang mudah dicerna oleh biota laut."
        fakta_2 = "Karena bentuknya, sedotan sulit disaring oleh mesin daur ulang dan sering kali langsung menjadi sampah residu."
        rekomendasi = "Rekomendasi Penanganan: Larang penyediaan sedotan plastik di kantin dan ganti dengan sedotan kertas atau tidak sama sekali."
        img_query = "Microplastic pollution in ocean"
    else: 
        fakta_1 = "Fakta Mengkhawatirkan: Setiap tahun, jutaan ton plastik berakhir di TPA dan mencemari lingkungan. Perubahan dimulai dari kesadaran kita!"
        fakta_2 = "Sampah yang tidak terkelola dengan baik menyebabkan banjir karena menyumbat saluran air dan menjadi sarang penyakit."
        rekomendasi = "Rekomendasi Penanganan: Adakan pelatihan pemilahan sampah yang ketat (organik vs non-organik) untuk meningkatkan efektivitas daur ulang di sekolah."
        img_query = "Global plastic waste problem"
        
    kata_mutiara = [
        "Bumi adalah rumah kita, mari jaga ia dengan aksi nyata, bukan hanya kata-kata.",
        "Sampah adalah cerminan peradaban. Mari tunjukkan bahwa peradaban kita bersih dan bijaksana.",
        "Kita tidak mewarisi bumi dari leluhur kita; kita meminjamnya dari anak cucu kita.",
        "Masa depan hijau hijau dimulai dengan keputusan kecil hari ini."
    ]
    
    return fakta_1, fakta_2, rekomendasi, random.choice(kata_mutiara), img_query

def display_final_report():
    nama = st.session_state.final_nama
    solusi = st.session_state.final_solusi
    jenis = st.session_state.final_jenis
    
    if not jenis or not nama or not solusi:
        return 

    fakta_1, fakta_2, rekomendasi, kata_mutiara_pilihan, img_query = generate_feedback(jenis)

    st.balloons()
    st.markdown(f"""
        <div style='background-color:#007bff; color:white; padding:20px; text-align:center; border-radius:10px;'>
            <h1 style='margin:0;'>🎉 SELAMAT! {nama.upper()}! 🎉</h1>
            <p style='font-size:1.2em;'>Anda telah berhasil menyelesaikan Proyek "Data Driven Trash Tracker"!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🔬 Laporan Temuan dan Apresiasi")
    st.markdown(f"""
        <div style='border: 1px solid #ced4da; padding: 15px; background-color: #f8f9fa; border-radius: 5px;'>
            <p><b>Fokus Utama Proyek Anda:</b> {jenis}</p>
            <hr>
            <p style='font-weight: bold; color:#dc3545;'>🚨 {fakta_1}</p>
            <p style='font-weight: bold; color:#dc3545;'>🚨 {fakta_2}</p>
            <p><b>Langkah Rekomendasi:</b> {rekomendasi}</p>
            <hr>
            <p><b>Rencana Solusi SMART Anda:</b></p>
            <div style='white-space: pre-wrap; padding: 10px; border: 1px dashed #ccc; background-color: #fff;'>{solusi}</div>
            <hr>
            <p style='font-style: italic;'>"{kata_mutiara_pilihan}"</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Visualisasi Dampak dan Solusi ({jenis}):**")
    st.image("https://via.placeholder.com/800x300.png?text=Contoh+Dampak+atau+Solusi+untuk+" + jenis.replace(" ", "+"))


# --- 2. FUNGSI ANALISIS DATA (INTI TAHAP 2 & 3) ---

def run_analisis(df, nama_siswa):
    """Menganalisis data, menampilkan visualisasi, dan memunculkan form solusi."""

    st.header("📊 Tahap 2: Hasil Analisis Data Audit")
    
    data_berat_per_jenis = df.groupby('Jenis Plastik')['Berat (gram)'].sum().sort_values(ascending=False)
    total_berat_keseluruhan = data_berat_per_jenis.sum()
    
    jenis_terdominan = data_berat_per_jenis.index[0] if not data_berat_per_jenis.empty else "Tidak Ada Data Plastik"
    berat_terdominan = data_berat_per_jenis.values[0] if not data_berat_per_jenis.empty else 0

    st.session_state.dominan_jenis = jenis_terdominan

    # Kotak Info dengan Kontras (PERBAIKAN DI SINI)
    st.markdown(f"""
        <div style='background-color:#ffeeba; color:#000000; padding:15px; border-radius:5px; border:1px solid #ffcc00;'>
            <b>Total Sampah Plastik yang Diaudit:</b> <b>{total_berat_keseluruhan:.2f} gram</b>.<br>
            <b>Jenis Paling Dominan:</b> <b>{jenis_terdominan}</b> (<b>{berat_terdominan:.2f} gram</b>).<br>
            Fokus solusi kita harus ada pada jenis ini!
        </div>
    """, unsafe_allow_html=True)
    
    if not data_berat_per_jenis.empty:
        col1, col2 = st.columns(2)
        
        # Visualisasi 1: Diagram Batang
        with col1:
            st.subheader("1. Kontributor Utama Sampah Plastik")
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            ax1.bar(data_berat_per_jenis.index, data_berat_per_jenis.values, 
                    color=plt.cm.viridis(data_berat_per_jenis.values / total_berat_keseluruhan))
            ax1.set_title('Berat Total Sampah Plastik (Gram)', fontsize=12)
            ax1.set_xlabel('Jenis Plastik')
            ax1.set_ylabel('Berat Total (gram)')
            plt.xticks(rotation=45, ha='right', fontsize=9)
            plt.tight_layout()
            st.pyplot(fig1) 
            
        
        # Visualisasi 2: Diagram Lingkaran
        with col2:
            st.subheader("2. Persentase Kontribusi")
            fig2, ax2 = plt.subplots(figsize=(5, 5))
            
            data_pie = data_berat_per_jenis[data_berat_per_jenis / total_berat_keseluruhan > 0.05]
            other_berat = total_berat_keseluruhan - data_pie.sum()
            if other_berat > 0 and not data_pie.empty: 
                data_pie['Lain-lain'] = other_berat

            if not data_pie.empty: 
                ax2.pie(data_pie.values, labels=data_pie.index, autopct='%1.1f%%', startangle=140, 
                        colors=plt.cm.Set3.colors, wedgeprops={'edgecolor': 'black'})
                ax2.set_title('Persentase Kontribusi', fontsize=12)
                ax2.axis('equal') 
                st.pyplot(fig2)
            else:
                st.warning("Tidak cukup data plastik untuk membuat Diagram Lingkaran
