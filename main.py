# main.py
from bingo.carton import Carton
from bingo.carton_doble import CartonDoble
from bingo.jugador import Jugador
from bingo.juego import Juego

def crear_cartones_demo():
    # Aquí se usa la implementación real del bingo de la práctica 1
    c1 = Carton("BINGO", 75)
    c2 = Carton("BINGO", 75)
    c3 = Carton("BINGO", 75)
    cdoble = CartonDoble("BINGO", 75)
    return c1, c2, c3, cdoble

def main():
    juego = Juego(max_numero=75)

    j1 = Jugador("Alice")
    j2 = Jugador("Bob")
    j3 = Jugador("Charlie")

    c1, c2, c3, cdoble = crear_cartones_demo()

    j1.agregar_carton(c1)
    j2.agregar_carton(c2)
    j2.agregar_carton(cdoble)  
    j3.agregar_carton(c3)

    juego.registrar_jugador(j1)
    juego.registrar_jugador(j2)
    juego.registrar_jugador(j3)

    juego.iniciar()

    while not juego.ganador and juego.bombo.hay_numeros():
        ganador = juego.ejecutar_turno()
        if ganador:
            print(f"\n¡Ha ganado {ganador.nombre}!")

    juego.reporte_final()

if __name__ == "__main__":
    main()