# NUEVA (SRP): validacion extraida de Carton.
# ANTES: todo estaba mezclado en Carton.
# AHORA: solo valida palabra y numero maximo.
from .excepciones import ValidacionError


class ValidadorCarton:
    @staticmethod
    def validar_palabra(palabra):
        if not palabra or len(palabra) != 5:
            raise ValidacionError("La palabra debe tener exactamente 5 letras.")
        if len(set(palabra)) != 5:
            raise ValidacionError("La palabra no debe tener letras repetidas.")

    @staticmethod
    def validar_max_numero(max_num):
        if not isinstance(max_num, int) or max_num <= 0:
            raise ValidacionError("El maximo numero debe ser un entero positivo.")
        if not (50 <= max_num <= 90):
            raise ValidacionError("El maximo numero debe estar entre 50 y 90.")
        if max_num % 5 != 0:
            raise ValidacionError("El maximo numero debe ser multiplo de 5.")

    @staticmethod
    def validar(palabra, max_num):
        ValidadorCarton.validar_palabra(palabra)
        ValidadorCarton.validar_max_numero(max_num)
