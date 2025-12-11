import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import io

# --- 0. KONFIGURASI DAN INIALISASI SESSION STATE ---

# Konfigurasi Streamlit (Header, Layout, dll.)
st.set_page_config(
    page_title="Data Driven Trash Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi Session State Global (Dikosolidasikan di sini)
if 'report_submitted' not in st.session_state:
    st.session_state.report_submitted = False
if 'final_solusi' not in st.session_state:
    st.session_state.final_solusi = ""
if 'final_jenis' not in st.session_state:
    st.session_state.final_jenis = ""
if 'final_nama' not in st.session_state:
    st.session_state.final_nama = ""
if 'uploaded_df' not in st.session_state:
    st.session_state.uploaded_df = None
if 'current_nama_siswa' not in st.session_state:
    st.session_state.current_nama_siswa = ""
if 'analisis_run' not in st.session_state:
    st.session_state.analisis_run = False
if 'kriteria_1' not in st.session_state:
    st.session_state.kriteria_1 = False
if 'kriteria_2' not in st.session_state:
    st.session_state.kriteria_2 = False
if 'dominan_jenis' not in st.session_state:
    st.session_state.dominan_jenis = ""


def generate_feedback(jenis_dominan_str):
    # Logika Fakta dan Rekomendasi (Tidak Diubah)
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

def submit_report_callback():
    """Callback function untuk tombol Selesaikan Laporan."""
    
    # Dapatkan data dari Session State
    solusi_input = st.session_state.solusi_area
    k1_check = st.session_state.kriteria_1
    k2_check = st.session_state.kriteria_2
    
    # Data tambahan yang diperlukan untuk laporan akhir
    jenis_terdominan = st.session_state.get('dominan_jenis', 'Tidak Ada Data')
    nama_siswa = st.session_state.current_nama_siswa
    
    if not solusi_input:
        st.error("❌ **ERROR:** Mohon masukkan ide solusi Anda di kolom teks.")
        st.session_state.report_submitted = False
        return
        
    if not k1_check or not k2_check:
        st.error("❌ **ERROR:** Mohon centang kedua kriteria Laporan Aksi (Specific dan Measurable) sebelum menyelesaikan laporan.")
        st.session_state.report_submitted = False
        return
        
    # Jika validasi lolos, simpan hasil akhir ke Session State
    st.session_state.report_submitted = True
    st.session_state.final_solusi = solusi_input
    st.session_state.final_jenis = jenis_terdominan
    st.session_state.final_nama = nama_siswa

def display_final_report():
    # Logika display sama, tidak diubah
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
            <p><b>Solusi Utama yang Anda Ajukan:</b> {solusi}</p>
            <p><b>Fokus Utama Proyek Anda:</b> {jenis}</p>
            <hr>
            <p style='font-weight: bold; color:#dc3545;'>🚨 {fakta_1}</p>
            <p style='font-weight: bold; color:#dc3545;'>🚨 {fakta_2}</p>
            <p><b>Langkah Rekomendasi:</b> {rekomendasi}</p>
            <hr>
            <p style='font-style: italic;'>"{kata_mutiara_pilihan}"</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Visualisasi Dampak dan Solusi ({jenis}):**")
    st.image("https://via.placeholder.com/800x300.png?text=Contoh+Dampak+atau+Solusi+untuk+" + jenis.replace(" ", "+"))


# --- 2. FUNGSI ANALISIS DATA ---

def run_analisis(df, nama_siswa):
    """Menganalisis data, menampilkan visualisasi, dan memunculkan form solusi."""

    st.header("📊 Tahap 2: Hasil Analisis Data Audit")
    
    data_berat_per_jenis = df.groupby('Jenis Plastik')['Berat (gram)'].sum().sort_values(ascending=False)
    total_berat_keseluruhan = data_berat_per_jenis.sum()
    
    jenis_terdominan = data_berat_per_jenis.index[0] if not data_berat_per_jenis.empty else "Tidak Ada Data Plastik"
    berat_terdominan = data_berat_per_jenis.values[0] if not data_berat_per_jenis.empty else 0

    # SIMPAN JENIS DOMINAN KE SESSION STATE
    st.session_state.dominan_jenis = jenis_terdominan

    # Kotak Info dengan Kontras
    st.markdown(f"""
        <div style='background-color:#ffeeba; color:#495057; padding:15px; border-radius:5px; border:1px solid #ffcc00;'>
            <b>Total Sampah Plastik yang Diaudit:</b> {total_berat_keseluruhan:.2f} gram.<br>
            <b>Jenis Paling Dominan:</b> <b>{jenis_terdominan}</b> ({berat_terdominan:.2f} gram).<br>
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
                st.warning("Tidak cukup data plastik untuk membuat Diagram Lingkaran yang berarti.")
    
    # --- FORM SOLUSI ---
    st.subheader("💡 Tahap 3: Merancang Solusi & Laporan Akhir")
    st.markdown(f"""
        Analisis data menunjukkan bahwa **{jenis_terdominan}** adalah masalah terbesar kita. 
        Tuliskan solusi Anda dengan memenuhi kriteria Laporan Aksi yang **SMART**:
    """)
    
    # --- KRITERIA VALIDASI MANDIRI ---
    st.markdown("#### ✅ Checklist Kriteria Laporan Aksi (Wajib Centang)")
    
    st.checkbox("1. Solusi sudah fokus/spesifik pada **Jenis Sampah Dominan** (Contoh: Botol PET). (SMART: Specific)", key='kriteria_1')
    st.checkbox("2. Solusi memiliki **Target yang Jelas** dan **Terukur** (Contoh: Mengurangi 50% sampah ini dalam 1 bulan). (SMART: Measurable & Realistic)", key='kriteria_2')
    
    st.markdown("#### 📝 Detail Rencana Aksi (Tuliskan Minimal 5 Poin Aksi Nyata)")
    
    # Input Solusi
    st.text_area(
        "Tuliskan Rencana Aksi/Solusi Utama Anda di sini:",
        placeholder='Contoh:\n1. Mengajukan surat resmi ke Kantin untuk mengganti wadah Styrofoam dengan wadah reusable.\n2. Melakukan kampanye edukasi setiap hari Senin di lapangan sekolah tentang bahaya bungkus snack.\n3. Memasang 5 papan informasi di lokasi Hotspot.\n4. Membentuk Tim Patroli Sampah.\n5. Mengadakan kompetisi desain tumbler antar kelas.',
        key='solusi_area' 
    )

    # Tombol Submit.
    st.button(
        "Selesaikan Laporan & Dapatkan Apresiasi!", 
        key="submit_solusi_btn",
        on_click=submit_report_callback
    )


# --- 3. PROGRAM UTAMA APLIKASI WEB (MAIN) ---

def main():
    st.title("🗑️ Data Driven Trash Tracker: Misi Mikroplastik Sekolah") 
    st.header("Selamat Datang, Detektif Lingkungan!")

    # Kutipan yang Di-Highlight
    st.markdown("""
        <div style='background-color:#E8F5E9; border-left: 5px solid #4CAF50; padding: 10px 15px; margin: 15px 0; border-radius: 4px;'>
            <p style='font-style: italic; font-size: 1.1em; color: #1B5E20;'>
                "Kita tidak mewarisi bumi dari leluhur kita; kita meminjamnya dari anak cucu kita."
                <br>
                <small>— Pepatah Suku Indian</small>
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("❓ Klik untuk memahami Tujuan Proyek"):
        st.markdown("""
            Proyek ini adalah investigasi ilmiah untuk mengungkap jejak sampah plastik di lingkungan sekolah.
            Tujuan: <b>Menganalisis</b> data, <b>Memahami</b> sumber masalah, dan <b>Bertindak</b> merancang solusi!
        """, unsafe_allow_html=True)

    # Input Nama Siswa (Tahap Awal)
    nama_siswa = st.text_input("📝 Masukkan Nama Anda / Nama Kelompok:", key="nama_input_unique")

    st.header("📥 Tahap 1: Unggah Data Audit Sampah")
    st.markdown("Unggah file Excel (`.xlsx`) hasil audit sampah Anda.")

    # File Uploader Streamlit
    uploaded_file = st.file_uploader("Pilih file Excel (data_sampah.xlsx):", type=['xlsx'])
    
    # LOGIKA PENTING: Proses Upload dan Penyimpanan ke Session State
    if uploaded_file is not None and nama_siswa:
        try:
            df = pd.read_excel(uploaded_file)
            
            kolom_wajib = ['Tanggal', 'Jenis Plastik', 'Berat (gram)', 'Sumber (Kantin/Kelas)']
            if not all(col in df.columns for col in kolom_wajib):
                st.error("⚠️ Error: Kolom Excel tidak sesuai! Pastikan kolomnya adalah: Tanggal, Jenis Plastik, Berat (gram), Sumber (Kantin/Kelas).")
                st.session_state.uploaded_df = None
                return

            st.success(f"✅ Data berhasil diunggah! Halo, **{nama_siswa}**.")
            st.dataframe(df.head())
            
            # SIMPAN DF DAN NAMA KE SESSION STATE
            st.session_state.uploaded_df = df
            st.session_state.current_nama_siswa = nama_siswa
            
            # PENTING: Jika file baru diupload, analisis harus diulang
            if st.session_state.analisis_run:
                st.session_state.analisis_run = False
            
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses file: Pastikan formatnya .xlsx yang valid. Error: {e}")
            st.session_state.uploaded_df = None

    # LOGIKA TOMBOL RUN ANALISIS (PERBAIKAN KUNCI DI SINI)
    if st.session_state.uploaded_df is not None and st.session_state.current_nama_siswa:
        # Tampilkan tombol hanya jika analisis belum berjalan atau sudah ada data baru
        if not st.session_state.analisis_run:
            if st.button("🚀 Run Analisis Data (Tahap 2 & 3)", key="run_analisis_btn"):
                st.session_state.analisis_run = True
                
                # Reset output dan form solusi
                st.session_state.report_submitted = False
                st.session_state.kriteria_1 = False
                st.session_state.kriteria_2 = False
                st.session_state.solusi_area = ""
                
                st.rerun() # Memastikan reran segera terjadi untuk menampilkan analisis

        # Tampilkan hasil analisis jika analisis_run sudah True (setelah tombol diklik)
        if st.session_state.analisis_run:
            st.markdown("---")
            run_analisis(st.session_state.uploaded_df, st.session_state.current_nama_siswa)

    # Tampilkan laporan jika sudah disubmit
    if st.session_state.report_submitted:
        display_final_report()


if __name__ == "__main__":
    main()
