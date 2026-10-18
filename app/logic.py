"""
=============================================================================
BERKAS: app/logic.py
PERAN  : Pure Business Logic / Math Engine (Model)
ANALOGI WEB: 
Mirip dengan class Service di TypeScript atau Redux Reducer di React.
File ini 100% murni logika matematika dan TIDAK MENGIMPOR FLET (zero UI).
Dapat diuji secara mandiri (unit test) menggunakan pytest tanpa butuh UI.
=============================================================================
"""

import math
from typing import Tuple, List, Dict


class CalculatorLogic:
    """
    Kelas pengelola state dan logika perhitungan kalkulator.
    
    Analogi Web:
    Mirip dengan class CalculatorService di Angular/React:
    - this.expression ~ state.expression (string rumus)
    - this.currentNumber ~ state.currentNumber (input aktif di buffer)
    """

    def __init__(self):
        # Reset seluruh state ke kondisi awal
        self.clear()
        self.history: List[Dict[str, str]] = []

    def clear(self):
        """
        Mereset seluruh input kalkulator (Tombol 'C').
        Analogi Web: setExpression(''), setCurrentNumber('0')
        """
        self.expression: str = ""       # Rumus berjalan (contoh: "12 × 4 + ")
        self.current_number: str = "0"  # Angka aktif di buffer layar utama
        self.last_result: str = "0"     # Hasil perhitungan terakhir
        self.just_calculated: bool = False # Flag apakah baru saja menekan '='

    def delete_backspace(self):
        """
        Menghapus 1 karakter terakhir (Tombol 'DEL').
        Analogi Web: currentNumber.slice(0, -1)
        """
        if self.just_calculated:
            self.clear()
            return

        if len(self.current_number) > 1:
            self.current_number = self.current_number[:-1]
        else:
            self.current_number = "0"

    def add_digit(self, digit: str):
        """
        Menambahkan digit angka (0-9) ke angka aktif saat ini.
        Analogi Web: currentNumber === '0' ? digit : currentNumber + digit
        """
        if self.just_calculated:
            self.current_number = digit
            self.expression = ""
            self.just_calculated = False
            return

        if self.current_number == "0":
            self.current_number = digit
        else:
            # Batasi panjang digit agar tidak meluap dari layar ponsel
            if len(self.current_number) < 15:
                self.current_number += digit

    def add_decimal(self):
        """
        VALIDASI TITIK DESIMAL (PROTEKSI GANDA):
        Mencegah pengguna memasukkan lebih dari satu titik desimal
        dalam satu angka aktif (misal: '12.3.4' dicegah otomatis).
        
        Analogi Web:
        if (!currentNumber.includes('.')) { currentNumber += '.'; }
        """
        if self.just_calculated:
            self.current_number = "0."
            self.expression = ""
            self.just_calculated = False
            return

        # Pengecekan krusial: hanya tambahkan '.' jika belum ada titik di angka ini
        if "." not in self.current_number:
            self.current_number += "."

    def toggle_negate(self):
        """
        Mengubah tanda positif / negatif (+/-).
        Analogi Web: currentNumber.startsWith('-') ? slice(1) : '-' + currentNumber
        """
        if self.current_number == "0" or "Error" in self.current_number:
            return
        if self.current_number.startswith("-"):
            self.current_number = self.current_number[1:]
        else:
            self.current_number = "-" + self.current_number

    def percent(self):
        """
        Menghitung persentase dari angka aktif (Tombol '%').
        Analogi Web: currentNumber = (parseFloat(currentNumber) / 100).toString()
        """
        try:
            val = float(self.current_number)
            self.current_number = self._format_number(val / 100.0)
        except Exception:
            self.current_number = "Error"

    def add_operator(self, op: str):
        """
        Menambahkan operator matematika (+, -, ×, ÷).
        Mendukung chaining operations (perangkaian rumus bertingkat).
        """
        if "Error" in self.current_number:
            self.clear()
            return

        if self.just_calculated:
            self.expression = f"{self.last_result} {op} "
            self.current_number = "0"
            self.just_calculated = False
            return

        # Gabungkan angka aktif ke dalam ekspresi rumus
        self.expression += f"{self.current_number} {op} "
        self.current_number = "0"

    def calculate(self):
        """
        EVALUASI HASIL RUMUS (Tombol '='):
        1. Menghitung ekspresi dengan urutan operasi matematika yang benar (PEMDAS).
        2. MENANGANI PEMBAGIAN DENGAN NOL SECARA AMAN (Safe Zero-Division Guard).
        """
        full_formula = self.expression + self.current_number
        if not full_formula.strip() or "Error" in self.current_number:
            return

        # Ganti simbol tampilan mobile ke operator aritmatika Python
        eval_formula = (
            full_formula
            .replace("×", "*")
            .replace("÷", "/")
        )

        try:
            # PROTEKSI PEMBAGIAN NOL:
            # Periksa jika ada pembagi nol (misal: '/ 0' atau '/0') yang bukan '0.5'
            parts = eval_formula.split("/")
            for p in parts[1:]:
                p_clean = p.strip().lstrip("(").strip()
                if p_clean == "0" or p_clean.startswith("0 ") or p_clean.startswith("0)"):
                    self.last_result = "Error: Dibagi 0"
                    self.current_number = "Error: Dibagi 0"
                    self.just_calculated = True
                    return

            # Evaluasi ekspresi matematika dengan lingkungan aman
            allowed_names = {"abs": abs, "round": round, "pow": pow, "math": math}
            raw_result = eval(eval_formula, {"__builtins__": None}, allowed_names)

            if isinstance(raw_result, (int, float)):
                if math.isinf(raw_result) or math.isnan(raw_result):
                    self.last_result = "Error: Tak Terdefinisi"
                else:
                    self.last_result = self._format_number(raw_result)
            else:
                self.last_result = str(raw_result)

            # Simpan ke riwayat kalkulasi
            self.history.append({
                "expression": full_formula,
                "result": self.last_result
            })

            self.current_number = self.last_result
            self.just_calculated = True

        except ZeroDivisionError:
            # Menangani error pembagian dengan angka nol secara eksplisit
            self.last_result = "Error: Dibagi 0"
            self.current_number = "Error: Dibagi 0"
            self.just_calculated = True
        except Exception:
            self.last_result = "Error: Format Rumus"
            self.current_number = "Error: Format Rumus"
            self.just_calculated = True

    def get_display(self) -> Tuple[str, str]:
        """
        Mengambil teks untuk layar atas (ekspresi) dan layar bawah (hasil).
        Analogi Web: return { expression: this.expression, result: this.current_number }
        """
        return self.expression, self.current_number

    def restore_result(self, val: str):
        """Memulihkan angka dari riwayat ke layar aktif."""
        if "Error" not in val:
            self.current_number = val
            self.expression = ""
            self.just_calculated = False

    def get_history(self) -> List[Dict[str, str]]:
        return self.history

    def _format_number(self, n: float) -> str:
        """Membersihkan angka desimal agar tidak ada trailing zero yang buruk."""
        if isinstance(n, int):
            return str(n)
        if n.is_integer():
            return str(int(n))
        
        formatted = f"{n:.10f}".rstrip("0").rstrip(".")
        if abs(n) >= 1e12 or (abs(n) <= 1e-6 and n != 0):
            formatted = f"{n:.6e}"
        return formatted
