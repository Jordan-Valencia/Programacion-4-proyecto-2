# bombo.py
import random


class Bombo:
    """
    Mecanismo de extracción de números de una partida de bingo.

    Relación:
    - Composición con Juego: el Bombo es parte constitutiva del Juego y
      su ciclo de vida está ligado al del Juego.
    """

    def __init__(self, max_numero):
        if max_numero <= 0:
            raise ValueError("max_numero debe ser positivo")
        self._disponibles = list(range(1, max_numero + 1))
        self.historial = []

    def hay_numeros(self):
        return len(self._disponibles) > 0

    def extraer(self):
        if not self._disponibles:
            raise RuntimeError("No quedan números en el bombo")
        numero = random.choice(self._disponibles)
        self._disponibles.remove(numero)
        self.historial.append(numero)
        return numero