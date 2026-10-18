import flet as ft
import traceback
from app.logic import CalculatorLogic
from app.ui import CalculatorUI

def main(page: ft.Page):
    # PERANGKAP BENAR: Diletakkan tepat di DALAM fungsi main
    try:
        page.title = "CALCULATE"
        
        # 1. Aktifkan logika kalkulator
        calc_logic = CalculatorLogic()
        
        # 2. Buat fungsi jembatan (agar tombol di UI bisa tersambung ke Logika)
        def handle_button_click(label):
            try:
                # Masukkan input ke logika (Pastikan nama fungsi 'process_input' sesuai dengan yang ada di logic.py Anda)
                calc_logic.process_input(label) 
                
                # Ambil hasil dan update layar
                exp, res = calc_logic.get_display()
                calc_ui.update_display(exp, res)
                page.update()
            except Exception as e:
                # Jika error saat menghitung, munculkan merah di bawah kalkulator
                page.add(ft.Text(f"Error Hitung:\n{traceback.format_exc()}", color="red"))
                page.update()

        # 3. Masukkan fungsi jembatan tadi ke dalam UI
        calc_ui = CalculatorUI(on_button_press=handle_button_click)
        
        # 4. PASANG KE LAYAR (Wajib menggunakan .build_view() !)
        page.add(calc_ui.build_view())
        page.update()

    except Exception as e:
        # Jika UI gagal dibangun, layarnya akan dipenuhi teks merah!
        error_trace = traceback.format_exc()
        page.scroll = "auto"
        page.add(ft.Text(f"Error Fatal di Flet:\n\n{error_trace}", color="red"))
        page.update()

if __name__ == "__main__":
    ft.app(target=main)