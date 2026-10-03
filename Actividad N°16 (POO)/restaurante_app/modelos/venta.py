class Venta:
    def __init__(self, id: int, usuario_id: int, producto_id: int, fecha: str):
        self.id = id
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.fecha = fecha

    def __str__(self):
        return f"{self.id} - Usuario {self.usuario_id} - Producto {self.producto_id} - {self.fecha}"
