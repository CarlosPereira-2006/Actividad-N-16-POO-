import tkinter as tk
from pathlib import Path

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


def main():
    base_dir = Path(__file__).resolve().parent

    root = tk.Tk()
    root.title("Restaurante App - Semana 16")
    root.geometry("1050x700")
    root.minsize(900, 620)

    archivo_servicio = ArchivoServicio()

    ruta_productos = base_dir / "datos" / "productos.json"
    ruta_usuarios = base_dir / "datos" / "usuarios.json"
    ruta_ventas = base_dir / "datos" / "ventas.json"
    ruta_logo = base_dir / "assets" / "logo.png"

    productos = archivo_servicio.leer_json(ruta_productos)
    usuarios = archivo_servicio.leer_json(ruta_usuarios)
    ventas = archivo_servicio.leer_json(ruta_ventas)

    restaurante_servicio = RestauranteServicio(
        archivo_servicio,
        productos,
        usuarios,
        ventas,
        ruta_productos,
        ruta_ventas,
        ruta_usuarios
    )

    main_view = None

    def mostrar_main(usuario_actual):
        main_view.set_usuario_actual(usuario_actual)
        main_view.ocultar()
        main_view.mostrar()

    def cerrar_sesion():
        main_view.ocultar()
        login_view.mostrar()

    main_view = MainView(
        root,
        restaurante_servicio,
        cerrar_sesion,
        ruta_logo
    )

    login_view = LoginView(
        root,
        restaurante_servicio,
        mostrar_main,
        ruta_logo
    )

    login_view.mostrar()

    root.mainloop()


if __name__ == "__main__":
    main()
