import flet as ft
import traceback # <--- Tambahkan ini untuk membaca error

# (Import Anda yang lain seperti app.logic dan app.ui biarkan saja di sini)

def main(page: ft.Page):
    try:
        page.title = "CALCULATE"
        
        # --- PINDAHKAN SELURUH KODE ASLI ANDA KE SINI ---
        # (Pastikan spasinya menjorok ke dalam agar masuk ke blok try)
        # 
        # Contoh:
        # exp, res = calc_logic.get_display()
        # calc_ui.update_display(exp, res)
        # page.update()
        
    except Exception as e:
        # Jika aplikasi crash, layarnya tidak akan hitam, 
        # melainkan menampilkan tulisan merah berisi penyebab error-nya:
        page.scroll = "auto"
        page.add(ft.Text(f"Telah Terjadi Error:\n\n{traceback.format_exc()}", color="red"))
        page.update()

if __name__ == "__main__":
    ft.app(target=main)