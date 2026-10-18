import flet as ft
import traceback
from app.logic import CalculatorLogic
from app.ui import CalculatorUI

def main(page: ft.Page):
    try:
        page.title = "CALCULATE"
        page.bgcolor = "#0B0F19" # Warna background gelap layar utama
        
        calc_logic = CalculatorLogic()
        
        def handle_button_click(label):
            try:
                calc_logic.process_input(label) 
                exp, res = calc_logic.get_display()
                calc_ui.update_display(exp, res)
                page.update()
            except Exception as e:
                page.add(ft.Text(f"Error Hitung:\n{traceback.format_exc()}", color="red"))
                page.update()

        calc_ui = CalculatorUI(on_button_press=handle_button_click)
        
        page.add(calc_ui.build_view())
        page.update()

    except Exception as e:
        error_trace = traceback.format_exc()
        page.scroll = "auto"
        page.add(ft.Text(f"Error Fatal di Flet:\n\n{error_trace}", color="red"))
        page.update()

if __name__ == "__main__":
    ft.app(target=main)