# NUEVA: jerarquia de excepciones para el proyecto.
# BingoError (base) -> ValidacionError, JuegoError.
class BingoError(Exception):
    pass


class ValidacionError(BingoError):
    pass


class JuegoError(BingoError):
    pass
