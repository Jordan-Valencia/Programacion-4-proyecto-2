class Carton:
    def __init__(self, palabra, tarjeta):
        self.palabra = palabra.upper()
        self.tam = len(self.palabra)
        self.tarjeta = tarjeta
        self.marcados = set()

    def marcar_numero(self, numero):
        for fila in self.tarjeta:
            if numero in fila:
                self.marcados.add(numero)
                return True
        return False

    def tiene_bingo(self):
        for fila in self.tarjeta:
            for numero in fila:
                if numero not in self.marcados:
                    return False
        return True

    def tiene_marcado(self, numero):
        return numero in self.marcados

    def __str__(self):
        lineas = ["   ".join(self.palabra), "-" * (self.tam * 4)]
        for fila in self.tarjeta:
            celdas = [
                " X" if numero in self.marcados else "{:2d}".format(numero)
                for numero in fila
            ]
            lineas.append("  ".join(celdas))
        return "\n".join(lineas)
