import flet as ft
import traceback

# PERANGKAP UTAMA: Kita tangkap error dari sejak file dimuat!
try:
    # Pindahkan import file Anda ke dalam sini
    from app.logic import CalculatorLogic
    from app.ui import CalculatorUI

    def main(page: ft.Page):
        page.title = "CALCULATE"
        
        # --- MASUKKAN KODE KALKULATOR ASLI ANDA DI BAWAH SINI ---
        # (Pastikan spasinya menjorok ke dalam sejajar dengan tulisan ini)
        
        
        
        # --------------------------------------------------------
        page.update()

except Exception as e:
    # Jika error terjadi saat import atau di luar fungsi main, 
    # tangkap dan buat fungsi main darurat untuk menampilkannya:
    error_trace = traceback.format_exc()
    
    def main(page: ft.Page):
        page.scroll = "auto"
        page.add(ft.Text(f"Error Fatal di Awal Aplikasi:\n\n{error_trace}", color="red"))
        page.update()

if __name__ == "__main__":
    ft.app(target=main)