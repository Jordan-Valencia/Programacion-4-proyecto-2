# carton_doble.py
from __future__ import annotations
from typing import List

from .carton import Carton


class CartonDoble(Carton):
    """
    Representa un cartón doble de bingo: contiene dos grillas independientes
    generadas con los mismos parámetros que el cartón base. [file:1]

    Relación:
    - Herencia: CartonDoble es un tipo especializado de Carton. [file:1]
    """

    def __init__(self, palabra: str = "BINGO", max_num: int = 75) -> None:
        # genera la primera tarjeta y toda la configuración base
        super().__init__(palabra, max_num)
        # segunda grilla usando la misma lógica del Carton base
        self.segunda_tarjeta: List[List[int]] = self.generar_tarjeta()
        self.marcados_segunda = set()

    def marcar_numero(self, numero: int) -> bool:
        """
        Marca el número en ambas grillas y devuelve True si se marcó en alguna. [file:1]
        """
        marcado_primera = super().marcar_numero(numero)

        marcado_segunda = False
        for fila in self.segunda_tarjeta:
            if numero in fila:
                self.marcados_segunda.add(numero)
                marcado_segunda = True

        return marcado_primera or marcado_segunda

    def tiene_bingo(self) -> bool:
        """
        Devuelve True si al menos una de las dos grillas tiene bingo. [file:1]
        """
        # bingo en primera
        for fila in self.tarjeta:
            for numero in fila:
                if numero not in self.marcados:
                    break
            else:
                # esta fila está completa, pero el enunciado dice bingo al completar la grilla entera
                # usamos la misma lógica de Carton: todas las casillas marcadas
                continue

        # reusamos la lógica de Carton: todas las casillas marcadas
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

    def faltantes_grilla(self, primera: bool = True) -> int:
        """
        Cuenta cuántos números faltan por marcar en una de las grillas. [file:1]
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

    def grilla_mas_cercana(self) -> int:
        """
        Retorna 1 o 2 indicando cuál grilla está más cerca de completarse,
        según la cantidad de casillas marcadas vs totales. [file:1]
        """
        faltantes_1 = self.faltantes_grilla(primera=True)
        faltantes_2 = self.faltantes_grilla(primera=False)
        return 1 if faltantes_1 <= faltantes_2 else 2

    def __str__(self) -> str:
        """
        Representación en texto de las dos grillas (marcadas con X). [file:1]
        """
        lineas = ["=== GRILLA 1 ===", super().__str__(), "", "=== GRILLA 2 ==="]
        # Imprimimos la segunda usando la misma lógica de Carton pero con sus propios marcados
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