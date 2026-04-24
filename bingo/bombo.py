# bombo.py
from __future__ import annotations
from typing import List
import random

class Bombo:
    """
    Mecanismo de extracción de números de una partida de bingo. [file:1]

    Relación:
    - Composición con Juego: el Bombo es parte constitutiva del Juego y
      su ciclo de vida está ligado al del Juego. [file:1]
    """

    def __init__(self, max_numero: int) -> None:
        if max_numero <= 0:
            raise ValueError("max_numero debe ser positivo")
        self._disponibles: List[int] = list(range(1, max_numero + 1))
        self._historial: List[int] = []

    @property
    def historial(self) -> List[int]:
        return list(self._historial)

    def hay_numeros(self) -> bool:
        return len(self._disponibles) > 0

    def extraer(self) -> int:
        """
        Extrae un número aleatorio sin repetición y lo guarda en el historial. [file:1]
        """
        if not self._disponibles:
            raise RuntimeError("No quedan números en el bombo")
        numero = random.choice(self._disponibles)
        self._disponibles.remove(numero)
        self._historial.append(numero)
        return numero