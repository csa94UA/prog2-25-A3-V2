"""
Modulo para la traducción de una entrada en formato LAN simplificado al movimiento deseado

Este modulo proporciona funciones para la traducción del formato LAN simplificado a movimiento,
simplificación de otros formatos LAN y manejo de errores.

Funciones:
    - digitar_movimiento() -> tuple:
    Piede al usuario digitar su movimiento en formato LAN simplificado y devuelve el movimiento correspondiente.

    - separar_datos(mov : str) -> tuple:
    Separa la entrada de datos en sus partes correspondientes
    - traducción_LAN(mov : str) -> str:
    Simplifica el formato LAN de entrada a nuestro formato ultrasimplificado.
"""

from typing import Any

def digitar_movimiento(color : int) -> None | tuple[tuple, tuple, int] | tuple[
    tuple[int, Any], tuple[int, Any], int | Any]:
    """
    Función encargada de leer por consola el movimiento digitado por el jugador en formato LAN hipersimplificado.

    Parametros:
    -----------
    color : bool -> Representa el color del jugador que digita el movimiento. Es importante para tener en cuenta su
    persepctiva del tablero con la perspectiva que tiene el tablero dentro del código.

    Retorna:
    -----------
    Any:
        En realidad retorna una especie de tupla con la posicion inicial y final del movimiento respecto de la
        perspectiva del tablero real (no la visual), además de devolver un entero que representa si es un movimiento
        normal, enroque largo o enroque corto. Para la promoción devuelve directamente el carácter siempre en mayusculas.

        Su estructura seria algo como -> None | tuple[tuple, tuple, int] | tuple[tuple[int, Any], tuple[int, Any], int | Any]
        Ahora entenderas porque no se pone (es demasiado largo).
    """

    traduccion = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3,
                  'e' : 4, 'f' : 5, 'g' : 6, 'h' : 7}

    while True:
        mov : str = input("\nDigite movimiento: \n")

        if len(mov) > 6:
            print("\nError. Movimiento demasiado largo\n")
            continue

        if mov == '0-0-0':
            return (),(),2
        if mov == '0-0':
            return (),(),1

        inicio, fin, especial = separar_datos(mov)

        if not(inicio[0]  in 'abcdefgh' and inicio[1] in '12345678'):
            print("\nError. Posicion inicial digitado incorrectamente\n")
            continue

        if not (fin[0] in 'abcdefgh' and fin[1] in '12345678'):
            print("\nError. Posicion final digitado incorrectamente\n")
            continue

        if inicio == fin:
            print("\nError. Posicion inicial y final son identicas\n")
            continue

        if especial is not None and (not especial[0] == '=' or len(especial) == 1):
            print("\nError. Promocion digitado incorrectamente\n")
            continue

        if especial is not None and especial[1] not in 'QRBNqrbn':
            print("\nError. Intento de promoción fallida por querer trasformar a una pieza no permitida\n")
            continue

        if color:
            return ((8 - int(inicio[1]), traduccion[inicio[0]]), (8 - int(fin[1]), traduccion[fin[0]]),
                    0 if especial is None else especial[1].upper())
        else:
            return ((int(inicio[1]) - 1, 7 - traduccion[inicio[0]]), (int(fin[1]) - 1, 7 - traduccion[fin[0]]),
                    0 if especial is None else especial[1].upper())



def separar_datos(mov : str) -> tuple:
    """
    Función que sirve para subdividir la cadena de texto otorgada por el jugador en {origen}{destino}{promocion}.

    Porametros:
    -----------
    mov : str -> Es el movimiento digitado por el jugador

    Retorna:
    --------
    tuple
        Retorna el movimiento del jugador segmentado en sus partes correspondientes: {origen}{destino}{promocion}
    """

    if len(mov) > 4:
        return mov[0:2],mov[2:4],mov[4:]
    else:
        return mov[0:2],mov[2:],None


def traducción_LAN(mov : str) -> str:
    """
    Función que permite transformar cualquier movimiento digitado en formato LAN al formato LAN hipersimplificado

    Parámetros:
    ----------
    mov : str -> Movimiento digitado por la máquina (que es quien digita en este formato)

    Retorna:
    ---------
    str
        Retorna el movimiento en formato LAN hipersimplificado
    """

    mov_sep : list[str] = list(mov)

    if mov == '0-0-0':
        return mov
    if mov == '0-0':
        return mov

    if '-' in mov_sep:
        mov_sep.remove('-')

    if '+' in mov_sep:
        mov_sep.remove('+')

    if '#' in mov_sep:
        mov_sep.remove('#')

    if 'x' in mov_sep:
        mov_sep.remove('x')

    if not mov_sep[0] in 'abcdefgh' or not mov_sep[1] in '12345678':
        mov_sep.remove(mov_sep[0])

    mov : str = ''
    for letra in mov_sep:
        mov += letra

    return mov

if __name__ == '__main__':
    print(digitar_movimiento(0))