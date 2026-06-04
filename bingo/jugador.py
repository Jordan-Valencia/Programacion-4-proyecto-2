class Jugador:
    def __init__(self, nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del jugador no puede estar vacio.")
        self.nombre = nombre.strip()
        self._cartones = []
        self.numeros_marcados = 0

    def get_cartones(self):
        return list(self._cartones)

    def agregar_carton(self, carton):
        if carton in self._cartones:
            raise ValueError("El jugador ya tiene ese carton.")
        self._cartones.append(carton)

    def retirar_carton(self, carton):
        if carton not in self._cartones:
            raise ValueError("El carton no pertenece al jugador.")
        self._cartones.remove(carton)

    def notificar_numero(self, numero):
        hay_bingo = False
        for carton in self._cartones:
            if carton.marcar_numero(numero):
                self.numeros_marcados += 1
            if carton.tiene_bingo():
                hay_bingo = True
        return hay_bingo
