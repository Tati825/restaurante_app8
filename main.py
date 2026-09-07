from servicios.restaurante import Restaurante

def mostrar_menu():
    print("\n" + "=" * 50)
    print("        SISTEMA DE RESTAURANTE")
    print("=" * 50)
    print("1. Registrar producto")
    print("2. Listar productos")
    print("3. Buscar producto")
    print("4. Actualizar producto")
    print("5. Eliminar producto")
    print("6. Registrar usuario")
    print("7. Listar usuarios")
    print("8. Buscar usuario")
    print("9. Registrar venta")
    print("10. Listar ventas")
    print("11. Consultar ventas por usuario")
    print("12. Consultar total de compras de usuario")
    print("13. Eliminar venta")
    print("14. Mostrar categorías")
    print("0. Salir")
    print("=" * 50)


def registrar_producto(restaurante):
    try:
        codigo = input("Código: ")
        nombre = input("Nombre: ")
        categoria = input("Categoría: ")
        precio = float(input("Precio: "))
        stock = int(input("Stock: "))

        producto = restaurante.registrar_producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock
        )

        print("\nProducto registrado correctamente")
        print(producto.mostrar_informacion())

    except ValueError as error:
        print(f"\nError: {error}")


def listar_productos(restaurante):
    productos = restaurante.listar_productos()

    print("\n--- PRODUCTOS ---")

    if not productos:
        print("No existen productos registrados")
        return

    for producto in productos:
        print(producto.mostrar_informacion())


def buscar_producto(restaurante):
    codigo = input("Ingrese el código del producto: ")

    producto = restaurante.buscar_producto(codigo)

    if producto:
        print("\nProducto encontrado:")
        print(producto.mostrar_informacion())
    else:
        print("\nProducto no encontrado")


def actualizar_producto(restaurante):
    try:
        codigo = input("Código del producto a actualizar: ")

        producto = restaurante.buscar_producto(codigo)

        if producto is None:
            print("\nProducto no encontrado")
            return

        print("\nDeje vacío un campo para mantener su valor actual")

        nombre = input(
            f"Nombre [{producto.nombre}]: "
        )

        categoria = input(
            f"Categoría [{producto.categoria}]: "
        )

        precio = input(
            f"Precio [{producto.precio}]: "
        )

        stock = input(
            f"Stock [{producto.stock}]: "
        )

        disponible = input(
            "¿Disponible? (s/n, vacío para mantener): "
        )

        restaurante.actualizar_producto(
            codigo=codigo,
            nombre=nombre if nombre else None,
            categoria=categoria if categoria else None,
            precio=float(precio) if precio else None,
            stock=int(stock) if stock else None,
            disponible=(
                True if disponible.lower() == "s"
                else False if disponible.lower() == "n"
                else None
            )
        )

        print("\nProducto actualizado correctamente")

    except ValueError as error:
        print(f"\nError: {error}")


def eliminar_producto(restaurante):
    try:
        codigo = input("Código del producto: ")

        restaurante.eliminar_producto(codigo)

        print("\nProducto eliminado correctamente")

    except ValueError as error:
        print(f"\nError: {error}")


def registrar_usuario(restaurante):
    try:
        identificacion = input("Identificación: ")
        nombre = input("Nombre: ")
        correo = input("Correo: ")

        usuario = restaurante.registrar_usuario(
            identificacion=identificacion,
            nombre=nombre,
            correo=correo
        )

        print("\nUsuario registrado correctamente")
        print(usuario.mostrar_informacion())

    except ValueError as error:
        print(f"\nError: {error}")


def listar_usuarios(restaurante):
    usuarios = restaurante.listar_usuarios()

    print("\n--- USUARIOS ---")

    if not usuarios:
        print("No existen usuarios registrados")
        return

    for usuario in usuarios:
        print(usuario.mostrar_informacion())


def buscar_usuario(restaurante):
    identificacion = input(
        "Ingrese la identificación del usuario: "
    )

    usuario = restaurante.buscar_usuario(
        identificacion
    )

    if usuario:
        print("\nUsuario encontrado:")
        print(usuario.mostrar_informacion())
    else:
        print("\nUsuario no encontrado")


def registrar_venta(restaurante):
    try:
        codigo_venta = input("Código de venta: ")
        identificacion = input(
            "Identificación del usuario: "
        )
        codigo_producto = input(
            "Código del producto: "
        )
        cantidad = int(
            input("Cantidad: ")
        )

        venta = restaurante.registrar_venta(
            codigo_venta=codigo_venta,
            identificacion_usuario=identificacion,
            codigo_producto=codigo_producto,
            cantidad=cantidad
        )

        print("\nVenta registrada correctamente")
        print(venta.mostrar_informacion())

        producto = restaurante.buscar_producto(
            codigo_producto
        )

        if producto:
            print(
                f"Stock restante: {producto.stock}"
            )

    except ValueError as error:
        print(f"\nError: {error}")


def listar_ventas(restaurante):
    ventas = restaurante.listar_ventas()

    print("\n--- VENTAS ---")

    if not ventas:
        print("No existen ventas registradas")
        return

    for venta in ventas:
        print(venta.mostrar_informacion())


def consultar_ventas_usuario(restaurante):
    identificacion = input(
        "Identificación del usuario: "
    )

    usuario = restaurante.buscar_usuario(
        identificacion
    )

    if usuario is None:
        print("\nUsuario no encontrado.")
        return

    ventas = restaurante.buscar_ventas_por_usuario(
        identificacion
    )

    print(
        f"\n--- VENTAS DE {usuario.nombre} ---"
    )

    if not ventas:
        print("El usuario no tiene ventas registradas")
        return

    for venta in ventas:
        print(venta.mostrar_informacion())


def consultar_total_usuario(restaurante):
    identificacion = input(
        "Identificación del usuario: "
    )

    usuario = restaurante.buscar_usuario(
        identificacion
    )

    if usuario is None:
        print("\nUsuario no encontrado")
        return

    total = restaurante.obtener_total_ventas_usuario(
        identificacion
    )

    print(
        f"\nUsuario: {usuario.nombre}"
    )
    print(
        f"Total de compras: ${total:.2f}"
    )


def eliminar_venta(restaurante):
    try:
        codigo = input(
            "Código de la venta a eliminar: "
        )

        restaurante.eliminar_venta(codigo)

        print(
            "\nVenta eliminada correctamente"
        )
        print(
            "El stock del producto fue restaurado"
        )

    except ValueError as error:
        print(f"\nError: {error}")


def mostrar_categorias(restaurante):
    categorias = restaurante.obtener_categorias()

    print("\n--- CATEGORÍAS ---")

    if not categorias:
        print("No existen categorías.")
        return

    for categoria in sorted(categorias):
        print(f"- {categoria}")


def main():
    restaurante = Restaurante()

    print("\nDatos cargados correctamente.")
    print(
        f"Productos: {len(restaurante.productos)}"
    )
    print(
        f"Usuarios: {len(restaurante.usuarios)}"
    )
    print(
        f"Ventas: {len(restaurante.ventas)}"
    )

    while True:
        mostrar_menu()

        opcion = input(
            "Seleccione una opción: "
        )

        if opcion == "1":
            registrar_producto(restaurante)

        elif opcion == "2":
            listar_productos(restaurante)

        elif opcion == "3":
            buscar_producto(restaurante)

        elif opcion == "4":
            actualizar_producto(restaurante)

        elif opcion == "5":
            eliminar_producto(restaurante)

        elif opcion == "6":
            registrar_usuario(restaurante)

        elif opcion == "7":
            listar_usuarios(restaurante)

        elif opcion == "8":
            buscar_usuario(restaurante)

        elif opcion == "9":
            registrar_venta(restaurante)

        elif opcion == "10":
            listar_ventas(restaurante)

        elif opcion == "11":
            consultar_ventas_usuario(restaurante)

        elif opcion == "12":
            consultar_total_usuario(restaurante)

        elif opcion == "13":
            eliminar_venta(restaurante)

        elif opcion == "14":
            mostrar_categorias(restaurante)

        elif opcion == "0":
            print(
                "\nPrograma finalizado"
            )
            break

        else:
            print(
                "\nOpción no válida"
            )


if __name__ == "__main__":
    main()
