import streamlit as st
import pandas as pd
from datetime import datetime
from utils.ai_helper import AIAssistant
from utils.pdf_generator import PDFGenerator
import base64

# Page configuration
st.set_page_config(
    page_title="AI Learning Planner",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.4rem;
        color: #2e86ab;
        border-bottom: 2px solid #2e86ab;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2e86ab;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #f0fff4;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #38a169;
        margin: 1rem 0;
    }
    .stButton button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class LearningPlannerApp:
    def __init__(self):
        self.ai = AIAssistant()
        self.pdf_gen = PDFGenerator()
        
    def setup_sidebar(self):
        """Setup sidebar with input forms"""
        with st.sidebar:
            st.markdown("### 📋 Informasi Dasar")
            
            with st.form("basic_info"):
                st.subheader("Data Guru & Sekolah")
                nama_guru = st.text_input("Nama Guru*", placeholder="Budi Santoso, S.Pd")
                nip = st.text_input("NIP*", placeholder="198304122006041002")
                sekolah = st.selectbox("Sekolah*", ["SMK", "SMA", "MAN", "SMK Plus", "Lainnya"])
                if sekolah == "Lainnya":
                    sekolah = st.text_input("Nama Sekolah")
                
                st.subheader("Data Pembelajaran")
                tahun_pelajaran = st.text_input("Tahun Pelajaran*", "2025/2026")
                semester = st.selectbox("Semester*", ["1", "2"])
                mata_pelajaran = st.text_input("Mata Pelajaran*", placeholder="Pemrograman Web dan Perangkat Bergerak")
                kelas_fase = st.text_input("Kelas / Fase Capaian*", placeholder="X RPL / D")
                topik_elemen = st.text_input("Topik / Elemen*", placeholder="HTML, CSS, JavaScript / Dasar Pemrograman Web")
                alokasi_waktu = st.text_input("Alokasi Waktu*", placeholder="8 x 45 Menit")
                tujuan_pembelajaran = st.text_area("Tujuan Pembelajaran*", 
                                                 placeholder="Siswa mampu membuat website responsive menggunakan HTML, CSS, dan JavaScript dasar",
                                                 height=100)
                capaian_pembelajaran = st.text_area("Capaian Pembelajaran",
                                                  placeholder="Di akhir fase D, peserta didik dapat mengembangkan website statis dengan layout responsive...",
                                                  height=80)
                
                submitted = st.form_submit_button("💾 Simpan Data Dasar", type="primary")
                
                if submitted:
                    # Validasi input
                    required_fields = [nama_guru, nip, mata_pelajaran, kelas_fase, topik_elemen, alokasi_waktu, tujuan_pembelajaran]
                    if all(required_fields):
                        st.session_state.basic_info = {
                            'nama_guru': nama_guru,
                            'nip': nip,
                            'sekolah': sekolah,
                            'tahun_pelajaran': tahun_pelajaran,
                            'semester': semester,
                            'mata_pelajaran': mata_pelajaran,
                            'kelas_fase': kelas_fase,
                            'topik_elemen': topik_elemen,
                            'alokasi_waktu': alokasi_waktu,
                            'tujuan_pembelajaran': tujuan_pembelajaran,
                            'capaian_pembelajaran': capaian_pembelajaran
                        }
                        st.success("✅ Data berhasil disimpan!")
                    else:
                        st.error("❌ Harap isi semua field yang wajib (*)")
            
            st.markdown("---")
            st.markdown("### 🔧 AI Settings")
            st.info("Pastikan API key OpenAI sudah diatur di `.streamlit/secrets.toml`")
            
            if 'OPENAI_API_KEY' in st.secrets and st.secrets.OPENAI_API_KEY != "sk-your-actual-openai-api-key-here":
                st.success("✅ API Key terdeteksi")
            else:
                st.warning("⚠️ API Key belum diatur")

    def display_basic_info(self):
        """Display basic information section"""
        if 'basic_info' in st.session_state:
            data = st.session_state.basic_info
            
            st.markdown('<div class="main-header">🎓 RENCANA PELAKSANAAN PEMBELAJARAN (RPP)</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="info-box">
                <strong>👨‍🏫 Nama Guru:</strong> {data['nama_guru']}<br>
                <strong>🔢 NIP:</strong> {data['nip']}<br>
                <strong>🏫 Sekolah:</strong> {data['sekolah']}<br>
                <strong>📅 Tahun Pelajaran:</strong> {data['tahun_pelajaran']}<br>
                <strong>📚 Semester:</strong> {data['semester']}
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="info-box">
                <strong>📖 Mata Pelajaran:</strong> {data['mata_pelajaran']}<br>
                <strong>🎯 Kelas / Fase Capaian:</strong> {data['kelas_fase']}<br>
                <strong>🔍 Topik / Elemen:</strong> {data['topik_elemen']}<br>
                <strong>⏰ Alokasi Waktu:</strong> {data['alokasi_waktu']}<br>
                <strong>🎯 Tujuan Pembelajaran:</strong> {data['tujuan_pembelajaran']}
                </div>
                """, unsafe_allow_html=True)
            
            return True
        else:
            st.info("ℹ️ Silakan isi form di sidebar terlebih dahulu")
            return False

    def generate_identifikasi_section(self):
        """Generate identification section with AI"""
        st.markdown('<div class="section-header">🔍 TABEL IDENTIFIKASI</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["A. Identifikasi Murid", "B. Materi Pelajaran", "C. Dimensi Profil Lulusan"])
        
        with tab1:
            if st.button("🤖 Generate Identifikasi Murid", key="btn_identifikasi"):
                with st.spinner("AI menganalisis identifikasi murid..."):
                    prompt = f"""
                    Buatkan identifikasi murid berdasarkan tujuan pembelajaran: "{st.session_state.basic_info['tujuan_pembelajaran']}"
                    
                    Analisis dalam 3 aspek:
                    1. Pengetahuan Awal - kondisi pemahaman dasar siswa
                    2. Minat Belajar - motivasi dan ketertarikan 
                    3. Kebutuhan Individual - penyesuaian yang diperlukan
                    
                    Format: daftar poin, maksimal 6 poin per aspek.
                    Gunakan bahasa Indonesia yang formal.
                    """
                    response = self.ai.get_ai_response(prompt)
                    st.session_state.identifikasi_murid = response
                
                if 'identifikasi_murid' in st.session_state:
                    st.markdown(st.session_state.identifikasi_murid)
        
        with tab2:
            if st.button("📚 Generate Materi Pelajaran", key="btn_materi"):
                with st.spinner("AI menyusun materi pelajaran..."):
                    prompt = f"""
                    Rancang materi pelajaran berdasarkan tujuan pembelajaran: "{st.session_state.basic_info['tujuan_pembelajaran']}"
                    
                    Struktur materi dalam 4 kategori:
                    1. Pengetahuan Faktual - fakta, data, informasi dasar
                    2. Pengetahuan Konseptual - prinsip, teori, model
                    3. Pengetahuan Prosedural - langkah-langkah, metode
                    4. Pengetahuan Metakognitif - strategi belajar
                    
                    Format: daftar poin, relevan dengan kehidupan nyata.
                    Gunakan bahasa Indonesia yang formal.
                    """
                    response = self.ai.get_ai_response(prompt)
                    st.session_state.materi_pelajaran = response
                
                if 'materi_pelajaran' in st.session_state:
                    st.markdown(st.session_state.materi_pelajaran)
        
        with tab3:
            if st.button("🌟 Generate Dimensi Profil", key="btn_dimensi"):
                with st.spinner("AI merekomendasikan dimensi profil..."):
                    prompt = f"""
                    Rekomendasikan 3 Dimensi Profil Lulusan untuk tujuan pembelajaran: "{st.session_state.basic_info['tujuan_pembelajaran']}"
                    
                    Pilihan dimensi: 
                    - keimanan dan ketakwaan
                    - kewargaan 
                    - penalaran kritis
                    - kreativitas
                    - kolaborasi
                    - kemandirian
                    - kesehatan
                    - komunikasi
                    
                    Format setiap rekomendasi:
                    - **Nama Dimensi** (tebal)
                    - Alasan kesesuaian (2-3 kalimat)
                    - Keterkaitan dengan kompetensi
                    
                    Gunakan bahasa Indonesia yang formal.
                    """
                    response = self.ai.get_ai_response(prompt)
                    st.session_state.dimensi_profil = response
                
                if 'dimensi_profil' in st.session_state:
                    st.markdown(st.session_state.dimensi_profil)

    def export_section(self):
        """Export and download section"""
        st.markdown('<div class="section-header">📤 EXPORT DOKUMEN</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Export ke PDF", use_container_width=True):
                if 'basic_info' in st.session_state:
                    pdf_data = self.pdf_gen.generate_rpp_pdf(st.session_state.basic_info)
                    if pdf_data:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_data,
                            file_name=f"RPP_{st.session_state.basic_info['mata_pelajaran']}_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    st.error("❌ Tidak ada data untuk di-export")
        
        with col2:
            if st.button("🖨️ Print Document", use_container_width=True):
                st.info("🖨️ Gunakan print browser (Ctrl+P) untuk mencetak halaman ini")
        
        with col3:
            if st.button("🔄 Reset Session", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    def run(self):
        """Main application runner"""
        self.setup_sidebar()
        
        if self.display_basic_info():
            self.generate_identifikasi_section()
            self.export_section()

# Run the app
if __name__ == "__main__":
    app = LearningPlannerApp()
    app.run()