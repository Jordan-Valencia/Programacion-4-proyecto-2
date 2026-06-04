import random


class GeneradorCarton:
    @staticmethod
    def _rango_columna(col, intervalo):
        minimo = col * intervalo + 1
        maximo = (col + 1) * intervalo
        return minimo, maximo

    @staticmethod
    def generar(tam, max_num):
        intervalo = max_num // tam
        tarjeta = [[0] * tam for _ in range(tam)]
        usados = set()

        for col in range(tam):
            minimo, maximo = GeneradorCarton._rango_columna(col, intervalo)
            disponibles = [n for n in range(minimo, maximo + 1) if n not in usados]
            if len(disponibles) < tam:
                raise ValueError("No hay suficientes numeros para generar el carton.")
            numeros_columna = random.sample(disponibles, tam)
            for fila in range(tam):
                valor = numeros_columna[fila]
                tarjeta[fila][col] = valor
                usados.add(valor)

        return tarjeta
