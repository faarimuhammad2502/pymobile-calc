"""
=============================================================================
BERKAS: main.py
=============================================================================
"""
import flet as ft
import math
from app.ui import CalculatorUI

def main(page: ft.Page):
    page.title = "PyMobile Calc"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0B0F19"
    page.padding = 16
    page.window.width = 412
    page.window.height = 780

    state = {"expression": "", "is_evaluated": False}

    def handle_button_press(label: str):
        if label == "C":
            state["expression"] = ""
            calc_ui.update_display("", "0")
        elif label == "DEL":
            if not state["is_evaluated"]:
                state["expression"] = state["expression"][:-1]
                calc_ui.update_display("", state["expression"] or "0")
        elif label == "=":
            if not state["expression"]: return
            expr = state["expression"]
            
            py_expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**")
            py_expr = py_expr.replace("π", str(math.pi))
            py_expr = py_expr.replace("sin(", "math.sin(math.radians(")
            py_expr = py_expr.replace("cos(", "math.cos(math.radians(")
            py_expr = py_expr.replace("tan(", "math.tan(math.radians(")
            py_expr = py_expr.replace("log(", "math.log10(")
            py_expr = py_expr.replace("√(", "math.sqrt(")
            
            py_expr += ")" * (py_expr.count("(") - py_expr.count(")"))

            try:
                # Perbaikan Otak Mesin: Menyuntikkan library 'math' agar sin, cos, dll dikenali
                res = eval(py_expr, {"__builtins__": {}, "math": math})
                
                if isinstance(res, float):
                    res = int(res) if res.is_integer() else round(res, 8)
                
                res_str = str(res)
                calc_ui.update_display(expr + " =", res_str)
                calc_ui.add_history_item(expr, res_str)
                
                state["expression"] = res_str
                state["is_evaluated"] = True
            except Exception:
                calc_ui.update_display(expr, "Error")
                state["expression"] = ""
        elif label == "+/-":
            if state["expression"].startswith("-"):
                state["expression"] = state["expression"][1:]
            else:
                state["expression"] = "-" + state["expression"]
            calc_ui.update_display("", state["expression"] or "0")
        elif label == "%":
            try:
                res = str(float(state["expression"]) / 100)
                state["expression"] = res
                calc_ui.update_display("", res)
            except: pass
        elif label in ["sin", "cos", "tan", "log", "√"]:
            if state["is_evaluated"]: state["expression"] = ""
            state["expression"] += f"{label}("
            state["is_evaluated"] = False
            calc_ui.update_display("", state["expression"])
        else:
            if state["is_evaluated"] and label.isdigit():
                state["expression"] = ""
            state["is_evaluated"] = False
            state["expression"] += label
            calc_ui.update_display("", state["expression"])
            
        page.update()

    calc_ui = CalculatorUI(on_button_press=handle_button_press)
    page.add(ft.Container(content=calc_ui.build_view(), alignment=ft.alignment.center))

if __name__ == "__main__":
    ft.app(target=main)