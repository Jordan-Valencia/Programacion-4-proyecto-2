from .bombo import Bombo
from .excepciones import JuegoError

# ANTES (DIP): self.bombo y self.ganador eran publicos;
#   main.py accedia directo: juego.bombo.historial, juego.ganador
# AHORA: _bombo privado, _ganadores privado, acceso por getters.
class Juego:
    def __init__(self, max_numero):
        self._bombo = Bombo(max_numero)
        self._jugadores = []
        self._ganadores = []
        self._en_curso = False

    def get_jugadores(self):
        return list(self._jugadores)

    def get_ganador(self):
        return self._ganadores[0] if self._ganadores else None

    def get_ganadores(self):
        return list(self._ganadores)

    def get_historial_numeros(self):
        return list(self._bombo.historial)

    def hay_numeros_disponibles(self):
        return self._bombo.hay_numeros()

    def get_numero_actual(self):
        if not self._bombo.historial:
            return None
        return self._bombo.historial[-1]

    def esta_en_curso(self):
        return self._en_curso

    def registrar_jugador(self, jugador):
        if jugador in self._jugadores:
            raise ValueError("Jugador ya registrado.")
        self._jugadores.append(jugador)

    def dar_de_baja_jugador(self, jugador):
        if jugador not in self._jugadores:
            raise ValueError("Jugador no esta registrado.")
        self._jugadores.remove(jugador)

    def iniciar(self):
        if len(self._jugadores) < 3:
            raise JuegoError("Se necesitan al menos 3 jugadores para iniciar.")
        self._en_curso = True

    def ejecutar_turno(self):
        if not self._en_curso:
            raise JuegoError("La partida no esta en curso.")
        if not self._bombo.hay_numeros():
            self._en_curso = False
            return None

        numero = self._bombo.extraer()

        for jugador in self._jugadores:
            gano = jugador.notificar_numero(numero)
            if gano and jugador not in self._ganadores:
                self._ganadores.append(jugador)

        if self._ganadores:
            self._en_curso = False

        return numero
