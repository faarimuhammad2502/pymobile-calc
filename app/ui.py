"""
=============================================================================
BERKAS: app/ui.py
PERAN  : Presentation Layer / Antarmuka Visual (View)
ANALOGI WEB:
- ft.Container  -> <div> dengan CSS inline / styling
- ft.Row        -> <div style="display: flex; flex-direction: row; gap: 10px;">
- ft.Column     -> <div style="display: flex; flex-direction: column; gap: 10px;">
- ft.Text       -> <span> / <p> dengan typography styling
- on_click      -> addEventListener('click', (e) => callback(value))
- bgcolor       -> background-color
- border_radius -> border-radius
=============================================================================
"""

import flet as ft
from typing import Callable, Optional


class CalculatorUI:
    """
    Kelas pembangun antarmuka kalkulator modern (Dark Mode).
    
    Analogi Web:
    Mirip dengan Komponen React:
    function CalculatorUI({ onButtonPress }) { ... }
    """

    def __init__(self, on_button_press: Callable[[str], None]):
        """
        Menerima callback 'on_button_press' dari controller (main.py).
        Ketika pengguna menyentuh tombol, UI memicu callback tersebut.
        """
        self.on_button_press = on_button_press
        self._init_components()

    def _init_components(self):
        """
        Inisialisasi elemen-elemen DOM Flet.
        """
        # Layar Atas: Menampilkan alur ekspresi / rumus (warna abu-abu)
        # Analogi Web: <p class="text-slate-400 text-sm font-mono text-right truncate">
        self.expression_display = ft.Text(
            value="",
            color="#94A3B8",
            size=16,
            text_align=ft.TextAlign.RIGHT,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        # Layar Bawah: Menampilkan angka aktif atau hasil kalkulasi besar
        # Analogi Web: <h1 class="text-white text-4xl font-bold font-mono text-right">
        self.result_display = ft.Text(
            value="0",
            color="#F8FAFC",
            size=44,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.RIGHT,
            max_lines=1,
            overflow=ft.TextOverflow.CLIP,
        )

        # Container Layar Display
        # Analogi Web: <div class="bg-[#161E2E] rounded-2xl p-4 shadow-lg border border-slate-800">
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
            bgcolor="#161E2E",      # CSS: background-color: #161E2E
            border_radius=20,       # CSS: border-radius: 20px
            border=ft.border.all(1, "#1E293B"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color="#050811",
                offset=ft.Offset(0, 4),
            ),
            height=150,
        )

    def _create_button(
        self,
        label: str,
        btn_type: str = "number",
        expand: int = 1,
        icon: Optional[str] = None,
    ) -> ft.Container:
        """
        Fungsi pembantu (helper) untuk membuat tombol sentuh.
        
        Analogi Web:
        Mirip dengan komponen <Button variant="operator" onClick={...}>label</Button>
        """
        # Skema warna Dark Mode
        bg_color = "#1E293B"     # CSS: bg-slate-800 (Tombol angka)
        text_color = "#F8FAFC"   # CSS: text-slate-50
        hover_color = "#334155"  # CSS: hover:bg-slate-700

        if btn_type == "operator":
            bg_color = "#EA580C"    # CSS: bg-orange-600 (Operator +, -, ×, ÷)
            text_color = "#FFFFFF"
            hover_color = "#F97316"
        elif btn_type == "action":
            bg_color = "#334155"    # CSS: bg-slate-700 (C, DEL, %)
            text_color = "#E2E8F0"
            hover_color = "#475569"
        elif btn_type == "equal":
            bg_color = "#F59E0B"    # CSS: bg-amber-500 (Tombol =)
            text_color = "#0B0F19"
            hover_color = "#FBBF24"

        # Konten teks atau ikon
        content = ft.Text(label, size=22, weight=ft.FontWeight.W_600, color=text_color)
        if icon == "backspace":
           content = ft.Icon(name=ft.icons.BACKSPACE_OUTLINED, color=text_color, size=22)
        # Event handler tombol
        def handle_click(e):
            # Memicu callback ke controller di main.py
            self.on_button_press(label)

        # Analogi Web:
        # <button class="flex items-center justify-center rounded-2xl h-16 transition-transform active:scale-95">
        return ft.Container(
            content=content,
            alignment=ft.alignment.center,
            bgcolor=bg_color,
            border_radius=16,
            height=64,
            expand=expand,        # CSS: flex: 1 (membagi lebar secara proporsional)
            on_click=handle_click, # Analogi Web: onClick={handleClick}
            animate=ft.Animation(120, ft.AnimationCurve.EASE_OUT),
            ink=True,              # Efek ripple sentuh Material/Flutter
        )

    def _build_keypad(self) -> ft.Column:
        """
        Membangun kisi papan tombol kalkulator menggunakan Flexbox (Row & Column).
        
        Analogi Web:
        <div style="display: flex; flex-direction: column; gap: 10px;">
          <div style="display: flex; flex-direction: row; gap: 10px;"> ... </div>
        </div>
        """
        return ft.Column(
            controls=[
                # Baris 1: C, DEL, %, ÷
                ft.Row([
                    self._create_button("C", btn_type="action"),
                    self._create_button("DEL", btn_type="action", icon="backspace"),
                    self._create_button("%", btn_type="action"),
                    self._create_button("÷", btn_type="operator"),
                ], spacing=10),

                # Baris 2: 7, 8, 9, ×
                ft.Row([
                    self._create_button("7"),
                    self._create_button("8"),
                    self._create_button("9"),
                    self._create_button("×", btn_type="operator"),
                ], spacing=10),

                # Baris 3: 4, 5, 6, -
                ft.Row([
                    self._create_button("4"),
                    self._create_button("5"),
                    self._create_button("6"),
                    self._create_button("-", btn_type="operator"),
                ], spacing=10),

                # Baris 4: 1, 2, 3, +
                ft.Row([
                    self._create_button("1"),
                    self._create_button("2"),
                    self._create_button("3"),
                    self._create_button("+", btn_type="operator"),
                ], spacing=10),

                # Baris 5: +/-, 0, ., =
                ft.Row([
                    self._create_button("+/-", btn_type="action"),
                    self._create_button("0"),
                    self._create_button("."),
                    self._create_button("=", btn_type="equal"),
                ], spacing=10),
            ],
            spacing=10,
        )

    def update_display(self, expression: str, result: str):
        """
        Memperbarui teks pada elemen layar secara dinamis.
        
        Analogi Web:
        expressionDisplay.innerText = expression;
        resultDisplay.innerText = result;
        """
        self.expression_display.value = expression
        self.result_display.value = result

        # Penyesuaian ukuran font dinamis (Dynamic Font Scaling)
        val_len = len(result)
        if val_len > 13:
            self.result_display.size = 26
        elif val_len > 8:
            self.result_display.size = 34
        else:
            self.result_display.size = 44

        # Ubah warna teks menjadi merah jika terjadi error (misal: dibagi nol)
        if "Error" in result:
            self.result_display.color = "#EF4444"
        else:
            self.result_display.color = "#F8FAFC"

    def build_view(self) -> ft.Container:
        """
        Mengembalikan wadah antarmuka root yang siap dipasang ke page.
        
        Analogi Web:
        Mirip dengan me-render komponen root:
        <main class="w-full max-w-sm flex flex-col gap-4">
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.display_container,
                    ft.Divider(height=1, color="#1E293B"),
                    self._build_keypad(),
                ],
                spacing=16,
            ),
            width=390,
            alignment=ft.alignment.center,
        )
