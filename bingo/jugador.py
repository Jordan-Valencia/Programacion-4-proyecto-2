# jugador.py
from __future__ import annotations
from typing import List
from .carton import Carton

class Jugador:
    """
    Representa un jugador que posee uno o más cartones de bingo. [file:1]

    Relaciones:
    - Agregación con Carton: los cartones existen de forma independiente
      del jugador y pueden reasignarse. [file:1]
    """

    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self._cartones: List[Carton] = []
        self._numeros_marcados: int = 0

    @property
    def cartones(self) -> List[Carton]:
        return list(self._cartones)

    @property
    def numeros_marcados(self) -> int:
        return self._numeros_marcados

    def agregar_carton(self, carton: Carton) -> None:
        if carton in self._cartones:
            raise ValueError("El jugador ya tiene ese cartón")
        self._cartones.append(carton)

    def retirar_carton(self, carton: Carton) -> None:
        self._cartones.remove(carton)

    def notificar_numero(self, numero: int) -> bool:
        """
        Marca el número en todos sus cartones.
        Devuelve True si alguno de sus cartones hizo bingo con este número. [file:1]
        """
        hubo_marca = False
        hay_bingo = False
        for carton in self._cartones:
            marcado = carton.marcar_numero(numero)
            if marcado:
                self._numeros_marcados += 1
                hubo_marca = True
            if getattr(carton, "tiene_bingo", None) and carton.tiene_bingo():
                hay_bingo = True
        return hay_bingo