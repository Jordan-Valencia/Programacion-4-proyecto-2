# juego.py
from __future__ import annotations
from typing import List, Optional
from .bombo import Bombo
from .jugador import Jugador

class Juego:
    """
    Director de una partida de bingo. Coordina jugadores y bombo. [file:1]

    Relaciones:
    - Composición con Bombo: crea y controla su Bombo interno. [file:1]
    - Asociación con Jugador: conoce a los jugadores, pero no los crea ni destruye. [file:1]
    """

    def __init__(self, max_numero: int) -> None:
        self._bombo = Bombo(max_numero)
        self._jugadores: List[Jugador] = []
        self._ganador: Optional[Jugador] = None
        self._en_curso: bool = False

    @property
    def bombo(self) -> Bombo:
        return self._bombo

    @property
    def jugadores(self) -> List[Jugador]:
        return list(self._jugadores)

    @property
    def ganador(self) -> Optional[Jugador]:
        return self._ganador

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
        """
        Extrae un número y notifica a todos los jugadores. [file:1]
        Devuelve el ganador si alguien gana en este turno. [file:1]
        """
        if not self._en_curso:
            raise RuntimeError("La partida no está en curso")
        if not self._bombo.hay_numeros():
            self._en_curso = False
            return None

        numero = self._bombo.extraer()
        print(f"\nSe extrajo el número: {numero}")

        for jugador in self._jugadores:
            gano = jugador.notificar_numero(numero)
            if gano and self._ganador is None:
                self._ganador = jugador

        if self._ganador:
            self._en_curso = False
        return self._ganador

    def reporte_final(self) -> None:
        """
        Imprime un reporte al finalizar la partida. [file:1]
        """
        print("\n--- REPORTE FINAL ---")
        if self._ganador:
            print(f"Ganador: {self._ganador.nombre}")
        else:
            print("No hubo ganador.")
        print("Historial de números extraídos:")
        print(self._bombo.historial)
        print("Números marcados por jugador:")
        for jugador in self._jugadores:
            print(f"- {jugador.nombre}: {jugador.numeros_marcados}")