# jugador.py
from .carton import Carton


class Jugador:
    """
    Representa un jugador que posee uno o más cartones de bingo.

    Relaciones:
    - Agregación con Carton: los cartones existen de forma independiente
      del jugador y pueden reasignarse.
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self._cartones = []
        self.numeros_marcados = 0

    def get_cartones(self):
        return list(self._cartones)

    def agregar_carton(self, carton):
        if carton in self._cartones:
            raise ValueError("El jugador ya tiene ese cartón")
        self._cartones.append(carton)

    def retirar_carton(self, carton):
        self._cartones.remove(carton)

    def notificar_numero(self, numero):
        hay_bingo = False
        for carton in self._cartones:
            marcado = carton.marcar_numero(numero)
            if marcado:
                self.numeros_marcados += 1
            if getattr(carton, "tiene_bingo", None) and carton.tiene_bingo():
                hay_bingo = True
        return hay_bingo