class Ambulancia():
    def __init__(self, id, tipo, congelador):
        self.id = id
        self.tipo = tipo
        self.congelador = congelador

    # Este método permite comparar las instancias de Ambulancia usando el operador <
    def __lt__(self, other):
        return self.id < other.id