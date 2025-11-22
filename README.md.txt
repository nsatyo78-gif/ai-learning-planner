# 🎓 AI Learning Planner

Aplikasi perencanaan pembelajaran berbasis AI untuk membantu guru membuat RPP (Rencana Pelaksanaan Pembelajaran) dengan mudah dan cepat.

## ✨ Fitur

- 📋 Form input data RPP lengkap
- 🤖 Integrasi AI untuk generate konten
- 🎯 Identifikasi murid berdasarkan tujuan pembelajaran
- 📚 Penyusunan materi pelajaran
- 🌟 Rekomendasi dimensi profil lulusan
- 🖨️ Export dan print document

## 🚀 Cara Deploy

### 1. Upload ke GitHub
- Buat repository baru di GitHub
- Upload semua file ke repository
- Pastikan file utama bernama `streamlit_app.py`

### 2. Deploy ke Streamlit
- Buka [share.streamlit.io](https://share.streamlit.io)
- Login dengan GitHub
- Pilih repository dan branch
- Main file path: `streamlit_app.py`
- Klik "Deploy"

### 3. Setup API Key
- Dapatkan API Key dari [OpenAI](https://platform.openai.com/api-keys)
- Di Streamlit app, buka Settings → Secrets
- Tambahkan:
```toml
OPENAI_API_KEY = "sk-..."