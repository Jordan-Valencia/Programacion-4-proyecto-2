from bingo.carton import Carton
from bingo.carton_doble import CartonDoble
from bingo.jugador import Jugador
from bingo.juego import Juego
from bingo.validacion import ValidadorCarton
from bingo.generador import GeneradorCarton
from bingo.excepciones import BingoError, ValidacionError, JuegoError


def pedir_palabra() -> str:
    while True:
        try:
            palabra = input(
                "  Ingrese la palabra de 5 letras para el carton "
                "(sin letras repetidas): "
            ).strip().upper()
            ValidadorCarton.validar_palabra(palabra)
            return palabra
        except ValidacionError as e:
            print(f"  Error: {e}")


def pedir_max_numero() -> int:
    while True:
        try:
            entrada = input(
                "  Cuantos numeros tendra el bombo? "
                "(entre 50 y 90, multiplo de 5): "
            ).strip()
            if not entrada.isdigit():
                print("  Error: ingrese un numero entero.")
                continue
            valor = int(entrada)
            ValidadorCarton.validar_max_numero(valor)
            return valor
        except ValidacionError as e:
            print(f"  Error: {e}")


def mostrar_cartones(jugador: Jugador) -> None:
    print(f"\n  Cartones de {jugador.nombre}:")
    for i, carton in enumerate(jugador.get_cartones(), 1):
        print(f"  [Carton {i}]")
        for linea in str(carton).splitlines():
            print(f"  {linea}")


def crear_carton(palabra: str, max_num: int, tipo: str):
    tam = len(palabra)
    if tipo == "d":
        t1 = GeneradorCarton.generar(tam, max_num)
        t2 = GeneradorCarton.generar(tam, max_num)
        return CartonDoble(palabra, t1, t2)
    return Carton(palabra, GeneradorCarton.generar(tam, max_num))


def registrar_nuevo_jugador(
    juego: Juego, palabra: str, max_num: int
) -> None:
    try:
        nombre = input("  Nombre del jugador: ").strip()
        if not nombre:
            print("  Nombre vacio, operacion cancelada.")
            return

        jugador = Jugador(nombre)
        tipo = input(
            f"  Carton simple (s) o doble (d) para {nombre}? "
        ).strip().lower()
        if tipo not in ("s", "d"):
            print("  Opcion invalida. Use 's' para simple o 'd' para doble.")
            return

        carton = crear_carton(palabra, max_num, tipo)
        jugador.agregar_carton(carton)
        juego.registrar_jugador(jugador)

        tipo_str = "doble" if tipo == "d" else "simple"
        print(f"  {nombre} registrado con carton {tipo_str}.")
        mostrar_cartones(jugador)

    except (ValueError, ValidacionError, JuegoError) as e:
        print(f"  Error: {e}")


def dar_de_baja(juego: Juego) -> None:
    try:
        jugadores = juego.get_jugadores()
        if not jugadores:
            print("  No hay jugadores registrados.")
            return

        print("  Jugadores actuales:")
        for i, j in enumerate(jugadores, 1):
            print(f"    {i}. {j.nombre}")

        seleccion = input(
            "  Numero del jugador a dar de baja (Enter para cancelar): "
        ).strip()
        if not seleccion.isdigit():
            return

        idx = int(seleccion) - 1
        if 0 <= idx < len(jugadores):
            juego.dar_de_baja_jugador(jugadores[idx])
            print(f"  {jugadores[idx].nombre} dado de baja.")
        else:
            print("  Numero invalido.")
    except (ValueError, JuegoError) as e:
        print(f"  Error: {e}")


def jugadores_marcaron_numero(juego: Juego, numero: int) -> list:
    marcaron = []
    for jugador in juego.get_jugadores():
        for carton in jugador.get_cartones():
            if carton.tiene_marcado(numero):
                marcaron.append(jugador.nombre)
                break
    return marcaron


def mostrar_reporte_final(juego: Juego) -> None:
    print("\n" + "=" * 40)
    print("          REPORTE FINAL")
    print("=" * 40)
    ganador = juego.get_ganador()
    if ganador:
        print(f"Ganador: {ganador.nombre}")
    else:
        print("No hubo ganador.")
    print(
        f"\nNumeros extraidos "
        f"({len(juego.get_historial_numeros())} en total):"
    )
    print(juego.get_historial_numeros())
    print("\nNumeros marcados por jugador:")
    for jugador in juego.get_jugadores():
        print(f"  - {jugador.nombre}: {jugador.numeros_marcados}")


def fase_registro(juego: Juego, palabra: str, max_num: int) -> None:
    print("\n=== REGISTRO DE JUGADORES ===")
    print("Se necesitan al menos 3 jugadores para comenzar.\n")

    while True:
        registrar_nuevo_jugador(juego, palabra, max_num)
        jugadores_actuales = len(juego.get_jugadores())
        if jugadores_actuales < 3:
            print(
                f"\n  Jugadores registrados: "
                f"{jugadores_actuales}/3 minimo. Registra mas."
            )
        else:
            try:
                otra = input(
                    "\nRegistrar otro jugador? (s/n): "
                ).strip().lower()
                if otra != "s":
                    break
            except (EOFError, KeyboardInterrupt):
                print("\n  Operacion cancelada.")
                break


def main() -> None:
    try:
        print("=" * 40)
        print("        BINGO INTERACTIVO")
        print("=" * 40)

        print("\n=== CONFIGURACION DE LA PARTIDA ===")
        palabra = pedir_palabra()
        max_num = pedir_max_numero()
        print(f"\n  Palabra: {palabra} | Numeros en el bombo: {max_num}")

        juego = Juego(max_numero=max_num)

        fase_registro(juego, palabra, max_num)

        try:
            juego.iniciar()
        except JuegoError as e:
            print(f"  Error: {e}")
            return

        print("\n=== PARTIDA INICIADA ===")
        print(
            "Jugadores: "
            + ", ".join(j.nombre for j in juego.get_jugadores())
        )
        print("\nOpciones durante la partida:")
        print("  [Enter]  Extraer siguiente numero")
        print("  a        Agregar un jugador")
        print("  b        Dar de baja un jugador")
        print("  q        Terminar la partida")

        while juego.esta_en_curso() and juego.hay_numeros_disponibles():
            print("\n" + "-" * 40)
            try:
                opcion = input("Accion > ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\n  Partida terminada.")
                break

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
                print(
                    "Opcion no reconocida. "
                    "Presiona Enter para extraer numero."
                )
                continue

            try:
                numero = juego.ejecutar_turno()
                if numero is None:
                    print("  No hay mas numeros en el bombo.")
                    break
            except JuegoError as e:
                print(f"  Error: {e}")
                break

            print(f"\n  >>> Numero extraido: {numero} <<<")

            marcaron = jugadores_marcaron_numero(juego, numero)
            if marcaron:
                print(
                    f"  Marcaron el {numero}: {', '.join(marcaron)}"
                )
            else:
                print(
                    f"  Nadie tenia el {numero} en su carton."
                )

            for jugador in juego.get_jugadores():
                mostrar_cartones(jugador)

            ganador = juego.get_ganador()
            if ganador:
                print(f"\n*** {ganador.nombre} ha ganado el BINGO! ***")

        mostrar_reporte_final(juego)

    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
    except BingoError as e:
        print(f"\nError en el juego: {e}")
    except Exception as e:
        print(f"\nError inesperado: {e}")


if __name__ == "__main__":
    main()
