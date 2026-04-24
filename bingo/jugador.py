# jugador.py
from __future__ import annotations
from typing import List
from .carton import Carton

class Jugador:
    """
    Representa un jugador que posee uno o más cartones de bingo.

    Relaciones:
    - Agregación con Carton: los cartones existen de forma independiente
      del jugador y pueden reasignarse.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self._cartones: List[Carton] = []
        self.numeros_marcados: int = 0

    def get_cartones(self) -> List[Carton]:
        return list(self._cartones)

    def agregar_carton(self, carton: Carton) -> None:
        if carton in self._cartones:
            raise ValueError("El jugador ya tiene ese cartón")
        self._cartones.append(carton)

    def retirar_carton(self, carton: Carton) -> None:
        self._cartones.remove(carton)

    def notificar_numero(self, numero: int) -> bool:
        hay_bingo = False
        for carton in self._cartones:
            marcado = carton.marcar_numero(numero)
            if marcado:
                self.numeros_marcados += 1
            if getattr(carton, "tiene_bingo", None) and carton.tiene_bingo():
                hay_bingo = True
        return hay_bingo