import streamlit as st
import requests

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
        border-radius: 10px;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

class AIAssistant:
    def __init__(self):
        self.api_key = st.secrets.get("OPENAI_API_KEY", "")
    
    def get_ai_response(self, prompt, max_tokens=1000):
        """Get response from OpenAI API"""
        if not self.api_key or self.api_key.startswith("sk-your-actual"):
            return self._get_fallback_response(prompt)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions", 
                headers=headers, 
                json=data, 
                timeout=30
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            st.error(f"❌ Error AI: {str(e)}")
            return self._get_fallback_response(prompt)
    
    def _get_fallback_response(self, prompt):
        """Fallback response jika API error"""
        return """
**IDENTIFIKASI MURID (Simulasi - API Key belum diatur)**

📚 **Pengetahuan Awal:**
- Pemahaman dasar tentang konsep terkait
- Variasi tingkat penguasaan materi prasyarat

🎯 **Minat Belajar:**
- Antusiasme tinggi pada pembelajaran berbasis proyek
- Ketertarikan pada teknologi dan aplikasi praktis

🔧 **Kebutuhan Individual:**
- Akses materi tambahan untuk pemula
- Tantangan ekstra untuk siswa yang cepat

*Untuk fitur AI penuh, silakan setup OpenAI API Key di Streamlit secrets.*
        """

def setup_sidebar():
    """Setup sidebar dengan form input"""
    with st.sidebar:
        st.markdown("### 📋 Informasi Dasar")
        
        with st.form("basic_info"):
            st.subheader("Data Guru & Sekolah")
            nama_guru = st.text_input("Nama Guru*", placeholder="Budi Santoso, S.Pd")
            nip = st.text_input("NIP*", placeholder="198304122006041002")
            sekolah = st.selectbox("Sekolah*", ["SMK", "SMA", "MAN", "SMK Plus"])
            
            st.subheader("Data Pembelajaran")
            tahun_pelajaran = st.text_input("Tahun Pelajaran*", "2025/2026")
            semester = st.selectbox("Semester*", ["1", "2"])
            mata_pelajaran = st.text_input("Mata Pelajaran*", placeholder="Pemrograman Web dan Perangkat Bergerak")
            kelas_fase = st.text_input("Kelas / Fase Capaian*", placeholder="X RPL / D")
            topik_elemen = st.text_input("Topik / Elemen*", placeholder="HTML, CSS, JavaScript / Dasar Pemrograman Web")
            alokasi_waktu = st.text_input("Alokasi Waktu*", placeholder="8 x 45 Menit")
            tujuan_pembelajaran = st.text_area(
                "Tujuan Pembelajaran*", 
                placeholder="Siswa mampu membuat website responsive menggunakan HTML, CSS, dan JavaScript dasar",
                height=80
            )
            
            submitted = st.form_submit_button("💾 Simpan Data Dasar", type="primary", use_container_width=True)
            
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
                        'tujuan_pembelajaran': tujuan_pembelajaran
                    }
                    st.success("✅ Data berhasil disimpan!")
                else:
                    st.error("❌ Harap isi semua field yang wajib (*)")
        
        st.markdown("---")
        st.markdown("### 🔧 Status AI")
        
        # Check API key status
        if 'OPENAI_API_KEY' in st.secrets:
            if st.secrets.OPENAI_API_KEY.startswith("sk-your-actual"):
                st.warning("⚠️ API Key belum dikonfigurasi")
                st.info("""
                **Setup API Key:**
                1. Buka [OpenAI](https://platform.openai.com/api-keys)
                2. Buat API Key
                3. Tambahkan di Streamlit Secrets:
                ```
                OPENAI_API_KEY = "sk-..."
                ```
                """)
            else:
                st.success("✅ API Key terdeteksi")
        else:
            st.warning("⚠️ API Key belum diatur")

def display_basic_info():
    """Display informasi dasar"""
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
            <strong>⏰ Alokasi Waktu:</strong> {data['alokasi_waktu']}
            </div>
            """, unsafe_allow_html=True)
        
        # Tujuan Pembelajaran
        st.markdown(f"""
        <div class="info-box">
        <strong>🎯 Tujuan Pembelajaran:</strong><br>
        {data['tujuan_pembelajaran']}
        </div>
        """, unsafe_allow_html=True)
        
        return True
    else:
        st.info("ℹ️ Silakan isi form di sidebar terlebih dahulu")
        return False

def generate_ai_content():
    """Generate konten dengan AI"""
    st.markdown('<div class="section-header">🔍 GENERATE DENGAN AI</div>', unsafe_allow_html=True)
    
    ai = AIAssistant()
    
    tab1, tab2, tab3 = st.tabs(["🤖 Identifikasi Murid", "📚 Materi Pelajaran", "🌟 Profil Lulusan"])
    
    with tab1:
        if st.button("🔄 Generate Identifikasi Murid", key="btn_ident", use_container_width=True):
            with st.spinner("AI menganalisis karakteristik murid..."):
                prompt = f"""
                Buatkan identifikasi murid berdasarkan tujuan pembelajaran: "{st.session_state.basic_info['tujuan_pembelajaran']}"
                
                Analisis dalam 3 aspek:
                1. Pengetahuan Awal - kondisi pemahaman dasar siswa
                2. Minat Belajar - motivasi dan ketertarikan 
                3. Kebutuhan Individual - penyesuaian yang diperlukan
                
                Format: daftar poin, bahasa Indonesia formal.
                Maksimal 6 poin per aspek.
                """
                response = ai.get_ai_response(prompt)
                st.session_state.identifikasi_murid = response
            
        if 'identifikasi_murid' in st.session_state:
            st.markdown(st.session_state.identifikasi_murid)
    
    with tab2:
        if st.button("🔄 Generate Materi Pelajaran", key="btn_materi", use_container_width=True):
            with st.spinner("AI menyusun materi pembelajaran..."):
                prompt = f"""
                Rancang materi pelajaran untuk: "{st.session_state.basic_info['tujuan_pembelajaran']}"
                
                Struktur dalam 4 kategori:
                1. Pengetahuan Faktual - fakta, data, informasi dasar
                2. Pengetahuan Konseptual - prinsip, teori, model
                3. Pengetahuan Prosedural - langkah-langkah, metode
                4. Pengetahuan Metakognitif - strategi belajar
                
                Format: daftar poin, relevan dengan kehidupan nyata.
                Bahasa Indonesia formal.
                """
                response = ai.get_ai_response(prompt)
                st.session_state.materi_pelajaran = response
            
        if 'materi_pelajaran' in st.session_state:
            st.markdown(st.session_state.materi_pelajaran)
    
    with tab3:
        if st.button("🔄 Generate Profil Lulusan", key="btn_profil", use_container_width=True):
            with st.spinner("AI merekomendasikan dimensi profil..."):
                prompt = f"""
                Rekomendasikan 3 Dimensi Profil Lulusan untuk: "{st.session_state.basic_info['tujuan_pembelajaran']}"
                
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
                
                Bahasa Indonesia formal.
                """
                response = ai.get_ai_response(prompt)
                st.session_state.dimensi_profil = response
            
        if 'dimensi_profil' in st.session_state:
            st.markdown(st.session_state.dimensi_profil)

def show_export_options():
    """Tampilkan opsi export"""
    st.markdown('<div class="section-header">📤 EKSPOR & RESET</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🖨️ Print Document", use_container_width=True):
            st.info("""
            **Untuk print dokumen:**
            - Gunakan **Ctrl+P** (Windows) atau **Cmd+P** (Mac)
            - Pilih destination "Save as PDF" untuk export ke PDF
            - Atau print langsung ke printer
            - Pilih layout "Landscape" untuk hasil terbaik
            """)
    
    with col2:
        if st.button("🔄 Reset Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ Session berhasil direset!")
            st.rerun()

def main():
    """Main application"""
    setup_sidebar()
    
    if display_basic_info():
        generate_ai_content()
        show_export_options()

if __name__ == "__main__":
    main()