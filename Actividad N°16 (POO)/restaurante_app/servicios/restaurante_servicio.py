from datetime import datetime

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(
        self,
        archivo_servicio,
        productos,
        usuarios,
        ventas,
        ruta_productos,
        ruta_ventas,
        ruta_usuarios
    ):
        self.archivo_servicio = archivo_servicio
        self.ruta_productos = ruta_productos
        self.ruta_ventas = ruta_ventas
        self.ruta_usuarios = ruta_usuarios

        self.productos = [
            Producto(
                producto["id"],
                producto["nombre"],
                producto["precio"],
                producto["cantidad"]
            )
            for producto in productos
        ]

        self.usuarios = [
            Usuario(
                usuario["id"],
                usuario["usuario"],
                usuario["contraseña"],
                usuario.get("rol", "Cliente"),
                usuario.get("nombre", usuario["usuario"])
            )
            for usuario in usuarios
        ]

        self.ventas = [
            Venta(
                venta["id"],
                venta["usuario_id"],
                venta["producto_id"],
                venta["fecha"]
            )
            for venta in ventas
        ]

    # =========================
    # AUTENTICACIÓN
    # =========================
    def validar_acceso(self, usuario, contrasena):
        for usuario_registrado in self.usuarios:
            if (
                usuario_registrado.usuario == usuario
                and usuario_registrado.contrasena == contrasena
            ):
                return usuario_registrado
        return None

    # =========================
    # PRODUCTOS
    # =========================
    def listar_productos(self):
        return self.productos

    def buscar_producto(self, id_producto):
        for producto in self.productos:
            if producto.id == id_producto:
                return producto
        return None

    def registrar_producto(self, id_producto, nombre, precio, cantidad):
        if self.buscar_producto(id_producto) is not None:
            raise ValueError("Ya existe un producto con ese ID.")

        if not nombre.strip():
            raise ValueError("El nombre del producto es obligatorio.")

        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")

        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        producto = Producto(id_producto, nombre.strip(), precio, cantidad)
        self.productos.append(producto)
        self._guardar_productos()
        return producto

    def actualizar_producto(self, id_producto, nombre, precio, cantidad):
        producto = self.buscar_producto(id_producto)

        if producto is None:
            raise ValueError("No existe un producto con ese ID.")

        if not nombre.strip():
            raise ValueError("El nombre del producto es obligatorio.")

        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")

        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        producto.nombre = nombre.strip()
        producto.precio = precio
        producto.cantidad = cantidad

        self._guardar_productos()
        return producto

    def eliminar_producto(self, id_producto):
        producto = self.buscar_producto(id_producto)

        if producto is None:
            raise ValueError("No existe un producto con ese ID.")

        self.productos.remove(producto)
        self._guardar_productos()

    def _guardar_productos(self):
        datos = [
            {
                "id": producto.id,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "cantidad": producto.cantidad
            }
            for producto in self.productos
        ]
        self.archivo_servicio.guardar_json(self.ruta_productos, datos)

    # =========================
    # USUARIOS - SEMANA 16
    # =========================
    def listar_usuarios(self):
        return self.usuarios

    def buscar_usuario(self, id_usuario):
        for usuario in self.usuarios:
            if usuario.id == id_usuario:
                return usuario
        return None

    def buscar_usuario_por_nombre(self, nombre_usuario):
        nombre_usuario = nombre_usuario.strip()
        for usuario in self.usuarios:
            if usuario.usuario == nombre_usuario:
                return usuario
        return None

    def registrar_usuario(self, id_usuario, nombre, usuario, contrasena, rol):
        if not str(nombre).strip() or not str(usuario).strip() or not str(contrasena).strip():
            raise ValueError("Nombre, usuario y contraseña son obligatorios.")

        nuevo = Usuario(id_usuario, usuario.strip(), contrasena, rol, nombre.strip())

        if nuevo.rol == "Administrador":
            raise ValueError("Solo se pueden registrar usuarios Empleado o Cliente desde esta pantalla.")
        if self.buscar_usuario(nuevo.id) is not None:
            raise ValueError("Ya existe un usuario con ese ID.")
        if self.buscar_usuario_por_nombre(nuevo.usuario) is not None:
            raise ValueError("Ya existe otro usuario con ese nombre de usuario.")

        self.usuarios.append(nuevo)
        self._guardar_usuarios()
        return nuevo

    def actualizar_usuario(self, id_usuario, nombre, usuario, contrasena, rol, id_usuario_actual=None):
        usuario_actual = self.buscar_usuario(id_usuario)
        if usuario_actual is None:
            raise ValueError("No existe un usuario con ese ID.")
        if not str(nombre).strip() or not str(usuario).strip() or not str(contrasena).strip():
            raise ValueError("Nombre, usuario y contraseña son obligatorios.")

        datos = Usuario(id_usuario, usuario.strip(), contrasena, rol, nombre.strip())
        otro = self.buscar_usuario_por_nombre(datos.usuario)
        if otro is not None and otro.id != usuario_actual.id:
            raise ValueError("Ya existe otro usuario con ese nombre de usuario.")

        if usuario_actual.id == id_usuario_actual and usuario_actual.rol == "Administrador" and datos.rol != "Administrador":
            raise ValueError("No puede cambiar el rol del administrador actualmente autenticado.")

        usuario_actual.nombre = datos.nombre
        usuario_actual.usuario = datos.usuario
        usuario_actual.contrasena = datos.contrasena
        usuario_actual.rol = datos.rol
        self._guardar_usuarios()
        return usuario_actual

    def eliminar_usuario(self, id_usuario, id_usuario_actual=None):
        usuario_actual = self.buscar_usuario(id_usuario)
        if usuario_actual is None:
            raise ValueError("No existe un usuario con ese ID.")
        if usuario_actual.id == id_usuario_actual:
            raise ValueError("No puede eliminar el usuario actualmente autenticado.")

        self.usuarios.remove(usuario_actual)
        self._guardar_usuarios()
        return usuario_actual

    def _guardar_usuarios(self):
        datos = [
            {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "usuario": usuario.usuario,
                "contraseña": usuario.contrasena,
                "rol": usuario.rol
            }
            for usuario in self.usuarios
        ]
        self.archivo_servicio.guardar_json(self.ruta_usuarios, datos)

    def cantidad_productos(self):
        return len(self.productos)

    def cantidad_usuarios(self):
        return len(self.usuarios)

    # =========================
    # VENTAS
    # =========================
    def listar_ventas(self):
        return self.ventas

    def registrar_venta(self, id_usuario, id_producto):
        usuario = self.buscar_usuario(id_usuario)
        if usuario is None:
            raise ValueError("El usuario seleccionado no existe.")

        producto = self.buscar_producto(id_producto)
        if producto is None:
            raise ValueError("El producto seleccionado no existe.")

        if producto.cantidad <= 0:
            raise ValueError("El producto seleccionado no tiene disponibilidad.")

        nuevo_id = max((venta.id for venta in self.ventas), default=0) + 1
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        venta = Venta(
            nuevo_id,
            usuario.id,
            producto.id,
            fecha
        )

        self.ventas.append(venta)
        self._guardar_ventas()
        return venta

    def _guardar_ventas(self):
        datos = [
            {
                "id": venta.id,
                "usuario_id": venta.usuario_id,
                "producto_id": venta.producto_id,
                "fecha": venta.fecha
            }
            for venta in self.ventas
        ]
        self.archivo_servicio.guardar_json(self.ruta_ventas, datos)
