import requests
import streamlit as st
import json

class AIAssistant:
    def __init__(self):
        self.api_key = st.secrets.get("OPENAI_API_KEY", "")
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    def get_ai_response(self, prompt, max_tokens=1500):
        """Get response from OpenAI API"""
        if not self.api_key or self.api_key == "sk-your-actual-openai-api-key-here":
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
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            st.error(f"❌ Error AI: {str(e)}")
            return self._get_fallback_response(prompt)
    
    def _get_fallback_response(self, prompt):
        """Fallback response jika API error atau tidak ada key"""
        fallback_responses = {
            "identifikasi murid": """
**IDENTIFIKASI MURID (Simulasi):**

📚 **Pengetahuan Awal:**
- Pemahaman dasar tentang konsep terkait
- Variasi tingkat penguasaan materi prasyarat  
- Pengalaman praktik sebelumnya

🎯 **Minat Belajar:**
- Antusiasme tinggi pada pembelajaran berbasis proyek
- Ketertarikan pada teknologi dan aplikasi praktis
- Preferensi terhadap pembelajaran visual dan hands-on

🔧 **Kebutuhan Individual:**
- Akses materi tambahan untuk pemula
- Tantangan ekstra untuk siswa yang cepat
- Pendekatan multimodal (visual, auditory, kinestetik)
- Dukungan teknis dan scaffolding
            """,
            "materi pelajaran": """
**MATERI PEMBELAJARAN (Simulasi):**

📖 **Pengetahuan Faktual:**
- Definisi dan terminologi kunci
- Data dan informasi dasar yang relevan
- Contoh-contoh konkret dari kehidupan sehari-hari

🧠 **Pengetahuan Konseptual:**
- Prinsip-prinsip fundamental
- Hubungan antar konsep
- Model dan teori pendukung

🛠️ **Pengetahuan Prosedural:**
- Langkah-langkah praktis implementasi
- Teknik dan metode aplikasi
- Proses troubleshooting dan problem-solving

💡 **Pengetahuan Metakognitif:**
- Strategi pembelajaran efektif
- Teknik evaluasi diri
- Perencanaan pengembangan kompetensi berkelanjutan
            """,
            "dimensi profil": """
**DIMENSI PROFIL LULUSAN (Simulasi):**

1. **PENALARAN KRITIS**
   - **Alasan:** Membantu siswa menganalisis informasi, mengevaluasi bukti, dan mengambil keputusan berdasarkan logika

2. **KOLABORASI** 
   - **Alasan:** Mengembangkan kemampuan kerja sama tim, komunikasi efektif, dan sinergi dalam menyelesaikan proyek

3. **KREATIVITAS**
   - **Alasan:** Mendorong inovasi dan pemecahan masalah dengan pendekatan out-of-the-box
            """
        }
        
        # Cari keyword dalam prompt untuk memberikan response yang relevan
        prompt_lower = prompt.lower()
        for key in fallback_responses:
            if key in prompt_lower:
                return fallback_responses[key]
        
        return "**Response simulasi:** Fitur AI akan aktif setelah setup API key OpenAI. Silakan tambahkan API key Anda di file secrets.toml"