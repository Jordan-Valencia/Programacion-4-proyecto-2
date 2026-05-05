# carton_doble.py
from .carton import Carton


class CartonDoble(Carton):
    """
    Representa un cartón doble de bingo: contiene dos grillas independientes
    generadas con los mismos parámetros que el cartón base. 

    Relación:
    - Herencia: CartonDoble es un tipo especializado de Carton. 
    """

    def __init__(self, palabra="BINGO", max_num=75):
        super().__init__(palabra, max_num)
        self.segunda_tarjeta = self.generar_tarjeta()
        self.marcados_segunda = set()

    def marcar_numero(self, numero):
        """
        Marca el número en ambas grillas y devuelve True si se marcó en alguna. 
        """
        marcado_primera = super().marcar_numero(numero)

        marcado_segunda = False
        for fila in self.segunda_tarjeta:
            if numero in fila:
                self.marcados_segunda.add(numero)
                marcado_segunda = True

        return marcado_primera or marcado_segunda

    def tiene_bingo(self):
        """
        Devuelve True si al menos una de las dos grillas tiene bingo. 
        """
        for fila in self.tarjeta:
            for numero in fila:
                if numero not in self.marcados:
                    break
            else:
                continue

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

    def faltantes_grilla(self, primera=True):
        """
        Cuenta cuántos números faltan por marcar en una de las grillas. 
        """
        if primera:
            faltantes = 0
            for fila in self.tarjeta:
                for numero in fila:
                    if numero not in self.marcados:
                        faltantes += 1
            return faltantes
        else:
            faltantes = 0
            for fila in self.segunda_tarjeta:
                for numero in fila:
                    if numero not in self.marcados_segunda:
                        faltantes += 1
            return faltantes

    def grilla_mas_cercana(self):
        """
        Retorna 1 o 2 indicando cuál grilla está más cerca de completarse,
        según la cantidad de casillas marcadas vs totales. 
        """
        faltantes_1 = self.faltantes_grilla(primera=True)
        faltantes_2 = self.faltantes_grilla(primera=False)
        return 1 if faltantes_1 <= faltantes_2 else 2

    def __str__(self):
        """
        Representación en texto de las dos grillas (marcadas con X). 
        """
        lineas = ["=== GRILLA 1 ===", super().__str__(), "", "=== GRILLA 2 ==="]
        encabezado = "   ".join(self.palabra)
        lineas.append(encabezado)
        lineas.append("-" * (self.tam * 4))
        for fila in self.segunda_tarjeta:
            celdas = []
            for numero in fila:
                if numero in self.marcados_segunda:
                    celdas.append(" X")
                else:
                    celdas.append("{:2d}".format(numero))
            lineas.append("  ".join(celdas))
        return "\n".join(lineas)