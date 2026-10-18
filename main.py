import flet as ft

def main(page: ft.Page):
    page.title = "CALCULATE"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.add(
        ft.Text("TES BERHASIL!", size=30, color="green", weight=ft.FontWeight.BOLD),
        ft.Text("Mesin Flet berjalan normal di HP ini.", size=15)
    )

if __name__ == "__main__":
    ft.app(target=main)