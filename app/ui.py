import flet as ft
from typing import Callable, Optional

class CalculatorUI:
    def __init__(self, on_button_press: Callable[[str], None], on_convert: Callable[[str, str, str, str], str], on_clear_history: Callable[[], None]):
        self.on_button_press = on_button_press
        self.on_convert = on_convert
        self.on_clear_history = on_clear_history
        self._init_components()

    def _init_components(self):
        # Display Layar Utama
        self.expression_display = ft.Text(
            value="", color="#94A3B8", size=16, text_align=ft.TextAlign.RIGHT,
            max_lines=1, overflow=ft.TextOverflow.ELLIPSIS
        )
        self.result_display = ft.Text(
            value="0", color="#F8FAFC", size=44, weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.RIGHT, max_lines=1, overflow=ft.TextOverflow.CLIP
        )
        self.display_container = ft.Container(
            content=ft.Column(
                controls=[self.expression_display, self.result_display],
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.END,
                spacing=2,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor="#161E2E",
            border_radius=18,
            border=ft.border.all(1, "#1E293B"),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=12, color="#050811", offset=ft.Offset(0, 4)),
            height=130,
        )

        # Dropdowns Konverter
        self.category_dd = ft.Dropdown(
            options=[
                ft.dropdown.Option("Panjang"),
                ft.dropdown.Option("Massa / Berat"),
                ft.dropdown.Option("Waktu"),
                ft.dropdown.Option("Suhu"),
                ft.dropdown.Option("Mata Uang"),
            ],
            value="Panjang",
            label="Kategori Konversi",
            color="#F8FAFC",
            bgcolor="#161E2E",
            border_color="#334155",
            on_change=self._on_category_change
        )
        self.from_unit_dd = ft.Dropdown(color="#F8FAFC", bgcolor="#161E2E", border_color="#334155", expand=True, label="Dari")
        self.to_unit_dd = ft.Dropdown(color="#F8FAFC", bgcolor="#161E2E", border_color="#334155", expand=True, label="Ke")
        self.convert_input = ft.TextField(
            label="Nilai Input", value="1", keyboard_type=ft.KeyboardType.NUMBER,
            color="#F8FAFC", border_color="#334155", bgcolor="#161E2E"
        )
        self.convert_result_text = ft.Text(value="Hasil: -", size=18, weight=ft.FontWeight.BOLD, color="#F59E0B")
        self._update_unit_options("Panjang")

        # Container Riwayat
        self.history_list = ft.ListView(expand=True, spacing=8, padding=4)

    def _update_unit_options(self, category: str):
        units = {
            "Panjang": ["Meter (m)", "Kilometer (km)", "Centimeter (cm)", "Millimeter (mm)", "Inch (in)", "Feet (ft)"],
            "Massa / Berat": ["Kilogram (kg)", "Gram (g)", "Milligram (mg)", "Pound (lbs)"],
            "Waktu": ["Detik (s)", "Menit (min)", "Jam (h)", "Hari (d)"],
            "Suhu": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"],
            "Mata Uang": ["Rupiah (IDR)", "US Dollar (USD)", "Euro (EUR)", "Yen (JPY)", "SGD (S$)"]
        }
        opts = [ft.dropdown.Option(u) for u in units.get(category, [])]
        self.from_unit_dd.options = opts
        self.to_unit_dd.options = opts
        if units.get(category):
            self.from_unit_dd.value = units[category][0]
            self.to_unit_dd.value = units[category][1] if len(units[category]) > 1 else units[category][0]

    def _on_category_change(self, e):
        self._update_unit_options(self.category_dd.value)
        if self.from_unit_dd.page:
            self.from_unit_dd.update()
            self.to_unit_dd.update()

    def _create_btn(self, label: str, btn_type: str = "number", icon: Optional[str] = None, font_size: int = 20, expand: int = 1) -> ft.Container:
        bg_color, text_color = "#1E293B", "#F8FAFC"
        if btn_type == "operator":
            bg_color, text_color = "#EA580C", "#FFFFFF"
        elif btn_type == "action":
            bg_color, text_color = "#334155", "#E2E8F0"
        elif btn_type == "equal":
            bg_color, text_color = "#F59E0B", "#0B0F19"
        elif btn_type == "sci":
            bg_color, text_color = "#0F172A", "#38BDF8"

        if icon == "backspace":
            content = ft.Icon(name=ft.icons.BACKSPACE_OUTLINED, color=text_color, size=22)
        else:
            content = ft.Text(label, size=font_size, weight=ft.FontWeight.W_600, color=text_color)

        return ft.Container(
            content=content,
            alignment=ft.alignment.center,
            bgcolor=bg_color,
            border_radius=14,
            expand=expand,
            on_click=lambda e: self.on_button_press(label),
            ink=True,
        )

    def _build_standard_keypad(self) -> ft.Column:
        return ft.Column([
            ft.Row([self._create_btn("C", "action"), self._create_btn("DEL", "action", icon="backspace"), self._create_btn("%", "action"), self._create_btn("÷", "operator")], spacing=8, expand=True),
            ft.Row([self._create_btn("7"), self._create_btn("8"), self._create_btn("9"), self._create_btn("×", "operator")], spacing=8, expand=True),
            ft.Row([self._create_btn("4"), self._create_btn("5"), self._create_btn("6"), self._create_btn("-", "operator")], spacing=8, expand=True),
            ft.Row([self._create_btn("1"), self._create_btn("2"), self._create_btn("3"), self._create_btn("+", "operator")], spacing=8, expand=True),
            ft.Row([self._create_btn("+/-", "action"), self._create_btn("0"), self._create_btn("."), self._create_btn("=", "equal")], spacing=8, expand=True),
        ], spacing=8, expand=True, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    def _build_scientific_keypad(self) -> ft.Column:
        return ft.Column([
            ft.Row([self._create_btn("sin", "sci", font_size=13), self._create_btn("cos", "sci", font_size=13), self._create_btn("tan", "sci", font_size=13), self._create_btn("log", "sci", font_size=13), self._create_btn("ln", "sci", font_size=13)], spacing=6, expand=True),
            ft.Row([self._create_btn("√", "sci"), self._create_btn("^", "sci"), self._create_btn("π", "sci"), self._create_btn("e", "sci"), self._create_btn("!", "sci")], spacing=6, expand=True),
            ft.Row([self._create_btn("(", "sci"), self._create_btn(")", "sci"), self._create_btn("C", "action"), self._create_btn("DEL", "action", icon="backspace"), self._create_btn("÷", "operator")], spacing=6, expand=True),
            ft.Row([self._create_btn("7"), self._create_btn("8"), self._create_btn("9"), self._create_btn("%", "action"), self._create_btn("×", "operator")], spacing=6, expand=True),
            ft.Row([self._create_btn("4"), self._create_btn("5"), self._create_btn("6"), self._create_btn("+/-", "action"), self._create_btn("-", "operator")], spacing=6, expand=True),
            ft.Row([self._create_btn("1"), self._create_btn("2"), self._create_btn("3"), self._create_btn(".", "number"), self._create_btn("+", "operator")], spacing=6, expand=True),
            ft.Row([self._create_btn("0", expand=2), self._create_btn("=", "equal", expand=3)], spacing=6, expand=True),
        ], spacing=6, expand=True, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    def _build_converter_view(self) -> ft.Column:
        def do_convert(e):
            res = self.on_convert(self.category_dd.value, self.from_unit_dd.value, self.to_unit_dd.value, self.convert_input.value)
            self.convert_result_text.value = f"Hasil: {res}"
            if self.convert_result_text.page:
                self.convert_result_text.update()

        return ft.Column([
            self.category_dd,
            ft.Row([self.from_unit_dd, self.to_unit_dd], spacing=8),
            self.convert_input,
            ft.Container(
                content=ft.ElevatedButton("Hitung Konversi", on_click=do_convert, bgcolor="#EA580C", color="#FFFFFF", height=48),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=8)
            ),
            ft.Divider(color="#334155"),
            ft.Container(
                content=self.convert_result_text,
                alignment=ft.alignment.center,
                padding=16,
                bgcolor="#161E2E",
                border_radius=12,
                border=ft.border.all(1, "#1E293B")
            )
        ], spacing=14, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    def _build_history_view(self) -> ft.Column:
        return ft.Column([
            ft.Row([
                ft.Text("Riwayat Perhitungan", size=18, weight=ft.FontWeight.BOLD, color="#F8FAFC"),
                ft.IconButton(icon=ft.icons.DELETE_OUTLINE, icon_color="#EF4444", on_click=lambda e: self.on_clear_history())
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(content=self.history_list, expand=True)
        ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    def update_history_ui(self, history_data: list):
        self.history_list.controls.clear()
        if not history_data:
            self.history_list.controls.append(ft.Text("Belum ada riwayat", color="#64748B"))
        else:
            for item in reversed(history_data):
                self.history_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(item['exp'], color="#94A3B8", size=14),
                            ft.Text(f"= {item['res']}", color="#F8FAFC", size=20, weight=ft.FontWeight.BOLD),
                        ]),
                        bgcolor="#161E2E", padding=12, border_radius=12, border=ft.border.all(1, "#1E293B")
                    )
                )
        if self.history_list.page:
            self.history_list.update()

    def update_display(self, expression: str, result: str):
        self.expression_display.value = expression
        self.result_display.value = result
        val_len = len(result)
        if val_len > 13: self.result_display.size = 26
        elif val_len > 8: self.result_display.size = 34
        else: self.result_display.size = 44
        self.result_display.color = "#EF4444" if "Error" in result else "#F8FAFC"
        if self.expression_display.page:
            self.expression_display.update()
            self.result_display.update()

    def _get_calc_layout(self, keypad_widget):
        return ft.Column([
            self.display_container,
            ft.Divider(height=1, color="#1E293B"),
            ft.Container(content=keypad_widget, expand=True)
        ], expand=True, spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    def build_view(self) -> ft.Column:
        self.std_layout = self._get_calc_layout(self._build_standard_keypad())
        self.sci_layout = self._get_calc_layout(self._build_scientific_keypad())
        self.conv_layout = self._build_converter_view()
        self.hist_layout = self._build_history_view()

        content_area = ft.Container(
            content=self.std_layout,
            expand=True,
            padding=ft.padding.only(top=8)
        )

        def on_tab_change(e):
            idx = e.control.selected_index
            if idx == 0:
                content_area.content = self.std_layout
            elif idx == 1:
                content_area.content = self.sci_layout
            elif idx == 2:
                content_area.content = self.conv_layout
            elif idx == 3:
                content_area.content = self.hist_layout
            content_area.update()

        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=150,
            tabs=[
                ft.Tab(text="Standar", icon=ft.icons.CALCULATE),
                ft.Tab(text="Ilmiah", icon=ft.icons.FUNCTIONS),
                ft.Tab(text="Konversi", icon=ft.icons.SWAP_HORIZ),
                ft.Tab(text="Riwayat", icon=ft.icons.HISTORY),
            ],
            on_change=on_tab_change,
            expand=False
        )

        return ft.Column([
            tabs,
            content_area
        ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)