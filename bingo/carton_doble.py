from .carton import Carton


class CartonDoble(Carton):
    def __init__(self, palabra, tarjeta, segunda_tarjeta):
        super().__init__(palabra, tarjeta)
        self.segunda_tarjeta = segunda_tarjeta
        self.marcados_segunda = set()

    def marcar_numero(self, numero):
        marcado_primera = super().marcar_numero(numero)
        marcado_segunda = False
        for fila in self.segunda_tarjeta:
            if numero in fila:
                self.marcados_segunda.add(numero)
                marcado_segunda = True
        return marcado_primera or marcado_segunda

    def tiene_bingo(self):
        bingo_primera = all(
            numero in self.marcados
            for fila in self.tarjeta
            for numero in fila
        )
        bingo_segunda = all(
            numero in self.marcados_segunda
            for fila in self.segunda_tarjeta
            for numero in fila
        )
        return bingo_primera or bingo_segunda

    def tiene_marcado(self, numero):
        return numero in self.marcados or numero in self.marcados_segunda

    def __str__(self):
        lineas = ["=== GRILLA 1 ===", super().__str__(), "", "=== GRILLA 2 ==="]
        encabezado = "   ".join(self.palabra)
        lineas.append(encabezado)
        lineas.append("-" * (self.tam * 4))
        for fila in self.segunda_tarjeta:
            celdas = [
                " X" if numero in self.marcados_segunda else "{:2d}".format(numero)
                for numero in fila
            ]
            lineas.append("  ".join(celdas))
        return "\n".join(lineas)
