# 📱 PyMobile Calc - Kalkulator Mobile Modular (Flet)

Aplikasi kalkulator mobile modern yang dibangun dengan **Python** dan **Flet** (berbasis Flutter engine), dirancang secara modular menggunakan pola arsitektur yang sangat familiar bagi pengembang web (HTML/CSS/JS).

---

## 🗂️ Struktur 3 Berkas Modular

```
pymobile_calc/
│
├── app/
│   ├── logic.py      # MURNI LOGIKA MATEMATIKA (Zero UI, Model/Service)
│   └── ui.py         # MURNI TAMPILAN VISUAL (Flexbox, Dark Mode, View)
│
├── main.py           # ENTRY POINT & CONTROLLER (Menghubungkan UI & Logic)
├── requirements.txt  # Pustaka Python (mirip package.json)
└── README.md         # Dokumentasi & Panduan
```

---

## 🌐 Tabel Padanan: Konsep Web vs Flet (Python)

| Konsep Web (HTML / CSS / JS) | Padanan di Flet (Python) | Keterangan |
| :--- | :--- | :--- |
| `window` / `document.body` | `page` (`ft.Page`) | Kanvas root aplikasi |
| `<div>` (Generic container) | `ft.Container` | Wadah elemen dengan background, padding, border |
| `display: flex; flex-direction: row` | `ft.Row` | Menata elemen secara horizontal berdampingan |
| `display: flex; flex-direction: column` | `ft.Column` | Menata elemen secara vertikal bertumpuk |
| `<span>` / `<p>` / `<h1>` | `ft.Text` | Elemen teks dengan ukuran font dan warna |
| `<button onClick={...}>` | `ft.Container(on_click=...)` | Tombol sentuh dengan animasi ripple Material |
| `border-radius: 16px;` | `border_radius=16` | Sudut melengkung |
| `background-color: #1E293B;` | `bgcolor="#1E293B"` | Warna latar belakang |
| `setState()` / Re-render DOM | `page.update()` | Memicu pembaruan tampilan ke layar |

---

## 💻 Cara Menjalankan di Komputer Anda (Tahap Uji Coba)

### 1. Buat Lingkungan Virtual (Virtual Environment)
```bash
# Di terminal Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# Di terminal Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate
```

### 2. Pasang Dependensi Flet
```bash
pip install -r requirements.txt
# atau langsung:
pip install flet
```

### 3. Jalankan Aplikasi
```bash
# Menjalankan dengan Python:
python main.py

# Atau gunakan Flet CLI dengan fitur Hot-Reload otomatis saat mengedit kode:
flet run main.py
```

---

## 🤖 Kompilasi ke Android (File APK) & iOS

```bash
# Build file APK siap pasang di HP Android:
flet build apk --project-name "pymobilecalc" --org "com.example.calc"

# Build proyek iOS / IPA (di macOS):
flet build ipa --project-name "pymobilecalc" --org "com.example.calc"
```
