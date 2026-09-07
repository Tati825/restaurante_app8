class Venta:
    def __init__(
        self,
        codigo_venta,
        identificacion_usuario,
        codigo_producto,
        cantidad,
        precio_unitario,
        total=None
    ):
        self.codigo_venta = codigo_venta
        self.identificacion_usuario = identificacion_usuario
        self.codigo_producto = codigo_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

        if total is None:
            self.total = self.cantidad * self.precio_unitario
        else:
            self.total = float(total)

    @property
    def codigo_venta(self):
        return self._codigo_venta

    @codigo_venta.setter
    def codigo_venta(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El código de venta no puede estar vacío")

        self._codigo_venta = str(valor).strip()

    @property
    def identificacion_usuario(self):
        return self._identificacion_usuario

    @identificacion_usuario.setter
    def identificacion_usuario(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("La identificación del usuario es obligatoria")

        self._identificacion_usuario = str(valor).strip()

    @property
    def codigo_producto(self):
        return self._codigo_producto

    @codigo_producto.setter
    def codigo_producto(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El código del producto es obligatorio")

        self._codigo_producto = str(valor).strip()

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        valor = int(valor)

        if valor <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")

        self._cantidad = valor

    @property
    def precio_unitario(self):
        return self._precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, valor):
        valor = float(valor)

        if valor <= 0:
            raise ValueError("El precio unitario debe ser mayor que 0")

        self._precio_unitario = valor

    def mostrar_informacion(self):
        return (
            f"Venta: {self.codigo_venta} | "
            f"Usuario: {self.identificacion_usuario} | "
            f"Producto: {self.codigo_producto} | "
            f"Cantidad: {self.cantidad} | "
            f"Precio unitario: ${self.precio_unitario:.2f} | "
            f"Total: ${self.total:.2f}"
        )

    def to_dict(self):
        return {
            "codigo_venta": self.codigo_venta,
            "identificacion_usuario": self.identificacion_usuario,
            "codigo_producto": self.codigo_producto,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "total": self.total
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            codigo_venta=datos["codigo_venta"],
            identificacion_usuario=datos["identificacion_usuario"],
            codigo_producto=datos["codigo_producto"],
            cantidad=datos["cantidad"],
            precio_unitario=datos["precio_unitario"],
            total=datos.get("total")
        )
