import flet as ft
from typing import Callable, Optional

class CalculatorUI:
    def __init__(self, on_button_press: Callable[[str], None]):
        self.on_button_press = on_button_press
        self._init_components()

    def _init_components(self):
        # Layar Atas (Rumus)
        self.expression_display = ft.Text(
            value="", color="#94A3B8", size=16, text_align=ft.TextAlign.RIGHT,
            max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
        )
        # Layar Bawah (Hasil)
        self.result_display = ft.Text(
            value="0", color="#F8FAFC", size=44, weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.RIGHT, max_lines=1, overflow=ft.TextOverflow.CLIP,
        )
        self.display_container = ft.Container(
            content=ft.Column(
                controls=[self.expression_display, self.result_display],
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.END,
                spacing=4,
            ),
            padding=ft.padding.all(20), bgcolor="#161E2E",
            border_radius=20, border=ft.border.all(1, "#1E293B"),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=12, color="#050811", offset=ft.Offset(0, 4)),
            height=150,
        )

    def _create_button(self, label: str, btn_type: str = "number", expand: int = 1, icon: Optional[str] = None) -> ft.Container:
        bg_color, text_color, hover_color = "#1E293B", "#F8FAFC", "#334155"
        if btn_type == "operator":
            bg_color, text_color, hover_color = "#EA580C", "#FFFFFF", "#F97316"
        elif btn_type == "action":
            bg_color, text_color, hover_color = "#334155", "#E2E8F0", "#475569"
        elif btn_type == "equal":
            bg_color, text_color, hover_color = "#F59E0B", "#0B0F19", "#FBBF24"

        content = ft.Text(label, size=22, weight=ft.FontWeight.W_600, color=text_color)
        if icon == "backspace":
            # Memperbaiki error ikon menjadi huruf kecil "ft.icons"
            content = ft.Icon(name=ft.icons.BACKSPACE_OUTLINED, color=text_color, size=22)

        def handle_click(e):
            self.on_button_press(label)

        return ft.Container(
            content=content,
            alignment=ft.alignment.center,
            bgcolor=bg_color,
            border_radius=16,
            height=64,
            expand=True, # <--- Kunci agar tombol membentang rapi dan tidak terpotong
            on_click=handle_click,
            animate=ft.Animation(120, ft.AnimationCurve.EASE_OUT),
            ink=True,
        )

    def _build_keypad(self) -> ft.Column:
        return ft.Column(
            controls=[
                ft.Row([self._create_button("C", btn_type="action"), self._create_button("DEL", btn_type="action", icon="backspace"), self._create_button("%", btn_type="action"), self._create_button("÷", btn_type="operator")], spacing=10),
                ft.Row([self._create_button("7"), self._create_button("8"), self._create_button("9"), self._create_button("×", btn_type="operator")], spacing=10),
                ft.Row([self._create_button("4"), self._create_button("5"), self._create_button("6"), self._create_button("-", btn_type="operator")], spacing=10),
                ft.Row([self._create_button("1"), self._create_button("2"), self._create_button("3"), self._create_button("+", btn_type="operator")], spacing=10),
                ft.Row([self._create_button("+/-", btn_type="action"), self._create_button("0"), self._create_button("."), self._create_button("=", btn_type="equal")], spacing=10),
            ],
            spacing=10,
            expand=True,
        )

    def update_display(self, expression: str, result: str):
        self.expression_display.value = expression
        self.result_display.value = result
        val_len = len(result)
        if val_len > 13: self.result_display.size = 26
        elif val_len > 8: self.result_display.size = 34
        else: self.result_display.size = 44
        self.result_display.color = "#EF4444" if "Error" in result else "#F8FAFC"

    def build_view(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.display_container,
                    ft.Divider(height=1, color="#1E293B"),
                    self._build_keypad(),
                ],
                spacing=16,
            ),
            expand=True, # <--- Mengganti width statis agar aplikasi menyesuaikan layar HP
            padding=10,
        )