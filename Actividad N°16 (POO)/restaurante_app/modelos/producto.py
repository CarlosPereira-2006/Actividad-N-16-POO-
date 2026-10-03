class Producto:
    def __init__(self, id: int, nombre: str, precio: float, cantidad: int):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def __str__(self):
        return f"{self.id} - {self.nombre} - ${self.precio:.2f} - Cantidad: {self.cantidad}"
