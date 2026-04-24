import random


class Carton:
    """Representa un cartón de bingo reutilizable dentro del sistema del juego.

    Responsabilidad:
    - Validar los parámetros de generación del cartón.
    - Generar y almacenar una tarjeta 5x5.
    - Permitir marcar números anunciados durante la partida.
    - Verificar si el cartón completó bingo.

    Relación:
    - Es la clase base que será extendida por CartonDoble.
    """

    def __init__(self, palabra="BINGO", max_num=75):
        self.palabra = palabra.upper()
        self.tam = len(self.palabra)
        self.max_num = max_num
        self._validar_parametros()
        self.intervalo_columna = self.max_num // self.tam
        self.tarjeta = self.generar_tarjeta()
        self.marcados = set()

    def _validar_parametros(self):
        """Valida la palabra y el máximo número del juego."""
        if self.tam != 5:
            raise ValueError("La palabra debe tener exactamente 5 letras.")
        if len(set(self.palabra)) != self.tam:
            raise ValueError("La palabra no debe tener letras repetidas.")
        if not (50 <= self.max_num <= 90):
            raise ValueError("El máximo número debe estar entre 50 y 90.")
        if self.max_num % self.tam != 0:
            raise ValueError("El máximo número debe ser múltiplo de 5.")

    def _rango_columna(self, col):
        """Devuelve el rango [min, max] para una columna."""
        minimo = col * self.intervalo_columna + 1
        maximo = (col + 1) * self.intervalo_columna
        return minimo, maximo

    def generar_tarjeta(self):
        """Genera una tarjeta aleatoria 5x5 sin números repetidos."""
        tarjeta = [[0] * self.tam for _ in range(self.tam)]
        usados = set()

        for col in range(self.tam):
            minimo, maximo = self._rango_columna(col)
            numeros_columna = random.sample(
                [n for n in range(minimo, maximo + 1) if n not in usados],
                self.tam,
            )
            for fila in range(self.tam):
                valor = numeros_columna[fila]
                tarjeta[fila][col] = valor
                usados.add(valor)

        return tarjeta

    def marcar_numero(self, numero):
        """Marca un número en la tarjeta si existe en ella."""
        for fila in self.tarjeta:
            if numero in fila:
                self.marcados.add(numero)
                return True
        return False

    def tiene_bingo(self):
        """Verifica si todos los números de la tarjeta ya fueron marcados."""
        for fila in self.tarjeta:
            for numero in fila:
                if numero not in self.marcados:
                    return False
        return True

    def faltantes_para_bingo(self):
        """Cuenta cuántos números faltan por marcar para completar bingo."""
        faltantes = 0
        for fila in self.tarjeta:
            for numero in fila:
                if numero not in self.marcados:
                    faltantes += 1
        return faltantes

    def generar_varias_tarjetas(self, cantidad):
        """Genera varias tarjetas nuevas con los mismos parámetros."""
        return [self.generar_tarjeta() for _ in range(cantidad)]

    def imprimir_tarjeta(self, tarjeta=None):
        """Imprime una tarjeta con la cabecera de la palabra."""
        if tarjeta is None:
            tarjeta = self.tarjeta

        print("   ".join(self.palabra))
        print("-" * (self.tam * 4))
        for fila in tarjeta:
            celdas = []
            for numero in fila:
                if numero in self.marcados:
                    celdas.append(" X")
                else:
                    celdas.append("{:2d}".format(numero))
            print("  ".join(celdas))

    def __str__(self):
        lineas = ["   ".join(self.palabra), "-" * (self.tam * 4)]
        for fila in self.tarjeta:
            celdas = []
            for numero in fila:
                if numero in self.marcados:
                    celdas.append(" X")
                else:
                    celdas.append("{:2d}".format(numero))
            lineas.append("  ".join(celdas))
        return "\n".join(lineas)