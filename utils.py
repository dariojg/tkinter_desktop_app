import re


def es_palabra(value):
    """
    Esta función verifica si la cadena 'value' contiene solo letras mayúsculas o minúsculas del alfabeto español,
    incluyendo las letras acentuadas (ÁÉÍÓÚáéíóú).

    Args:
        value (str): La cadena que se va a verificar.

    Returns:
        bool: True si 'value' es una palabra válida, False en caso contrario.
    """
    pattern = re.compile(r'^[a-zA-ZÁÉÍÓÚóúáéíóú]+$')
    return pattern.match(value)


def es_numero(value):
    """
    Esta función verifica si 'value' es un número, ya sea un número entero o un número decimal.

    Args:
        value (str o int o float): El valor que se va a verificar.

    Returns:
        bool: True si 'value' es un número válido, False en caso contrario.
    """
    pattern = re.compile(r'^-?\d+(\.\d+)?$')
    return pattern.match(str(value))
