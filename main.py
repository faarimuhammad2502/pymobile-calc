import flet as ft
import traceback
from app.logic import CalculatorLogic
from app.ui import CalculatorUI

def main(page: ft.Page):
    try:
        page.title = "CALCULATE"
        page.bgcolor = "#0B0F19"
        page.padding = 12
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

        calc_logic = CalculatorLogic()

        def handle_button_click(label):
            try:
                calc_logic.process_input(label)
                exp, res = calc_logic.get_display()
                calc_ui.update_display(exp, res)
                calc_ui.update_history_ui(calc_logic.history)
                page.update()
            except Exception as e:
                print("Error:", e)

        def handle_convert(category, from_u, to_u, val_str):
            return calc_logic.convert_units(category, from_u, to_u, val_str)

        def handle_clear_history():
            calc_logic.clear_history()
            calc_ui.update_history_ui(calc_logic.history)
            page.update()

        calc_ui = CalculatorUI(
            on_button_press=handle_button_click,
            on_convert=handle_convert,
            on_clear_history=handle_clear_history
        )

        page.add(calc_ui.build_view())
        page.update()

    except Exception as e:
        error_trace = traceback.format_exc()
        page.scroll = ft.ScrollMode.AUTO
        page.add(ft.Text(f"Error Fatal di Flet:\n\n{error_trace}", color="red"))
        page.update()

if __name__ == "__main__":
    ft.app(target=main)