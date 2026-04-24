# juego.py
from __future__ import annotations
from typing import List, Optional
from .bombo import Bombo
from .jugador import Jugador

class Juego:
    """
    Director de una partida de bingo. Coordina jugadores y bombo.

    Relaciones:
    - Composición con Bombo: crea y controla su Bombo interno.
    - Asociación con Jugador: conoce a los jugadores, pero no los crea ni destruye.
    """

    def __init__(self, max_numero: int) -> None:
        self.bombo: Bombo = Bombo(max_numero)
        self._jugadores: List[Jugador] = []
        self.ganador: Optional[Jugador] = None
        self._en_curso: bool = False

    def get_jugadores(self) -> List[Jugador]:
        return list(self._jugadores)

    def registrar_jugador(self, jugador: Jugador) -> None:
        if jugador in self._jugadores:
            raise ValueError("Jugador ya registrado")
        self._jugadores.append(jugador)

    def dar_de_baja_jugador(self, jugador: Jugador) -> None:
        self._jugadores.remove(jugador)

    def iniciar(self) -> None:
        if not self._jugadores:
            raise RuntimeError("No hay jugadores registrados")
        self._en_curso = True

    def ejecutar_turno(self) -> Optional[Jugador]:
        if not self._en_curso:
            raise RuntimeError("La partida no está en curso")
        if not self.bombo.hay_numeros():
            self._en_curso = False
            return None

        numero = self.bombo.extraer()

        for jugador in self._jugadores:
            gano = jugador.notificar_numero(numero)
            if gano and self.ganador is None:
                self.ganador = jugador

        if self.ganador:
            self._en_curso = False
        return self.ganador

    def reporte_final(self) -> None:
        print("\n" + "=" * 40)
        print("          REPORTE FINAL")
        print("=" * 40)
        if self.ganador:
            print(f"Ganador: {self.ganador.nombre}")
        else:
            print("No hubo ganador.")
        print(f"\nNúmeros extraídos ({len(self.bombo.historial)} en total):")
        print(self.bombo.historial)
        print("\nNúmeros marcados por jugador:")
        for jugador in self._jugadores:
            print(f"  - {jugador.nombre}: {jugador.numeros_marcados}")