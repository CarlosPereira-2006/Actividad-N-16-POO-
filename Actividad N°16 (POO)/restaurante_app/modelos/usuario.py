class Usuario:
    ROLES_PERMITIDOS = ("Administrador", "Empleado", "Cliente")

    def __init__(self, id: int, usuario: str, contrasena: str, rol: str = "Cliente", nombre: str = ""):
        self.id = id
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol
        self.nombre = nombre

    @property
    def rol(self):
        return self._rol

    @rol.setter
    def rol(self, valor):
        valor = str(valor).strip()
        if valor not in self.ROLES_PERMITIDOS:
            raise ValueError("El rol seleccionado no es válido.")
        self._rol = valor

    def __str__(self):
        return f"{self.id} - {self.usuario}"
