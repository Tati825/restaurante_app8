import json
import os

class ArchivoServicio:
    def __init__(self, carpeta_datos="datos"):
        self.carpeta_datos = carpeta_datos

        os.makedirs(self.carpeta_datos, exist_ok=True)

        self.archivo_productos = os.path.join(
            self.carpeta_datos,
            "productos.json"
        )

        self.archivo_usuarios = os.path.join(
            self.carpeta_datos,
            "usuarios.json"
        )

        self.archivo_ventas = os.path.join(
            self.carpeta_datos,
            "ventas.json"
        )

        self._crear_archivo_si_no_existe(self.archivo_productos)
        self._crear_archivo_si_no_existe(self.archivo_usuarios)
        self._crear_archivo_si_no_existe(self.archivo_ventas)

    def _crear_archivo_si_no_existe(self, ruta):
        if not os.path.exists(ruta):
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump([], archivo, indent=4, ensure_ascii=False)

    def guardar_productos(self, productos):
        datos = [producto.to_dict() for producto in productos]
        self._guardar(self.archivo_productos, datos)

    def cargar_productos(self):
        return self._cargar(self.archivo_productos)

    def guardar_usuarios(self, usuarios):
        datos = [usuario.to_dict() for usuario in usuarios]
        self._guardar(self.archivo_usuarios, datos)

    def cargar_usuarios(self):
        return self._cargar(self.archivo_usuarios)

    def guardar_ventas(self, ventas):
        datos = [venta.to_dict() for venta in ventas]
        self._guardar(self.archivo_ventas, datos)

    def cargar_ventas(self):
        return self._cargar(self.archivo_ventas)

    def _guardar(self, ruta, datos):
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    def _cargar(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)

                if isinstance(contenido, list):
                    return contenido

                return []

        except (json.JSONDecodeError, FileNotFoundError):
            return []
