# main.py
from bingo.carton import Carton
from bingo.carton_doble import CartonDoble
from bingo.jugador import Jugador
from bingo.juego import Juego


def mostrar_cartones(jugador: Jugador) -> None:
    print(f"\n  Cartones de {jugador.nombre}:")
    for i, carton in enumerate(jugador.get_cartones(), 1):
        print(f"  [Carton {i}]")
        for linea in str(carton).splitlines():
            print(f"  {linea}")


def registrar_nuevo_jugador(juego: Juego) -> None:
    nombre = input("  Nombre del jugador: ").strip()
    if not nombre:
        print("  Nombre vacío, operación cancelada.")
        return

    jugador = Jugador(nombre)

    tipo = input(f"  ¿Cartón simple (s) o doble (d) para {nombre}? ").strip().lower()
    carton = CartonDoble("BINGO", 75) if tipo == "d" else Carton("BINGO", 75)
    jugador.agregar_carton(carton)

    try:
        juego.registrar_jugador(jugador)
        tipo_str = "doble" if tipo == "d" else "simple"
        print(f"  {nombre} registrado con cartón {tipo_str}.")
        mostrar_cartones(jugador)
    except ValueError as e:
        print(f"  Error: {e}")


def dar_de_baja(juego: Juego) -> None:
    jugadores = juego.get_jugadores()
    if not jugadores:
        print("  No hay jugadores registrados.")
        return

    print("  Jugadores actuales:")
    for i, j in enumerate(jugadores, 1):
        print(f"    {i}. {j.nombre}")

    seleccion = input("  Número del jugador a dar de baja (Enter para cancelar): ").strip()
    if not seleccion.isdigit():
        return

    idx = int(seleccion) - 1
    if 0 <= idx < len(jugadores):
        baja = jugadores[idx]
        juego.dar_de_baja_jugador(baja)
        print(f"  {baja.nombre} dado de baja.")
    else:
        print("  Número inválido.")


def fase_registro(juego: Juego) -> None:
    print("\n=== REGISTRO DE JUGADORES ===")
    print("Registra al menos un jugador para comenzar.\n")

    while True:
        registrar_nuevo_jugador(juego)
        if juego.get_jugadores():
            otra = input("\n¿Registrar otro jugador? (s/n): ").strip().lower()
            if otra != "s":
                break


def main() -> None:
    print("=" * 40)
    print("        BINGO INTERACTIVO")
    print("=" * 40)

    juego = Juego(max_numero=75)

    fase_registro(juego)
    juego.iniciar()

    print("\n=== PARTIDA INICIADA ===")
    print("Jugadores: " + ", ".join(j.nombre for j in juego.get_jugadores()))
    print("\nOpciones durante la partida:")
    print("  [Enter]  Extraer siguiente número")
    print("  a        Agregar un jugador")
    print("  b        Dar de baja un jugador")
    print("  q        Terminar la partida")

    while juego.ganador is None and juego.bombo.hay_numeros():
        print("\n" + "-" * 40)
        opcion = input("Acción > ").strip().lower()

        if opcion == "q":
            print("Partida terminada manualmente.")
            break
        elif opcion == "a":
            registrar_nuevo_jugador(juego)
            continue
        elif opcion == "b":
            dar_de_baja(juego)
            continue
        elif opcion != "":
            print("Opción no reconocida. Presiona Enter para extraer número.")
            continue

        juego.ejecutar_turno()
        numero_actual = juego.bombo.historial[-1]
        print(f"\n  >>> Número extraído: {numero_actual} <<<")

        for jugador in juego.get_jugadores():
            mostrar_cartones(jugador)

        if juego.ganador:
            print(f"\n*** ¡{juego.ganador.nombre} ha ganado el BINGO! ***")

    juego.reporte_final()


if __name__ == "__main__":
    main()
