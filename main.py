"""
=============================================================================
BERKAS: main.py
PERAN  : Entry Point & Controller
ANALOGI WEB:
- main.py bertindak seperti index.js / App.tsx di React:
  1. Inisialisasi root DOM (page)
  2. Buat instance state/service (CalculatorLogic)
  3. Buat instance tampilan (CalculatorUI)
  4. Hubungkan event tombol ke logika (Event Binding)
  5. Panggil page.update() untuk memicu re-render (mirip React setState)
=============================================================================
"""

import flet as ft
from app.logic import CalculatorLogic
from app.ui import CalculatorUI


def main(page: ft.Page):
    """
    Fungsi utama yang dipanggil oleh Flet runtime.
    
    Analogi Web:
    'page' setara dengan objek 'window' atau 'document.body' di browser.
    """
    # -------------------------------------------------------------------------
    # 1. KONFIGURASI HALAMAN MOBILE (CSS Root & Viewport)
    # -------------------------------------------------------------------------
    page.title = "PyMobile Calc - Cross-Platform Flet"
    page.theme_mode = ft.ThemeMode.DARK  # CSS: color-scheme: dark
    page.bgcolor = "#0B0F19"             # CSS: body { background: #0B0F19; }
    page.padding = 16                    # CSS: body { padding: 16px; }

    # Konfigurasi ukuran jendela pengujian (Rasio layar smartphone)
    page.window.width = 412
    page.window.height = 780
    page.window.resizable = True

    # -------------------------------------------------------------------------
    # 2. INISIALISASI LOGIKA DAN ANTARMUKA (MVC Binding)
    # -------------------------------------------------------------------------
    # Inisialisasi Mesin Logika (Model)
    calc_logic = CalculatorLogic()

    def handle_button_press(button_label: str):
        """
        EVENT DISPATCHER (Controller Action):
        Fungsi ini dipanggil oleh UI setiap kali sebuah tombol disentuh.
        
        Analogi Web:
        Mirip dengan event dispatcher:
        function onAction(action) {
          switch(action) { case 'C': logic.clear(); ... }
          render();
        }
        """
        if button_label == "C":
            calc_logic.clear()
        elif button_label == "DEL":
            calc_logic.delete_backspace()
        elif button_label == "=":
            calc_logic.calculate()
        elif button_label == "+/-":
            calc_logic.toggle_negate()
        elif button_label == "%":
            calc_logic.percent()
        elif button_label in ["+", "-", "×", "÷"]:
            calc_logic.add_operator(button_label)
        elif button_label == ".":
            calc_logic.add_decimal()
        elif button_label.isdigit():
            calc_logic.add_digit(button_label)

        # Ambil nilai terbaru dari logika dan perbarui tampilan UI
        exp, res = calc_logic.get_display()
        calc_ui.update_display(exp, res)

        # Analogi Web: Pemicu re-render DOM (seperti React setState / dispatch)
        page.update()

    # Inisialisasi Komponen Antarmuka (View) dengan meneruskan handler di atas
    calc_ui = CalculatorUI(on_button_press=handle_button_press)

    # -------------------------------------------------------------------------
    # 3. MOUNTING KOMPONEN KE DOM (DOM Attachment)
    # -------------------------------------------------------------------------
    # Analogi Web: document.body.appendChild(calc_ui.build_view())
    page.add(
        ft.Container(
            content=calc_ui.build_view(),
            alignment=ft.alignment.center,
        )
    )

    # Render awal layar
    exp, res = calc_logic.get_display()
    calc_ui.update_display(exp, res)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)