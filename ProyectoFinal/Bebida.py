class Bebida:

    def __init__(self,nombre,precio,tipo,alcoholica,cantidad):
        self.nombre=nombre
        self.precio=precio
        self.tipo=tipo
        self.alcoholica=alcoholica
        self.cantidad=cantidad

    def mostrar(self):
        print(f" - Nombre: {self.nombre} || Precio: ${self.precio} || Tipo: {self.tipo} || Alcoholica: {self.alcoholica} \n")

