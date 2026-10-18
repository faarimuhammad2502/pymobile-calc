"""
=============================================================================
BERKAS: app/ui.py
PERAN  : Presentation Layer / Antarmuka Visual (View) - VERSI FINAL
=============================================================================
"""
import flet as ft
from typing import Callable

class CalculatorUI:
    def __init__(self, on_button_press: Callable[[str], None]):
        self.on_button_press = on_button_press
        self._init_components()

    def _init_components(self):
        self.expression_display = ft.Text(value="", color="#94A3B8", size=16, text_align=ft.TextAlign.RIGHT)
        self.result_display = ft.Text(value="0", color="#F8FAFC", size=48, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.RIGHT)

        self.display_container = ft.Container(
            content=ft.Column(
                controls=[self.expression_display, self.result_display],
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.END,
                spacing=5,
            ),
            padding=20, bgcolor="#0F172A", border_radius=24, width=340, height=130, alignment=ft.alignment.bottom_right,
        )
        
        self.history_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)

        # KOMPONEN KONVERSI
        self.conv_category = ft.Dropdown(
            options=[ft.dropdown.Option("Panjang"), ft.dropdown.Option("Massa"), ft.dropdown.Option("Waktu"), ft.dropdown.Option("Basis Bilangan")],
            value="Panjang", bgcolor="#1E293B", color="#F8FAFC", border_color="#334155", on_change=self._handle_category_change
        )
        self.conv_input = ft.TextField(hint_text="0", value="", bgcolor="#1E293B", color="#F8FAFC", border_color="#334155", on_change=self._handle_convert)
        self.conv_from = ft.Dropdown(width=140, bgcolor="#1E293B", color="#F8FAFC", border_color="#334155", on_change=self._handle_convert)
        self.conv_to = ft.Dropdown(width=140, bgcolor="#1E293B", color="#F8FAFC", border_color="#334155", on_change=self._handle_convert)
        self.conv_result = ft.Text("0", color="#EA580C", size=32, weight=ft.FontWeight.BOLD)
        
        # Panggil pemuatan awal kategori
        self._handle_category_change(None, init=True)

    def _handle_category_change(self, e, init=False):
        cat = self.conv_category.value
        units = {
            "Panjang": ["Meter", "Centimeter", "Kilometer", "Milimeter"],
            "Massa": ["Kilogram", "Gram", "Miligram"],
            "Waktu": ["Detik", "Menit", "Jam", "Hari"],
            "Basis Bilangan": ["Desimal", "Biner", "Oktal", "Heksadesimal"]
        }
        
        # PERBAIKAN BUG: Hapus opsi lama sepenuhnya agar sistem Flet merender opsi satuan yang baru
        self.conv_from.options.clear()
        self.conv_to.options.clear()
        
        for u in units[cat]:
            self.conv_from.options.append(ft.dropdown.Option(u))
            self.conv_to.options.append(ft.dropdown.Option(u))
            
        self.conv_from.value = units[cat][0]
        self.conv_to.value = units[cat][1]
        
        if not init:
            self.conv_input.value = ""  # Kosongkan nilai input secara otomatis saat ganti kategori
            self.conv_input.update()
            self.conv_from.update()
            self.conv_to.update()
            self._handle_convert(None)

    def _handle_convert(self, e):
        inp = self.conv_input.value.strip() or "0"
        cat = self.conv_category.value
        fr = self.conv_from.value
        to = self.conv_to.value
        
        if not fr or not to: return

        if cat == "Basis Bilangan":
            bases = {"Desimal": 10, "Biner": 2, "Oktal": 8, "Heksadesimal": 16}
            try:
                clean_inp = inp.split('.')[0] # Sistem basis bilangan hanya menerima angka bulat (integer)
                dec_val = int(clean_inp, bases[fr])
                
                if to == "Desimal": res = str(dec_val)
                elif to == "Biner": res = bin(dec_val)[2:]
                elif to == "Oktal": res = oct(dec_val)[2:]
                elif to == "Heksadesimal": res = hex(dec_val)[2:].upper()
                
                self.conv_result.value = res
            except ValueError:
                self.conv_result.value = "Error"
        else:
            try:
                val = float(inp)
                factors = {
                    "Panjang": {"Meter": 1, "Centimeter": 0.01, "Kilometer": 1000, "Milimeter": 0.001},
                    "Massa": {"Kilogram": 1000, "Gram": 1, "Miligram": 0.001},
                    "Waktu": {"Detik": 1, "Menit": 60, "Jam": 3600, "Hari": 86400}
                }
                # Menghitung konversi menyilang via nilai standar
                std_val = val * factors[cat][fr]
                res_val = std_val / factors[cat][to]
                
                # Format hasil akhir agar rapi dan tidak kepanjangan
                if res_val.is_integer():
                    self.conv_result.value = str(int(res_val))
                else:
                    self.conv_result.value = f"{res_val:.6g}"
            except ValueError:
                self.conv_result.value = "Error"
                
        self.conv_result.update()

    def _create_button(self, label: str, btn_type: str = "number", width=70, height=70, font_size=24):
        bg_color = "#1E293B"
        text_color = "#F8FAFC"
        if btn_type == "operator" or btn_type == "equal":
            bg_color = "#EA580C"
            text_color = "#FFFFFF"
        elif btn_type == "action":
            bg_color = "#334155"
            text_color = "#E2E8F0"

        return ft.Container(
            content=ft.Text(label, size=font_size, weight=ft.FontWeight.W_500, color=text_color, text_align=ft.TextAlign.CENTER),
            width=width, height=height, bgcolor=bg_color, border_radius=20, alignment=ft.alignment.center,
            ink=True, on_click=lambda e: self.on_button_press(label)
        )

    def _build_standar_keypad(self):
        return ft.Column([
            ft.Row([self._create_button("C", "action"), self._create_button("DEL", "action"), self._create_button("%", "action"), self._create_button("÷", "operator")], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self._create_button("7"), self._create_button("8"), self._create_button("9"), self._create_button("×", "operator")], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self._create_button("4"), self._create_button("5"), self._create_button("6"), self._create_button("-", "operator")], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self._create_button("1"), self._create_button("2"), self._create_button("3"), self._create_button("+", "operator")], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self._create_button("+/-", "action"), self._create_button("0"), self._create_button("."), self._create_button("=", "equal")], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
        ], spacing=12)

    def _build_ilmiah_keypad(self):
        def _btn(lbl, btype="number"): return self._create_button(lbl, btype, width=70, height=52, font_size=18)
        return ft.Column([
            ft.Row([_btn("sin", "action"), _btn("cos", "action"), _btn("tan", "action"), _btn("log", "action")], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([_btn("√", "action"), _btn("^", "action"), _btn("(", "action"), _btn(")", "action")], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([_btn("C", "action"), _btn("DEL", "action"), _btn("%", "action"), _btn("÷", "operator")], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([_btn("7"), _btn("8"), _btn("9"), _btn("×", "operator")], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([_btn("4"), _btn("5"), _btn("6"), _btn("-", "operator")], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([_btn("1"), _btn("2"), _btn("3"), _btn("+", "operator")], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([_btn("π", "action"), _btn("0"), _btn("."), _btn("=", "equal")], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
        ], spacing=12)

    def update_display(self, expression: str, result: str):
        self.expression_display.value = expression
        self.result_display.value = result
        val_len = len(result)
        if val_len > 12: self.result_display.size = 28
        elif val_len > 8: self.result_display.size = 36
        else: self.result_display.size = 48
        self.result_display.color = "#EF4444" if "Error" in result else "#F8FAFC"
        self.result_display.update()
        self.expression_display.update()

    def add_history_item(self, expression: str, result: str):
        item = ft.Container(
            content=ft.Column([
                ft.Text(expression, color="#94A3B8", size=14),
                ft.Text(f"= {result}", color="#EA580C", size=20, weight=ft.FontWeight.BOLD)
            ], horizontal_alignment=ft.CrossAxisAlignment.END),
            padding=15, bgcolor="#1E293B", border_radius=15, margin=ft.margin.only(bottom=10)
        )
        self.history_list.controls.insert(0, item)
        self.history_list.update()

    def clear_history(self):
        self.history_list.controls.clear()
        self.history_list.update()

    def build_view(self):
        tab_standar = ft.Container(content=ft.Column([ft.Container(height=10), self.display_container, ft.Container(height=10), self._build_standar_keypad()], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        tab_ilmiah = ft.Container(content=ft.Column([ft.Container(height=5), self.display_container, ft.Container(height=5), self._build_ilmiah_keypad()], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        
        tab_konversi = ft.Container(
            content=ft.Column([
                ft.Text("Kategori Konversi", color="#94A3B8"),
                self.conv_category,
                ft.Container(height=5),
                self.conv_input,
                ft.Container(height=5),
                ft.Row([self.conv_from, ft.Icon(ft.icons.ARROW_FORWARD, color="#EA580C"), self.conv_to], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=20),
                ft.Container(content=ft.Column([ft.Text("Hasil Konversi:", color="#94A3B8", size=14), self.conv_result]), padding=20, bgcolor="#1E293B", border_radius=15, width=340)
            ]), padding=ft.padding.only(top=20), alignment=ft.alignment.top_center
        )

        tab_riwayat = ft.Container(
            content=ft.Column([
                ft.Row([ft.Text("Riwayat Terakhir", size=18, weight=ft.FontWeight.BOLD, color="#F8FAFC"), ft.IconButton(icon=ft.icons.DELETE_OUTLINE, icon_color="#EF4444", on_click=lambda e: self.clear_history(), tooltip="Hapus Semua")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(color="#334155"),
                self.history_list
            ]), padding=ft.padding.only(top=20)
        )

        tabs_menu = ft.Tabs(
            selected_index=0, animation_duration=300, expand=1, label_color="#EA580C", unselected_label_color="#94A3B8", indicator_color="#EA580C",
            tabs=[ft.Tab(text="Standar", content=tab_standar), ft.Tab(text="Ilmiah", content=tab_ilmiah), ft.Tab(text="Konversi", content=tab_konversi), ft.Tab(text="Riwayat", content=tab_riwayat)]
        )

        return ft.Container(content=tabs_menu, width=380, height=740, padding=ft.padding.only(left=20, right=20, top=10, bottom=20), bgcolor="#0B0F19", border_radius=30)