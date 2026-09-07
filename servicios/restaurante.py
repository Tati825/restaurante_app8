from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class Restaurante:
    def __init__(self):
        #Colecciones principales
        self.productos = []
        self.usuarios = []
        self.ventas = []

        #Índices en memoria
        self.productos_por_codigo = {}
        self.usuarios_por_identificacion = {}
        self.ventas_por_usuario = {}

        #Servicio de persistencia
        self.archivo_servicio = ArchivoServicio()

        #Cargar información desde JSON
        self.cargar_datos()

        #Reconstrucción de índices
        self.reconstruir_indices()

    def cargar_datos(self):
        datos_productos = self.archivo_servicio.cargar_productos()
        datos_usuarios = self.archivo_servicio.cargar_usuarios()
        datos_ventas = self.archivo_servicio.cargar_ventas()

        self.productos = [
            Producto.from_dict(datos)
            for datos in datos_productos
        ]

        self.usuarios = [
            Usuario.from_dict(datos)
            for datos in datos_usuarios
        ]

        self.ventas = [
            Venta.from_dict(datos)
            for datos in datos_ventas
        ]

    #Índices
    def reconstruir_indices(self):
        self.productos_por_codigo = {
            producto.codigo: producto
            for producto in self.productos
        }

        self.usuarios_por_identificacion = {
            usuario.identificacion: usuario
            for usuario in self.usuarios
        }

        self.ventas_por_usuario = {}

        for venta in self.ventas:
            identificacion = venta.identificacion_usuario

            if identificacion not in self.ventas_por_usuario:
                self.ventas_por_usuario[identificacion] = []

            self.ventas_por_usuario[identificacion].append(venta)

    #Productos
    def registrar_producto(
        self,
        codigo,
        nombre,
        categoria,
        precio,
        stock,
        disponible=True
    ):
        if codigo in self.productos_por_codigo:
            raise ValueError(
                "Ya existe un producto con ese código"
            )

        producto = Producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            disponible=disponible,
            stock=stock
        )

        #Colección principal
        self.productos.append(producto)

        #Actualizar índice
        self.productos_por_codigo[producto.codigo] = producto

        #Los cambios persisten
        self.archivo_servicio.guardar_productos(self.productos)

        return producto

    def buscar_producto(self, codigo):
        return self.productos_por_codigo.get(str(codigo).strip())

    def listar_productos(self):
        return self.productos

    def actualizar_producto(
        self,
        codigo,
        nombre=None,
        categoria=None,
        precio=None,
        stock=None,
        disponible=None
    ):
        producto = self.buscar_producto(codigo)

        if producto is None:
            raise ValueError("Producto no encontrado")

        if nombre is not None:
            producto.nombre = nombre

        if categoria is not None:
            producto.categoria = categoria

        if precio is not None:
            producto.precio = precio

        if stock is not None:
            producto.stock = stock

        if disponible is not None:
            producto.disponible = disponible

        self.productos_por_codigo[producto.codigo] = producto

        self.archivo_servicio.guardar_productos(self.productos)

        return producto

    def eliminar_producto(self, codigo):
        producto = self.buscar_producto(codigo)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        #Evitar eliminar un producto utilizado en una venta
        for venta in self.ventas:
            if venta.codigo_producto == producto.codigo:
                raise ValueError(
                    "No se puede eliminar el producto porque tiene ventas registradas"
                )

        #Eliminar de la colección principal
        self.productos.remove(producto)

        #Eliminar del índice
        del self.productos_por_codigo[producto.codigo]

        #Los cambios persisten
        self.archivo_servicio.guardar_productos(self.productos)

        return True

    #Usuarios
    def registrar_usuario(
        self,
        identificacion,
        nombre,
        correo
    ):
        if identificacion in self.usuarios_por_identificacion:
            raise ValueError(
                "Ya existe un usuario con esa identificación"
            )

        usuario = Usuario(
            identificacion=identificacion,
            nombre=nombre,
            correo=correo
        )

        #Colección principal
        self.usuarios.append(usuario)

        #Actualizar índice
        self.usuarios_por_identificacion[
            usuario.identificacion
        ] = usuario

        #Los cambios persisten
        self.archivo_servicio.guardar_usuarios(self.usuarios)

        return usuario

    def buscar_usuario(self, identificacion):
        return self.usuarios_por_identificacion.get(
            str(identificacion).strip()
        )

    def listar_usuarios(self):
        return self.usuarios

    def actualizar_usuario(
        self,
        identificacion,
        nombre=None,
        correo=None
    ):
        usuario = self.buscar_usuario(identificacion)

        if usuario is None:
            raise ValueError("Usuario no encontrado")

        if nombre is not None:
            usuario.nombre = nombre

        if correo is not None:
            usuario.correo = correo

        self.usuarios_por_identificacion[
            usuario.identificacion
        ] = usuario

        self.archivo_servicio.guardar_usuarios(self.usuarios)

        return usuario

    def eliminar_usuario(self, identificacion):
        usuario = self.buscar_usuario(identificacion)

        if usuario is None:
            raise ValueError("Usuario no encontrado.")

        # No eliminar usuarios que tengan ventas
        if identificacion in self.ventas_por_usuario:
            if len(self.ventas_por_usuario[identificacion]) > 0:
                raise ValueError(
                    "No se puede eliminar el usuario porque "
                    "tiene ventas registradas."
                )

        self.usuarios.remove(usuario)

        del self.usuarios_por_identificacion[
            usuario.identificacion
        ]

        self.archivo_servicio.guardar_usuarios(self.usuarios)

        return True

    #Ventas
    def registrar_venta(
        self,
        codigo_venta,
        identificacion_usuario,
        codigo_producto,
        cantidad
    ):
        #Verificar que no exista la venta
        if any(
            venta.codigo_venta == codigo_venta
            for venta in self.ventas
        ):
            raise ValueError(
                "Ya existe una venta con ese código."
            )

        #Buscar usuario utilizando el índice
        usuario = self.buscar_usuario(identificacion_usuario)

        if usuario is None:
            raise ValueError(
                "El usuario no existe."
            )

        #Buscar producto utilizando el índice
        producto = self.buscar_producto(codigo_producto)

        if producto is None:
            raise ValueError(
                "El producto no existe."
            )

        cantidad = int(cantidad)

        if cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que 0"
            )

        #Verificar stock
        if producto.stock < cantidad:
            raise ValueError(
                f"Stock insuficiente. "
                f"Stock disponible: {producto.stock}"
            )

        #Crear venta
        venta = Venta(
            codigo_venta=codigo_venta,
            identificacion_usuario=usuario.identificacion,
            codigo_producto=producto.codigo,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )

        #Descontar del stock
        producto.stock -= cantidad

        if producto.stock == 0:
            producto.disponible = False

        #Agregar a la colección principal
        self.ventas.append(venta)

        #Actualizar índice de ventas por usuario
        if usuario.identificacion not in self.ventas_por_usuario:
            self.ventas_por_usuario[usuario.identificacion] = []

        self.ventas_por_usuario[
            usuario.identificacion
        ].append(venta)

        #Los cambios persisten
        self.archivo_servicio.guardar_ventas(self.ventas)
        self.archivo_servicio.guardar_productos(self.productos)

        return venta

    def listar_ventas(self):
        return self.ventas

    def buscar_venta(self, codigo_venta):
        for venta in self.ventas:
            if venta.codigo_venta == codigo_venta:
                return venta

        return None

    def buscar_ventas_por_usuario(self, identificacion):
        return self.ventas_por_usuario.get(
            str(identificacion).strip(),
            []
        )

    def eliminar_venta(self, codigo_venta):
        venta = self.buscar_venta(codigo_venta)

        if venta is None:
            raise ValueError("Venta no encontrada")

        producto = self.buscar_producto(venta.codigo_producto)

        if producto is not None:
            producto.stock += venta.cantidad
            producto.disponible = True

        # liminar de la colección principal
        self.ventas.remove(venta)

        #Eliminar del índice de ventas por usuario
        identificacion = venta.identificacion_usuario

        if identificacion in self.ventas_por_usuario:
            self.ventas_por_usuario[identificacion].remove(venta)

            if len(self.ventas_por_usuario[identificacion]) == 0:
                del self.ventas_por_usuario[identificacion]

        #Los cambios persisten
        self.archivo_servicio.guardar_ventas(self.ventas)
        self.archivo_servicio.guardar_productos(self.productos)

        return True

    #Se realizan las siguientes consultas
    def obtener_productos_disponibles(self):
        return [
            producto
            for producto in self.productos
            if producto.disponible and producto.stock > 0
        ]

    def obtener_categorias(self):
        return {
            producto.categoria
            for producto in self.productos
        }

    def obtener_total_ventas_usuario(self, identificacion):
        ventas_usuario = self.buscar_ventas_por_usuario(
            identificacion
        )

        return sum(
            venta.total
            for venta in ventas_usuario
        )
