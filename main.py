from bingo.carton import Carton
from bingo.carton_doble import CartonDoble
from bingo.jugador import Jugador
from bingo.juego import Juego


def pedir_palabra():
    while True:
        palabra = input("  Ingrese la palabra de 5 letras para el cartón (sin letras repetidas): ").strip().upper()
        if len(palabra) != 5:
            print("  Error: la palabra debe tener exactamente 5 letras.")
        elif len(set(palabra)) != 5:
            print("  Error: la palabra no debe tener letras repetidas.")
        else:
            return palabra


def pedir_max_numero():
    while True:
        entrada = input("  ¿Cuántos números tendrá el bombo? (entre 50 y 90, múltiplo de 5): ").strip()
        if not entrada.isdigit():
            print("  Error: ingrese un número entero.")
            continue
        valor = int(entrada)
        if not (50 <= valor <= 90):
            print("  Error: el número debe estar entre 50 y 90.")
        elif valor % 5 != 0:
            print("  Error: el número debe ser múltiplo de 5.")
        else:
            return valor


def mostrar_cartones(jugador):
    print(f"\n  Cartones de {jugador.nombre}:")
    for i, carton in enumerate(jugador.get_cartones(), 1):
        print(f"  [Carton {i}]")
        for linea in str(carton).splitlines():
            print(f"  {linea}")


def registrar_nuevo_jugador(juego, palabra, max_num):
    nombre = input("  Nombre del jugador: ").strip()
    if not nombre:
        print("  Nombre vacío, operación cancelada.")
        return

    jugador = Jugador(nombre)

    tipo = input(f"  ¿Cartón simple (s) o doble (d) para {nombre}? ").strip().lower()
    carton = CartonDoble(palabra, max_num) if tipo == "d" else Carton(palabra, max_num)
    jugador.agregar_carton(carton)

    try:
        juego.registrar_jugador(jugador)
        tipo_str = "doble" if tipo == "d" else "simple"
        print(f"  {nombre} registrado con cartón {tipo_str}.")
        mostrar_cartones(jugador)
    except ValueError as e:
        print(f"  Error: {e}")


def dar_de_baja(juego):
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


def fase_registro(juego, palabra, max_num):
    print("\n=== REGISTRO DE JUGADORES ===")
    print("Se necesitan al menos 3 jugadores para comenzar.\n")

    while True:
        registrar_nuevo_jugador(juego, palabra, max_num)
        jugadores_actuales = len(juego.get_jugadores())
        if jugadores_actuales < 3:
            print(f"\n  Jugadores registrados: {jugadores_actuales}/3 mínimo. Registra más.")
        else:
            otra = input("\n¿Registrar otro jugador? (s/n): ").strip().lower()
            if otra != "s":
                break


def main():
    print("=" * 40)
    print("        BINGO INTERACTIVO")
    print("=" * 40)

    print("\n=== CONFIGURACIÓN DE LA PARTIDA ===")
    palabra = pedir_palabra()
    max_num = pedir_max_numero()
    print(f"\n  Palabra: {palabra} | Números en el bombo: {max_num}")

    juego = Juego(max_numero=max_num)

    fase_registro(juego, palabra, max_num)
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
            registrar_nuevo_jugador(juego, palabra, max_num)
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

        marcaron = [
            jugador.nombre
            for jugador in juego.get_jugadores()
            if any(numero_actual in carton.marcados for carton in jugador.get_cartones())
        ]
        if marcaron:
            print(f"  Marcaron el {numero_actual}: {', '.join(marcaron)}")
        else:
            print(f"  Nadie tenía el {numero_actual} en su cartón.")

        for jugador in juego.get_jugadores():
            mostrar_cartones(jugador)

        if juego.ganador:
            print(f"\n*** ¡{juego.ganador.nombre} ha ganado el BINGO! ***")

    juego.reporte_final()


if __name__ == "__main__":
    main()