class Producto:
    def __init__(self, codigo, nombre, categoria, precio, disponible=True, stock=0):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.disponible = disponible
        self.stock = stock

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El código del producto no puede estar vacío")

        self._codigo = str(valor).strip()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El nombre del producto no puede estar vacío")

        self._nombre = str(valor).strip()

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("La categoría no puede estar vacía")

        self._categoria = str(valor).strip()

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        valor = float(valor)

        if valor <= 0:
            raise ValueError("El precio debe ser mayor que 0")

        self._precio = valor

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        valor = int(valor)

        if valor < 0:
            raise ValueError("El stock no puede ser negativo")

        self._stock = valor

    def mostrar_informacion(self):
        estado = "Disponible" if self.disponible else "No disponible"

        return (
            f"Código: {self.codigo} | "
            f"Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | "
            f"Precio: ${self.precio:.2f} | "
            f"Stock: {self.stock} | "
            f"Estado: {estado}"
        )

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "disponible": self.disponible,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            categoria=datos["categoria"],
            precio=datos["precio"],
            disponible=datos.get("disponible", True),
            stock=datos.get("stock", 0)
        )
