import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import io

# --- 0. KONFIGURASI DAN FUNGSI UTAMA ---

# Konfigurasi Streamlit (Header, Layout, dll.)
st.set_page_config(
    page_title="Data Driven Trash Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi Session State
if 'report_submitted' not in st.session_state:
    st.session_state.report_submitted = False
if 'final_solusi' not in st.session_state:
    st.session_state.final_solusi = ""
if 'final_jenis' not in st.session_state:
    st.session_state.final_jenis = ""
if 'final_nama' not in st.session_state:
    st.session_state.final_nama = ""

def generate_feedback(jenis_dominan_str):
    fakta, rekomendasi, img_query = "", "", ""

    if "Botol PET" in jenis_dominan_str:
        fakta = "Fakta Mengkhawatirkan: Botol PET membutuhkan waktu sekitar 450 tahun untuk terurai. Sebagian besar botol hanya digunakan sekali!"
        rekomendasi = "Rekomendasi Penanganan: Wajibkan penggunaan botol minum (tumbler) isi ulang di seluruh area sekolah (guru dan siswa)."
        img_query = "Reusable water bottle vs single use plastic bottle"
    elif "Bungkus Snack" in jenis_dominan_str or "Plastik Film" in jenis_dominan_str:
        fakta = "Fakta Mengkhawatirkan: Bungkus berlapis (multilayer) seperti bungkus snack hampir tidak mungkin didaur ulang di Indonesia dan langsung menjadi residu."
        rekomendasi = "Rekomendasi Penanganan: Dorong siswa membawa bekal makanan ringan dari rumah dalam wadah yang dapat dipakai ulang (tupperware)."
        img_query = "Multilayer plastic packaging"
    elif "Sedotan" in jenis_dominan_str:
        fakta = "Fakta Mengkhawatirkan: Meskipun ringan, jutaan sedotan digunakan setiap hari. Karena ukurannya, sedotan adalah penyumbang mikroplastik di laut yang berbahaya bagi biota."
        rekomendasi = "Rekomendasi Penanganan: Larang penyediaan sedotan plastik di kantin dan ganti dengan sedotan kertas atau tidak sama sekali."
        img_query = "Microplastic pollution in ocean"
    else: 
        fakta = "Fakta Mengkhawatirkan: Setiap tahun, jutaan ton plastik berakhir di TPA dan mencemari lingkungan. Perubahan dimulai dari kesadaran kita!"
        rekomendasi = "Rekomendasi Penanganan: Adakan pelatihan pemilahan sampah yang ketat (organik vs non-organik) untuk meningkatkan efektivitas daur ulang di sekolah."
        img_query = "Global plastic waste problem"
        
    kata_mutiara = [
        "Bumi adalah rumah kita, mari jaga ia dengan aksi nyata, bukan hanya kata-kata.",
        "Sampah adalah cerminan peradaban. Mari tunjukkan bahwa peradaban kita bersih dan bijaksana.",
        "Kita tidak mewarisi bumi dari leluhur kita; kita meminjamnya dari anak cucu kita.",
        "Masa depan hijau hijau dimulai dengan keputusan kecil hari ini."
    ]
    
    return fakta, rekomendasi, random.choice(kata_mutiara), img_query

def submit_report_callback(jenis_terdominan, nama_siswa):
    """Callback function yang dipanggil saat tombol submit diklik."""
    # Ambil nilai dari Session State sebelum state diubah
    solusi_input = st.session_state.solusi_area
    
    if not solusi_input:
        st.error("Mohon masukkan ide solusi Anda terlebih dahulu.")
        st.session_state.report_submitted = False
        return
        
    # Simpan hasil akhir ke Session State
    st.session_state.report_submitted = True
    st.session_state.final_solusi = solusi_input
    st.session_state.final_jenis = jenis_terdominan
    st.session_state.final_nama = nama_siswa
    # Streamlit akan me-rerun, dan output akan ditampilkan di luar fungsi callback

def display_final_report():
    """Menampilkan laporan akhir dari Session State."""
    nama = st.session_state.final_nama
    solusi = st.session_state.final_solusi
    jenis = st.session_state.final_jenis
    
    if not jenis or not nama or not solusi:
        return # Jangan tampilkan jika data belum lengkap

    fakta, rekomendasi, kata_mutiara_pilihan, img_query = generate_feedback(jenis)

    # Output Apresiasi Streamlit
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
            <p style='font-weight: bold; color:#dc3545;'>🚨 {fakta}</p>
            <p><b>Langkah Rekomendasi:</b> {rekomendasi}</p>
            <hr>
            <p style='font-style: italic;'>"{kata_mutiara_pilihan}"</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Visualisasi Dampak dan Solusi ({jenis}):**")
    # Ganti dengan URL gambar realistik
    st.image("https://via.placeholder.com/800x300.png?text=Contoh+Dampak+atau+Solusi+untuk+" + jenis.replace(" ", "+"))


# --- 2. FUNGSI ANALISIS DATA ---

def run_analisis(df, nama_siswa):
    """Menganalisis data, menampilkan visualisasi, dan memunculkan form solusi."""

    st.header("📊 Tahap 2: Hasil Analisis Data Audit")
    
    data_berat_per_jenis = df.groupby('Jenis Plastik')['Berat (gram)'].sum().sort_values(ascending=False)
    total_berat_keseluruhan = data_berat_per_jenis.sum()
    
    jenis_terdominan = data_berat_per_jenis.index[0] if not data_berat_per_jenis.empty else "Tidak Ada Data Plastik"
    berat_terdominan = data_berat_per_jenis.values[0] if not data_berat_per_jenis.empty else 0


    st.info(f"""
        **Total Sampah Plastik yang Diaudit:** {total_berat_keseluruhan:.2f} gram.
        **Jenis Paling Dominan:** **{jenis_terdominan}** ({berat_terdominan:.2f} gram).
        Fokus solusi kita harus ada pada jenis ini!
    """)
    
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
        Tuliskan solusi Anda di bawah ini!
    """)
    
    # Input Solusi
    st.text_area(
        "Tuliskan Rencana Aksi/Solusi Utama Anda di sini:",
        placeholder='Contoh: Kampanye Stop Botol Sekali Pakai...',
        key='solusi_area' 
    )

    # Tombol Submit dengan callback, memastikan data solusi dan jenis dominan diolah
    st.button(
        "Selesaikan Laporan & Dapatkan Apresiasi!", 
        key="submit_solusi_btn",
        on_click=submit_report_callback,
        args=(jenis_terdominan, nama_siswa)
    )
    
    # Tampilkan laporan jika sudah disubmit
    if st.session_state.report_submitted:
        display_final_report()


# --- 3. PROGRAM UTAMA APLIKASI WEB (MAIN) ---

def main():
    st.title("🗑️ Data Driven Trash Tracker: Misi Mikroplastik Sekolah") 
    st.header("Selamat Datang, Detektif Lingkungan!")

    with st.expander("❓ Klik untuk memahami Tujuan Proyek"):
        st.markdown("""
            Proyek ini adalah investigasi ilmiah untuk mengungkap jejak sampah plastik di lingkungan sekolah.
            Tujuan: <b>Menganalisis</b> data, <b>Memahami</b> sumber masalah, dan <b>Bertindak</b> merancang solusi!
        """, unsafe_allow_html=True)

    # Input Nama Siswa
    nama_siswa = st.text_input("📝 Masukkan Nama Anda / Nama Kelompok:", key="nama_input")

    st.header("📥 Tahap 1: Unggah Data Audit Sampah")
    st.markdown("Unggah file Excel (`.xlsx`) hasil audit sampah Anda.")

    # File Uploader Streamlit
    uploaded_file = st.file_uploader("Pilih file Excel (data_sampah.xlsx):", type=['xlsx'])
    
    if uploaded_file is not None and nama_siswa:
        try:
            df = pd.read_excel(uploaded_file)
            
            kolom_wajib = ['Tanggal', 'Jenis Plastik', 'Berat (gram)', 'Sumber (Kantin/Kelas)']
            if not all(col in df.columns for col in kolom_wajib):
                st.error("⚠️ Error: Kolom Excel tidak sesuai! Pastikan kolomnya adalah: Tanggal, Jenis Plastik, Berat (gram), Sumber (Kantin/Kelas).")
                return

            st.success(f"✅ Data berhasil diunggah! Halo, **{nama_siswa}**.")
            
            # Panggil Analisis
            run_analisis(df, nama_siswa)

        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses file: Pastikan formatnya .xlsx yang valid. Error: {e}")

    elif uploaded_file is None and nama_siswa:
        st.warning("Silakan unggah file Excel Anda untuk memulai analisis.")
    elif uploaded_file is not None and not nama_siswa:
        st.warning("Mohon isi nama Anda/Kelompok di atas terlebih dahulu.")

if __name__ == "__main__":
    main()
