import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox


class MainView:
    def __init__(self, root, restaurante_servicio, cerrar_sesion, logo_path=None):
        self.root = root
        self.restaurante_servicio = restaurante_servicio
        self.cerrar_sesion = cerrar_sesion
        self.logo_path = logo_path
        self.logo = None
        self.icono_usuarios = None
        self.usuario_actual = None
        self.boton_usuarios = None
        self.usuario_identificador_seleccionado = None

        self.frame = ttk.Frame(root, padding=15)

        encabezado = ttk.Frame(self.frame)
        encabezado.pack(fill="x", pady=(0, 12))

        if logo_path:
            try:
                self.logo = tk.PhotoImage(file=str(logo_path))
                ttk.Label(encabezado, image=self.logo).pack(side="left", padx=(0, 8))
            except tk.TclError:
                pass

        ttk.Label(
            encabezado,
            text="RESTAURANTE APP",
            font=("Arial", 20, "bold")
        ).pack(side="left")

        ttk.Button(
            encabezado,
            text="Cerrar sesión",
            command=self.cerrar_sesion
        ).pack(side="right")

        contenido = ttk.Frame(self.frame)
        contenido.pack(fill="both", expand=True)

        navegacion = ttk.LabelFrame(
            contenido,
            text="Navegación",
            padding=10
        )
        navegacion.pack(side="left", fill="y", padx=(0, 12))

        ttk.Button(
            navegacion, text="Inicio", width=18,
            command=self.mostrar_inicio
        ).pack(fill="x", pady=5)

        self.boton_usuarios = ttk.Button(
            navegacion, text="Usuarios", width=18,
            command=self.mostrar_usuarios
        )
        self.boton_usuarios.pack(fill="x", pady=5)

        ttk.Button(
            navegacion, text="Productos", width=18,
            command=self.mostrar_productos
        ).pack(fill="x", pady=5)

        ttk.Button(
            navegacion, text="Ventas", width=18,
            command=self.mostrar_ventas
        ).pack(fill="x", pady=5)

        self.contenido = ttk.Frame(contenido)
        self.contenido.pack(side="left", fill="both", expand=True)

        self.mostrar_inicio()

    def set_usuario_actual(self, usuario):
        self.usuario_actual = usuario
        if self.boton_usuarios is not None:
            if usuario.rol == "Administrador":
                self.boton_usuarios.pack(fill="x", pady=5)
            else:
                self.boton_usuarios.pack_forget()

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
        self.mostrar_inicio()

    def ocultar(self):
        self.frame.pack_forget()

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_contenido()

        ttk.Label(
            self.contenido,
            text="Panel Principal",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        resumen = ttk.LabelFrame(
            self.contenido,
            text="Resumen del sistema",
            padding=20
        )
        resumen.pack(fill="x", padx=10)

        ttk.Label(
            resumen,
            text=f"Productos registrados: {self.restaurante_servicio.cantidad_productos()}"
        ).pack(anchor="w", pady=5)

        ttk.Label(
            resumen,
            text=f"Usuarios registrados: {self.restaurante_servicio.cantidad_usuarios()}"
        ).pack(anchor="w", pady=5)

        ttk.Label(
            resumen,
            text=f"Ventas registradas: {len(self.restaurante_servicio.listar_ventas())}"
        ).pack(anchor="w", pady=5)

        ttk.Label(
            self.contenido,
            text="Seleccione una opción del menú de navegación."
        ).pack(pady=25)

    def mostrar_usuarios(self):
        if self.usuario_actual is None or self.usuario_actual.rol != "Administrador":
            messagebox.showerror("Usuarios", "Solo el administrador puede acceder a la gestión de usuarios.")
            return

        self.limpiar_contenido()

        encabezado_usuarios = ttk.Frame(self.contenido)
        encabezado_usuarios.pack(pady=(0, 12))

        try:
            self.icono_usuarios = tk.PhotoImage(
                file=str(Path(self.logo_path).parent / "icono_usuarios.png")
            )
            ttk.Label(encabezado_usuarios, image=self.icono_usuarios).pack(side="left", padx=(0, 8))
        except (tk.TclError, TypeError):
            pass

        ttk.Label(
            encabezado_usuarios,
            text="Gestión de Usuarios",
            font=("Arial", 18, "bold")
        ).pack(side="left")

        formulario = ttk.LabelFrame(
            self.contenido, text="Datos del usuario", padding=12
        )
        formulario.pack(fill="x", pady=(0, 12))

        ttk.Label(formulario, text="ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.usuario_id_entry = ttk.Entry(formulario, width=20)
        self.usuario_id_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.usuario_nombre_entry = ttk.Entry(formulario, width=28)
        self.usuario_nombre_entry.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Usuario:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.usuario_login_entry = ttk.Entry(formulario, width=20)
        self.usuario_login_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Contraseña:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.usuario_contrasena_entry = ttk.Entry(formulario, width=28, show="*")
        self.usuario_contrasena_entry.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Rol:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.usuario_rol_combo = ttk.Combobox(
            formulario, values=("Empleado", "Cliente"), state="readonly", width=18
        )
        self.usuario_rol_combo.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.usuario_rol_combo.set("Cliente")

        self.usuario_rol_estado = ttk.Label(formulario, text="Rol seleccionado: Cliente")
        self.usuario_rol_estado.grid(row=2, column=2, columnspan=2, sticky="w", padx=5, pady=5)

        botones = ttk.Frame(formulario)
        botones.grid(row=3, column=0, columnspan=4, pady=(10, 0))

        ttk.Button(botones, text="Registrar", command=self.registrar_usuario).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar", command=self.actualizar_usuario).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", command=self.eliminar_usuario).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar", command=self.limpiar_formulario_usuario).pack(side="left", padx=4)

        tabla_frame = ttk.LabelFrame(
            self.contenido, text="Usuarios registrados", padding=8
        )
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("id", "nombre", "usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(
            tabla_frame, columns=columnas, show="headings", height=10
        )
        for columna, texto in ((
            "id", "ID"), ("nombre", "Nombre"),
            ("usuario", "Usuario"), ("rol", "Rol")
        ):
            self.tabla_usuarios.heading(columna, text=texto)

        self.tabla_usuarios.column("id", width=70, anchor="center")
        self.tabla_usuarios.column("nombre", width=200)
        self.tabla_usuarios.column("usuario", width=150)
        self.tabla_usuarios.column("rol", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=scrollbar.set)
        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Semana 16: eventos con bind().
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.al_seleccionar_usuario)
        self.usuario_rol_combo.bind("<<ComboboxSelected>>", self.al_seleccionar_rol)
        self.usuario_rol_combo.bind("<Return>", self.al_presionar_enter)

        for widget in (
            self.usuario_id_entry, self.usuario_nombre_entry,
            self.usuario_login_entry, self.usuario_contrasena_entry,
            self.usuario_rol_combo, self.tabla_usuarios
        ):
            widget.bind("<Escape>", self.al_presionar_escape)

        self.refrescar_usuarios()

    def obtener_datos_usuario(self):
        try:
            id_usuario = int(self.usuario_id_entry.get().strip())
        except ValueError:
            raise ValueError("El ID del usuario debe ser numérico.")

        return (
            id_usuario,
            self.usuario_nombre_entry.get().strip(),
            self.usuario_login_entry.get().strip(),
            self.usuario_contrasena_entry.get(),
            self.usuario_rol_combo.get(),
        )

    def registrar_usuario(self):
        try:
            self.restaurante_servicio.registrar_usuario(*self.obtener_datos_usuario())
            self.refrescar_usuarios()
            self.limpiar_formulario_usuario()
            messagebox.showinfo("Usuarios", "Usuario registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def al_seleccionar_usuario(self, event):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        valores = self.tabla_usuarios.item(seleccion[0], "values")
        if not valores:
            return

        id_usuario = int(valores[0])
        usuario = self.restaurante_servicio.buscar_usuario(id_usuario)
        if usuario is None:
            return

        # El Treeview solo proporciona el identificador; los datos se consultan en el servicio.
        self.usuario_identificador_seleccionado = usuario.id
        for entry, valor in ((
            self.usuario_id_entry, usuario.id),
            (self.usuario_nombre_entry, usuario.nombre),
            (self.usuario_login_entry, usuario.usuario),
            (self.usuario_contrasena_entry, usuario.contrasena),
        ):
            entry.delete(0, tk.END)
            entry.insert(0, str(valor))

        if usuario.id == self.usuario_actual.id and usuario.rol == "Administrador":
            self.usuario_rol_combo.configure(values=("Administrador",), state="disabled")
        else:
            self.usuario_rol_combo.configure(values=("Empleado", "Cliente"), state="readonly")
        self.usuario_rol_combo.set(usuario.rol)
        self.al_seleccionar_rol(None)

    def actualizar_usuario(self):
        if self.usuario_identificador_seleccionado is None:
            messagebox.showerror("Usuarios", "Seleccione un usuario de la tabla.")
            return

        try:
            datos = self.obtener_datos_usuario()
            if datos[0] != self.usuario_identificador_seleccionado:
                raise ValueError("No cambie el ID del usuario seleccionado.")

            self.restaurante_servicio.actualizar_usuario(
                *datos, id_usuario_actual=self.usuario_actual.id
            )
            self.refrescar_usuarios()
            messagebox.showinfo("Usuarios", "Usuario actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def eliminar_usuario(self):
        if self.usuario_identificador_seleccionado is None:
            messagebox.showerror("Usuarios", "Seleccione un usuario de la tabla.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Desea eliminar el usuario seleccionado?"
        )
        if not confirmar:
            return

        try:
            self.restaurante_servicio.eliminar_usuario(
                self.usuario_identificador_seleccionado,
                self.usuario_actual.id
            )
            self.limpiar_formulario_usuario()
            self.refrescar_usuarios()
            messagebox.showinfo("Usuarios", "Usuario eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def limpiar_formulario_usuario(self):
        for entry in (
            self.usuario_id_entry, self.usuario_nombre_entry,
            self.usuario_login_entry, self.usuario_contrasena_entry
        ):
            entry.delete(0, tk.END)

        self.usuario_identificador_seleccionado = None
        self.usuario_rol_combo.configure(values=("Empleado", "Cliente"), state="readonly")
        self.usuario_rol_combo.set("Cliente")
        self.al_seleccionar_rol(None)

        for item in self.tabla_usuarios.selection():
            self.tabla_usuarios.selection_remove(item)

        self.usuario_id_entry.focus()

    def al_presionar_enter(self, event):
        # Reutiliza el método existente: no duplica la lógica de registro.
        self.registrar_usuario()

    def al_presionar_escape(self, event):
        self.limpiar_formulario_usuario()

    def al_seleccionar_rol(self, event):
        rol = self.usuario_rol_combo.get()
        self.usuario_rol_estado.config(text=f"Rol seleccionado: {rol}")

    def refrescar_usuarios(self):
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)

        for usuario in self.restaurante_servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "", "end",
                values=(usuario.id, usuario.nombre, usuario.usuario, usuario.rol)
            )

    def mostrar_productos(self):
        self.limpiar_contenido()

        ttk.Label(
            self.contenido,
            text="Gestión de Productos",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 10))

        formulario = ttk.LabelFrame(
            self.contenido, text="Formulario de producto", padding=12
        )
        formulario.pack(fill="x", pady=(0, 12))

        ttk.Label(formulario, text="ID:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.id_entry = ttk.Entry(formulario, width=20)
        self.id_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Nombre:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.nombre_entry = ttk.Entry(formulario, width=35)
        self.nombre_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Precio:").grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )
        self.precio_entry = ttk.Entry(formulario, width=20)
        self.precio_entry.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Cantidad:").grid(
            row=1, column=2, sticky="w", padx=5, pady=5
        )
        self.cantidad_entry = ttk.Entry(formulario, width=20)
        self.cantidad_entry.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        botones = ttk.Frame(formulario)
        botones.grid(row=2, column=0, columnspan=4, pady=(10, 0))

        ttk.Button(
            botones, text="Registrar", command=self.registrar_producto
        ).pack(side="left", padx=4)
        ttk.Button(
            botones, text="Cargar / Consultar", command=self.cargar_producto
        ).pack(side="left", padx=4)
        ttk.Button(
            botones, text="Actualizar", command=self.actualizar_producto
        ).pack(side="left", padx=4)
        ttk.Button(
            botones, text="Eliminar", command=self.eliminar_producto
        ).pack(side="left", padx=4)
        ttk.Button(
            botones, text="Limpiar", command=self.limpiar_formulario
        ).pack(side="left", padx=4)

        tabla_frame = ttk.LabelFrame(
            self.contenido, text="Productos disponibles", padding=8
        )
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("id", "nombre", "precio", "cantidad")
        self.tabla_productos = ttk.Treeview(
            tabla_frame, columns=columnas, show="headings", height=10
        )

        for columna, texto in (
            ("id", "ID"),
            ("nombre", "Nombre"),
            ("precio", "Precio"),
            ("cantidad", "Cantidad")
        ):
            self.tabla_productos.heading(columna, text=texto)

        self.tabla_productos.column("id", width=60, anchor="center")
        self.tabla_productos.column("nombre", width=220)
        self.tabla_productos.column("precio", width=100, anchor="e")
        self.tabla_productos.column("cantidad", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)

        self.tabla_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.actualizar_tabla()

    def obtener_datos_formulario(self):
        try:
            id_producto = int(self.id_entry.get().strip())
            precio = float(self.precio_entry.get().strip())
            cantidad = int(self.cantidad_entry.get().strip())
        except ValueError:
            raise ValueError("ID, precio y cantidad deben ser valores numéricos.")

        nombre = self.nombre_entry.get().strip()
        return id_producto, nombre, precio, cantidad

    def registrar_producto(self):
        try:
            datos = self.obtener_datos_formulario()
            self.restaurante_servicio.registrar_producto(*datos)
            messagebox.showinfo("Registro", "Producto registrado correctamente.")
            self.actualizar_tabla()
            self.limpiar_formulario()
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def cargar_producto(self):
        try:
            id_producto = int(self.id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un ID válido para consultar.")
            return

        producto = self.restaurante_servicio.buscar_producto(id_producto)

        if producto is None:
            messagebox.showwarning(
                "Consulta", "No se encontró un producto con ese ID."
            )
            return

        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, producto.nombre)
        self.precio_entry.delete(0, tk.END)
        self.precio_entry.insert(0, str(producto.precio))
        self.cantidad_entry.delete(0, tk.END)
        self.cantidad_entry.insert(0, str(producto.cantidad))

    def actualizar_producto(self):
        try:
            datos = self.obtener_datos_formulario()
            self.restaurante_servicio.actualizar_producto(*datos)
            messagebox.showinfo(
                "Actualización", "Producto actualizado correctamente."
            )
            self.actualizar_tabla()
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def eliminar_producto(self):
        try:
            id_producto = int(self.id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un ID válido para eliminar.")
            return

        producto = self.restaurante_servicio.buscar_producto(id_producto)

        if producto is None:
            messagebox.showwarning(
                "Eliminación", "No se encontró un producto con ese ID."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar el producto '{producto.nombre}'?"
        )
        if not confirmar:
            return

        try:
            self.restaurante_servicio.eliminar_producto(id_producto)
            messagebox.showinfo(
                "Eliminación", "Producto eliminado correctamente."
            )
            self.actualizar_tabla()
            self.limpiar_formulario()
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def actualizar_tabla(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto.id,
                    producto.nombre,
                    f"${producto.precio:.2f}",
                    producto.cantidad
                )
            )

    def limpiar_formulario(self):
        for entry in (
            self.id_entry,
            self.nombre_entry,
            self.precio_entry,
            self.cantidad_entry
        ):
            entry.delete(0, tk.END)
        self.id_entry.focus()

    # =========================
    # VENTAS - SEMANA 15
    # =========================
    def mostrar_ventas(self):
        self.limpiar_contenido()

        ttk.Label(
            self.contenido,
            text="Registro de Ventas",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 12))

        formulario = ttk.LabelFrame(
            self.contenido,
            text="Nueva venta",
            padding=15
        )
        formulario.pack(fill="x", pady=(0, 12))

        ttk.Label(
            formulario, text="Usuario:"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=8)

        self.usuario_venta_combo = ttk.Combobox(
            formulario,
            state="readonly",
            width=30
        )
        self.usuario_venta_combo.grid(
            row=0, column=1, sticky="w", padx=5, pady=8
        )

        ttk.Label(
            formulario, text="Producto:"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=8)

        self.producto_venta_combo = ttk.Combobox(
            formulario,
            state="readonly",
            width=30
        )
        self.producto_venta_combo.grid(
            row=1, column=1, sticky="w", padx=5, pady=8
        )

        ttk.Button(
            formulario,
            text="Registrar venta",
            command=self.registrar_venta
        ).grid(
            row=0, column=2, rowspan=2, padx=15, pady=8, ipadx=10, ipady=5
        )

        self.cargar_opciones_venta()

        tabla_frame = ttk.LabelFrame(
            self.contenido,
            text="Ventas registradas",
            padding=8
        )
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("id", "usuario", "producto", "fecha")
        self.tabla_ventas = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=12
        )

        for columna, texto in (
            ("id", "ID"),
            ("usuario", "Usuario"),
            ("producto", "Producto"),
            ("fecha", "Fecha")
        ):
            self.tabla_ventas.heading(columna, text=texto)

        self.tabla_ventas.column("id", width=60, anchor="center")
        self.tabla_ventas.column("usuario", width=160)
        self.tabla_ventas.column("producto", width=220)
        self.tabla_ventas.column("fecha", width=180)

        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_ventas.yview
        )
        self.tabla_ventas.configure(yscrollcommand=scrollbar.set)

        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.actualizar_tabla_ventas()

    def cargar_opciones_venta(self):
        usuarios = self.restaurante_servicio.listar_usuarios()
        productos = self.restaurante_servicio.listar_productos()

        self.usuarios_venta = usuarios
        self.productos_venta = productos

        self.usuario_venta_combo["values"] = [
            f"{usuario.id} - {usuario.usuario}"
            for usuario in usuarios
        ]
        self.producto_venta_combo["values"] = [
            f"{producto.id} - {producto.nombre}"
            for producto in productos
            if producto.cantidad > 0
        ]

        if self.usuario_venta_combo["values"]:
            self.usuario_venta_combo.current(0)

        if self.producto_venta_combo["values"]:
            self.producto_venta_combo.current(0)

    def registrar_venta(self):
        # Este método es el callback asociado a command=.
        try:
            usuario_seleccionado = self.usuario_venta_combo.get()
            producto_seleccionado = self.producto_venta_combo.get()

            if not usuario_seleccionado or not producto_seleccionado:
                raise ValueError(
                    "Seleccione un usuario y un producto antes de registrar la venta."
                )

            id_usuario = int(usuario_seleccionado.split(" - ", 1)[0])
            id_producto = int(producto_seleccionado.split(" - ", 1)[0])

            # La regla y la persistencia están en RestauranteServicio.
            self.restaurante_servicio.registrar_venta(
                id_usuario,
                id_producto
            )

            messagebox.showinfo(
                "Venta registrada",
                "La venta se registró correctamente."
            )

            self.cargar_opciones_venta()
            self.actualizar_tabla_ventas()

        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def actualizar_tabla_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        for venta in self.restaurante_servicio.listar_ventas():
            usuario = self.restaurante_servicio.buscar_usuario(venta.usuario_id)
            producto = self.restaurante_servicio.buscar_producto(venta.producto_id)

            nombre_usuario = usuario.usuario if usuario else "Desconocido"
            nombre_producto = producto.nombre if producto else "Desconocido"

            self.tabla_ventas.insert(
                "",
                "end",
                values=(
                    venta.id,
                    nombre_usuario,
                    nombre_producto,
                    venta.fecha
                )
            )
