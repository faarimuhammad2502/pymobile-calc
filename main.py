import flet as ft
import traceback

try:
    # Mengambil komponen kalkulator Anda
    from app.logic import CalculatorLogic
    from app.ui import CalculatorUI

    def main(page: ft.Page):
        page.title = "CALCULATE"
        
        # Mengaktifkan logika dan tampilan kalkulator
        calc_logic = CalculatorLogic()
        calc_ui = CalculatorUI(page, calc_logic)
        
        # Memasukkan kalkulator ke layar HP
        page.add(calc_ui)
        page.update()

except Exception as e:
    # Perangkap error: Munculkan teks merah jika gagal
    error_trace = traceback.format_exc()
    
    def main(page: ft.Page):
        page.scroll = "auto"
        page.add(ft.Text(f"Error Fatal di Awal Aplikasi:\n\n{error_trace}", color="red"))
        page.update()

if __name__ == "__main__":
    ft.app(target=main)