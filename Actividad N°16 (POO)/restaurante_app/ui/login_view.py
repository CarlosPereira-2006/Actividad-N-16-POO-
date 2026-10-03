import tkinter as tk
from tkinter import ttk


class LoginView:
    def __init__(self, root, restaurante_servicio, mostrar_main, logo_path=None):
        self.root = root
        self.restaurante_servicio = restaurante_servicio
        self.mostrar_main = mostrar_main

        self.frame = ttk.Frame(root, padding=30)

        contenedor = ttk.LabelFrame(
            self.frame,
            text="Acceso al sistema",
            padding=25
        )
        contenedor.pack(expand=True)

        if logo_path:
            try:
                self.logo = tk.PhotoImage(file=str(logo_path))
                ttk.Label(contenedor, image=self.logo).grid(
                    row=0, column=0, columnspan=2, pady=(0, 10)
                )
            except tk.TclError:
                pass

        ttk.Label(
            contenedor,
            text="RESTAURANTE APP",
            font=("Arial", 22, "bold")
        ).grid(row=1, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(contenedor, text="Usuario:").grid(
            row=2, column=0, sticky="w", pady=8
        )

        self.usuario_entry = ttk.Entry(contenedor, width=30)
        self.usuario_entry.grid(row=2, column=1, pady=8)

        ttk.Label(contenedor, text="Contraseña:").grid(
            row=3, column=0, sticky="w", pady=8
        )

        # Se usa "contrasena_entry" sin ñ para evitar inconsistencias en identificadores.
        self.contrasena_entry = ttk.Entry(
            contenedor,
            width=30,
            show="*"
        )
        self.contrasena_entry.grid(row=3, column=1, pady=8)

        ttk.Button(
            contenedor,
            text="Ingresar",
            command=self.ingresar
        ).grid(row=4, column=0, columnspan=2, pady=18)

        self.mensaje = ttk.Label(
            contenedor,
            text=""
        )
        self.mensaje.grid(row=5, column=0, columnspan=2)

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
        self.usuario_entry.focus()

    def ocultar(self):
        self.frame.pack_forget()

    def ingresar(self):
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get()

        if not usuario or not contrasena:
            self.mensaje.config(text="Complete todos los campos.")
            return

        acceso = self.restaurante_servicio.validar_acceso(
            usuario,
            contrasena
        )

        if acceso:
            self.mensaje.config(text="")
            self.usuario_entry.delete(0, tk.END)
            self.contrasena_entry.delete(0, tk.END)
            self.ocultar()
            self.mostrar_main(acceso)
        else:
            self.mensaje.config(text="Usuario o contraseña incorrectos.")
