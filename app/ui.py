import flet as ft
from typing import Callable, Optional

class CalculatorUI:
    def __init__(self, on_button_press: Callable[[str], None]):
        self.on_button_press = on_button_press
        self._init_components()

    def _init_components(self):
        # Layar Atas: Menampilkan ekspresi/rumus
        self.expression_display = ft.Text(
            value="",
            color="#94A3B8",
            size=16,
            text_align=ft.TextAlign.RIGHT,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        # Layar Bawah: Menampilkan hasil/angka aktif
        self.result_display = ft.Text(
            value="0",
            color="#F8FAFC",
            size=40,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.RIGHT,
            max_lines=1,
            overflow=ft.TextOverflow.CLIP,
        )

        # Container Layar Display
        self.display_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.expression_display,
                    self.result_display,
                ],
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.END,
                spacing=4,
            ),
            padding=ft.padding.all(20),
            bgcolor="#161E2E",
            border_radius=20,
            border=ft.border.all(1, "#1E293B"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color="#050811",
                offset=ft.Offset(0, 4),
            ),
            height=140,
        )

    def _create_button(
        self,
        label: str,
        btn_type: str = "number",
        icon: Optional[str] = None,
    ) -> ft.Container:
        bg_color = "#1E293B"     # Tombol angka
        text_color = "#F8FAFC"

        if btn_type == "operator":
            bg_color = "#EA580C" # Tombol operator (+, -, ×, ÷)
            text_color = "#FFFFFF"
        elif btn_type == "action":
            bg_color = "#334155" # Tombol aksi (C, DEL, %)
            text_color = "#E2E8F0"
        elif btn_type == "equal":
            bg_color = "#F59E0B" # Tombol sama dengan (=)
            text_color = "#0B0F19"

        if icon == "backspace":
            content = ft.Icon(name=ft.icons.BACKSPACE_OUTLINED, color=text_color, size=22)
        else:
            content = ft.Text(label, size=22, weight=ft.FontWeight.W_600, color=text_color)

        def handle_click(e):
            self.on_button_press(label)

        return ft.Container(
            content=content,
            alignment=ft.alignment.center,
            bgcolor=bg_color,
            border_radius=16,
            height=62,
            expand=True, # Membagi 4 tombol rata 25% selebar baris
            on_click=handle_click,
            ink=True,
        )

    def _build_keypad(self) -> ft.Column:
        return ft.Column(
            controls=[
                ft.Row(
                    [
                        self._create_button("C", btn_type="action"),
                        self._create_button("DEL", btn_type="action", icon="backspace"),
                        self._create_button("%", btn_type="action"),
                        self._create_button("÷", btn_type="operator"),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        self._create_button("7"),
                        self._create_button("8"),
                        self._create_button("9"),
                        self._create_button("×", btn_type="operator"),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        self._create_button("4"),
                        self._create_button("5"),
                        self._create_button("6"),
                        self._create_button("-", btn_type="operator"),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        self._create_button("1"),
                        self._create_button("2"),
                        self._create_button("3"),
                        self._create_button("+", btn_type="operator"),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        self._create_button("+/-", btn_type="action"),
                        self._create_button("0"),
                        self._create_button("."),
                        self._create_button("=", btn_type="equal"),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def update_display(self, expression: str, result: str):
        self.expression_display.value = expression
        self.result_display.value = result

        val_len = len(result)
        if val_len > 13:
            self.result_display.size = 24
        elif val_len > 8:
            self.result_display.size = 32
        else:
            self.result_display.size = 40

        if "Error" in result:
            self.result_display.color = "#EF4444"
        else:
            self.result_display.color = "#F8FAFC"

    def build_view(self) -> ft.Column:
        return ft.Column(
            controls=[
                self.display_container,
                ft.Divider(height=1, color="#1E293B"),
                self._build_keypad(),
            ],
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )