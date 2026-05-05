# juego.py
from .bombo import Bombo
from .jugador import Jugador


class Juego:
    """
    Director de una partida de bingo. Coordina jugadores y bombo.

    Relaciones:
    - Composición con Bombo: crea y controla su Bombo interno.
    - Asociación con Jugador: conoce a los jugadores, pero no los crea ni destruye.
    """

    def __init__(self, max_numero):
        self.bombo = Bombo(max_numero)
        self._jugadores = []
        self.ganadores = []
        self._en_curso = False

    def get_jugadores(self):
        return list(self._jugadores)

    def registrar_jugador(self, jugador):
        if jugador in self._jugadores:
            raise ValueError("Jugador ya registrado")
        self._jugadores.append(jugador)

    def dar_de_baja_jugador(self, jugador):
        self._jugadores.remove(jugador)

    def iniciar(self):
        if not self._jugadores:
            raise RuntimeError("No hay jugadores registrados")
        self._en_curso = True

    def ejecutar_turno(self):
        if not self._en_curso:
            raise RuntimeError("La partida no está en curso")
        if not self.bombo.hay_numeros():
            self._en_curso = False
            return None

        numero = self.bombo.extraer()

        for jugador in self._jugadores:
            gano = jugador.notificar_numero(numero)
            if gano and jugador not in self.ganadores:
                self.ganadores.append(jugador)

        if self.ganadores:
            self._en_curso = False
        return self.ganadores

    def reporte_final(self):
        print("\n" + "=" * 40)
        print("          REPORTE FINAL")
        print("=" * 40)
        if self.ganadores:
            if len(self.ganadores) == 1:
                print(f"Ganador: {self.ganadores[0].nombre}")
            else:
                print("Ganadores:")
                for g in self.ganadores:
                    print(f"  - {g.nombre}")
        else:
            print("No hubo ganador.")
        print(f"\nNúmeros extraídos ({len(self.bombo.historial)} en total):")
        print(self.bombo.historial)
        print("\nNúmeros marcados por jugador:")
        for jugador in self._jugadores:
            print(f"  - {jugador.nombre}: {jugador.numeros_marcados}")