import random


class Bombo:
    def __init__(self, max_numero):
        if max_numero <= 0:
            raise ValueError("El maximo numero debe ser positivo.")
        self._disponibles = list(range(1, max_numero + 1))
        self.historial = []

    def hay_numeros(self):
        return len(self._disponibles) > 0

    def extraer(self):
        if not self._disponibles:
            raise RuntimeError("No quedan numeros en el bombo.")
        numero = random.choice(self._disponibles)
        self._disponibles.remove(numero)
        self.historial.append(numero)
        return numero

    def numeros_restantes(self):
        return len(self._disponibles)
