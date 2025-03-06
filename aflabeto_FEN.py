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
        mov = input("\nDigite movimiento: \n")

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

        if not especial is None and (not especial[0] == '=' or len(especial) == 1):
            print("\nError. Promocion digitado incorrectamente\n")

        if especial is None:
            return (8 - int(inicio[1]), traduccion[inicio[0]]), (8 - int(fin[1]), traduccion[fin[0]]), 0
        else:
            return (8 - int(inicio[1]), traduccion[inicio[0]]), (8 - int(fin[1]), traduccion[fin[0]]), especial[1]



def separar_datos(mov : str) -> tuple:

    if len(mov) > 4:
        return mov[0:2],mov[2:4],mov[4:]
    else:
        return mov[0:2],mov[2:],None

