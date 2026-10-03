# Restaurante App - Semana 16

Aplicación de escritorio desarrollada en Python con Tkinter/ttk. Esta versión continúa directamente el proyecto de la Semana 15 y amplía la sección **Usuarios** para demostrar el manejo de eventos mediante `bind()`, callbacks y persistencia JSON.

## Objetivo de la Semana 16

Evidenciar el flujo:

```text
interacción del usuario
      ↓
evento
      ↓
bind()
      ↓
callback(event)
      ↓
RestauranteServicio
      ↓
persistencia en usuarios.json
      ↓
respuesta visual
```

La interfaz captura las interacciones, pero las validaciones, reglas y operaciones de usuarios permanecen en `RestauranteServicio`.

## Funcionalidades conservadas

- Inicio de sesión.
- Navegación por Inicio, Usuarios, Productos y Ventas.
- Registro, consulta, actualización y eliminación de productos.
- Registro de ventas.
- Persistencia mediante archivos JSON.
- Uso de `command=` en botones.

## Semana 16: gestión de usuarios

La entidad `Usuario` incorpora el atributo `rol`, con tres valores: `Administrador`, `Empleado` y `Cliente`.

La cuenta `Administrador` puede acceder a la gestión administrativa de usuarios. Desde esa pantalla se pueden gestionar usuarios `Empleado` y `Cliente`. Los usuarios que no son administradores no muestran la opción de gestión de usuarios.

### CRUD de usuarios

- Registrar usuarios.
- Consultar usuarios mediante selección en `Treeview`.
- Actualizar usuarios.
- Eliminar usuarios con confirmación.
- Evitar eliminar la cuenta actualmente autenticada.
- Evitar registrar nuevos administradores desde el formulario.

### Eventos implementados

**Treeview:**

```text
selección de fila
      ↓
<<TreeviewSelect>>
      ↓
bind()
      ↓
al_seleccionar_usuario(event)
      ↓
obtener ID
      ↓
RestauranteServicio.buscar_usuario()
      ↓
cargar datos en formulario
```

**Teclado:**

- `<Return>` registra reutilizando `registrar_usuario()`.
- `<Escape>` limpia el formulario y cancela la selección.

**Combobox:**

- `<<ComboboxSelected>>` actualiza visualmente el rol seleccionado.

**Botones:**

- `Registrar`, `Actualizar`, `Eliminar` y `Limpiar` utilizan `command=`.

## Arquitectura

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logo.png
│   ├── icono_usuarios.png
│   ├── icono_productos.png
│   └── icono_ventas.png
├── main.py
└── README.md
```

## Separación de responsabilidades

- **Modelos:** representan Usuario, Producto y Venta.
- **ArchivoServicio:** lee y escribe JSON.
- **RestauranteServicio:** valida datos, aplica reglas de negocio y persiste usuarios, productos y ventas.
- **LoginView:** captura las credenciales y obtiene el usuario autenticado mediante el servicio.
- **MainView:** presenta la interfaz y coordina los callbacks y eventos.
- **main.py:** inicializa y conecta los componentes.

La interfaz no lee ni escribe directamente los archivos JSON.

## Usuarios de prueba

- Administrador: `admin` / `1234`
- Empleado: `cajero` / `1234`

## Comprobación

1. Ejecutar `python main.py`.
2. Iniciar sesión con `admin / 1234`.
3. Entrar a **Usuarios**.
4. Registrar un usuario `Cliente` o `Empleado`.
5. Seleccionar una fila y comprobar que `<<TreeviewSelect>>` carga sus datos.
6. Actualizar un dato y verificar el cambio.
7. Eliminar un usuario y confirmar la operación.
8. Intentar eliminar la cuenta administrativa actualmente autenticada y comprobar que el servicio lo impide.
9. Usar `Enter` desde el Combobox de rol para registrar reutilizando el método existente.
10. Usar `Escape` para limpiar formulario y selección.
11. Cambiar el rol y comprobar `<<ComboboxSelected>>`.
12. Cerrar sesión e iniciar con `cajero / 1234`; la opción **Usuarios** no debe estar disponible.
13. Cerrar y volver a ejecutar la aplicación para verificar la recuperación desde `usuarios.json`.
14. Comprobar que Productos y Ventas continúan funcionando.

## Ejecución

Desde la carpeta `restaurante_app`:

```bash
python main.py
```

## Evolución del proyecto

```text
Semana 15: acción → command= → callback → servicio → persistencia → respuesta visual
Semana 16: interacción → evento → bind() → callback(event) → servicio → persistencia → respuesta visual
```
