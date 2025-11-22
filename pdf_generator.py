from fpdf import FPDF
import streamlit as st
from datetime import datetime

class PDFGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
    
    def generate_rpp_pdf(self, data):
        """Generate RPP dalam format PDF"""
        try:
            self.pdf.add_page()
            
            # Header
            self.pdf.set_font("Arial", 'B', 16)
            self.pdf.cell(0, 10, "RENCANA PELAKSANAAN PEMBELAJARAN (RPP)", 0, 1, 'C')
            self.pdf.ln(5)
            
            # Informasi Dasar
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(0, 10, "INFORMASI DASAR", 0, 1)
            self.pdf.set_font("Arial", '', 10)
            
            info_lines = [
                f"Nama Guru: {data.get('nama_guru', '')}",
                f"NIP: {data.get('nip', '')}",
                f"Sekolah: {data.get('sekolah', '')}",
                f"Tahun Pelajaran: {data.get('tahun_pelajaran', '')}",
                f"Semester: {data.get('semester', '')}",
                f"Mata Pelajaran: {data.get('mata_pelajaran', '')}",
                f"Kelas/Fase: {data.get('kelas_fase', '')}",
                f"Topik/Elemen: {data.get('topik_elemen', '')}",
                f"Alokasi Waktu: {data.get('alokasi_waktu', '')}"
            ]
            
            for line in info_lines:
                self.pdf.cell(0, 6, line, 0, 1)
            
            self.pdf.ln(5)
            
            # Tambahkan konten lainnya sesuai kebutuhan
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(0, 10, "TUJUAN PEMBELAJARAN", 0, 1)
            self.pdf.set_font("Arial", '', 10)
            self.pdf.multi_cell(0, 6, data.get('tujuan_pembelajaran', ''))
            
            return self.pdf.output(dest='S').encode('latin1')
            
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
            return None