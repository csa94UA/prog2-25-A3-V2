"""
Modulo para la traducción de una entrada en formato LAN simplificado al movimiento deseado

Este modulo proporciona funciones para la traducción del formato LAN simplificado a movimiento,
simplificación de otros formatos LAN y manejo de errores.

Funciones:
    - digitar_movimiento() -> tuple: Piede al usuario digitar su movimiento en formato LAN simplificado y devuelve
    el movimiento correspondiente
    - separar_datos(mov : str) -> Separa la entrada de datos en sus partes correspondientes
    - simplificacion(mov : str) -> Simplifica el formato LAN de entrada
"""

def digitar_movimiento() -> tuple:

    traduccion = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4,
                  'e' : 5, 'f' : 6, 'g' : 7, 'h' : 8}

    while True:
        mov : str = input("\nDigite movimiento: \n")

        if len(mov) > 6:
            print("\nError. Movimiento demasiado largo\n")
            continue

        if mov == '0-0-0':
            return [],2
        if mov == '0-0':
            return [],1

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

        if not especial is None and (not especial[0] == '=' or len(especial) == 1):
            print("\nError. Promocion digitado incorrectamente\n")
            continue

        if especial[1] not in 'QRBNqrbn':
            print("\nError. Intento de promoción fallida por querer trasformar a una pieza no permitida\n")
            continue

        if especial is None:
            return (8 - int(inicio[1]), traduccion[inicio[0]]), (8 - int(fin[1]), traduccion[fin[0]]), 0
        else:
            return (8 - int(inicio[1]), traduccion[inicio[0]]), (8 - int(fin[1]), traduccion[fin[0]]), especial[1].upper()



def separar_datos(mov : str) -> tuple:

    if len(mov) > 4:
        return mov[0:2],mov[2:4],mov[4:]
    else:
        return mov[0:2],mov[2:],None


def traducción_LAN(mov : str) -> str:
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
    movimientos = [
        "e2-e4",  # Movimiento normal de peón (de e2 a e4)
        "d2-d4",  # Movimiento normal de peón (de d2 a d4)
        "e5xd6",  # Captura de peón (de e5 captura en d6)
        "Ng1-f3",  # Movimiento normal de Caballo (de g1 a f3)
        "Nb1xc3",  # Captura del Caballo (de b1 captura en c3)
        "Bf1-c4",  # Movimiento normal de Alfil (de f1 a c4)
        "Ra1-a3",  # Movimiento normal de Torre (de a1 a a3)
        "Qd1-d3",  # Movimiento normal de Reina (de d1 a d3)
        "Ke1-e2",  # Movimiento normal de Rey (de e1 a e2)
        "e7-e8=Q",  # Promoción de peón (de e7 a e8, coronándose a Dama)
        "g7-g8=N+",  # Promoción de peón con jaque (de g7 a g8, coronándose a Caballo y dando jaque)
        "0-0",  # Enroque corto (rey y torre se mueven)
        "0-0-0"  # Enroque largo (rey y torre se mueven)
    ]

    # Ejemplo de impresión:
    for mov in movimientos:
        print(traducción_LAN(mov))

    print(digitar_movimiento())