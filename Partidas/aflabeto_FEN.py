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

from typing import Any, Optional, Union
from Partidas.error_partidas import ErrorPartida

traduccion = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3,
                  'e' : 4, 'f' : 5, 'g' : 6, 'h' : 7}

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

    while True:
        try:
            #Pedimos al usuario que digite un movimiento
            mov : str = input("\nDigite movimiento (para detener partida digite parar y para rendirse digite fin): \n")

            #Si se digita un movimiento muy largo se considera invalido
            if len(mov) > 6:
                raise ErrorPartida("Movimiento demasiado largo","digitar movimiento")

        except ErrorPartida as e:
            print(e)
            continue

        #Si digita que quiere irse temporalmente de la partida o se rinde
        if mov.upper() == 'PARAR':
            return (),(),3
        if mov.upper() == 'FIN':
            return (),(),4

        #Si se digitan enroques solo se devuelve su clave (2 es largo y 1 corto)
        if mov == '0-0-0':
            return (),(),2
        if mov == '0-0':
            return (),(),1

        try:
            #Obtenemos desglosado el movimiento
            inicio, fin, especial = separar_datos(mov)

            #Si no se ha digitado bien la posición de origen
            if not(inicio[0]  in 'abcdefgh' and inicio[1] in '12345678'):
                raise ErrorPartida("Posicion inicial digitado incorrectamente","digitar movimiento")

            #Si no se ha digitado bien la posición destino
            if not (fin[0] in 'abcdefgh' and fin[1] in '12345678'):
                raise ErrorPartida("Posicion final digitado incorrectamente", "digitar movimiento")

            #Si destino y origen son iguales
            if inicio == fin:
                raise ErrorPartida("Posicion inicial y final son identicas", "digitar movimiento")

            #Si no se digita correctamente la promoción
            if especial is not None and (not especial[0] == '=' or len(especial) == 1):
                raise ErrorPartida("Promocion digitado incorrectamente", "digitar movimiento")

            #Si deseas promocionar a una pieza que no se puede
            if especial is not None and especial[1] not in 'QRBNqrbn':
                raise ErrorPartida("Intento de promoción fallida por querer trasformar a una pieza no permitida", "digitar movimiento")

        except ErrorPartida as e:
            print(e)
            continue
        except IndexError:
            e = ErrorPartida("No se ha digitado movimiento","digitar movimiento")
            print(e)
            continue

        else:
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

def traducir_movimiento_ia(mov : str) -> tuple[tuple, tuple, int] | tuple[tuple[int, Any], tuple[int, Any], int | Any]:
    if mov == '0-0-0':
        return (), (), 2
    if mov == '0-0':
        return (), (), 1

    inicio, fin, especial = separar_datos(mov)

    return ((8 - int(inicio[1]), traduccion[inicio[0]]), (8 - int(fin[1]), traduccion[fin[0]]),
            0 if especial is None else especial[1].upper())


def transformacion_a_LAN_hipersimplificado(mov : str) -> list[str] | str | Any:
    """
    Función que permite transformar cualquier movimiento digitado en formato SAN al formato LAN hipersimplificado, pero
    ignora la posición de origen y la pieza que se mueve.

    Parámetros:
    ----------
    mov : str -> Movimiento digitado por la máquina (que es quien digita en este formato)

    Retorna:
    ---------
    str
        Retorna el movimiento en formato LAN hipersimplificado
    """

    mov_sep : list[str] = list(mov)

    if mov == '0-0-0' or mov == '0-0':
        return mov

    if mov in ['e1g1','e1h1','e8g8','e8h8']:
        return ['0-0',mov]

    if mov in ['e1c1','e1a1','e8c8','e8a8']:
        return ['0-0-0',mov]

    if '+' in mov_sep:
        mov_sep.remove('+')

    if '#' in mov_sep:
        mov_sep.remove('#')

    if 'x' in mov_sep:
        mov_sep.remove('x')

    while True:
        if not mov_sep[0] in 'abcdefgh' or not mov_sep[1] in '12345678':
            mov_sep.remove(mov_sep[0])
            continue

        break

    if mov_sep[-1].upper() in 'RNBQ':
        mov_sep.insert(-1,'=')

    mov : str = ''
    for letra in mov_sep:
        mov += letra

    return mov

def traduccion_posicion(posicion : str) -> tuple[int,int]:
    """
    Transforma una posición escrita en formato LAN a coordenadas del tablero

    Parámetros:
    ----------
    pos : str

        Posición del tablero

    Retorna:
    ---------
    tuple[int,int]
        Devuelve la posición en coordenadas
    """

    return traduccion[posicion[0]],int(posicion[1])

def traduccion_inversa(posicion : Union[tuple[int,int], int], donde : Optional[str] = None) -> str:
    columnas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    if type(posicion) == int:
        if donde == "fila":
            return str(posicion - 1)

        return columnas[posicion]

    return columnas[posicion[1]] + str(8 - posicion[0])

def traduccion_total_inversa(movimiento : tuple[tuple, tuple, int] | tuple[tuple[int, Any], tuple[int, Any], int | Any]) -> str:
    if str(movimiento[2]) in '12':
        return '0-0-0' if movimiento[2] == 2 else '0-0'

    inicio : str = traduccion_inversa(movimiento[0])
    fin : str = traduccion_inversa(movimiento[1])
    promocion : str = ''

    if movimiento[2] != 0:
        promocion = f'={movimiento[2]}'

    return inicio + fin + promocion

if __name__ == '__main__':
    #print(traducir_movimiento_ia(transformacion_a_LAN_hipersimplificado(input("Movimiento: "))))
    #print(digitar_movimiento(1))
    print(traduccion_total_inversa(traducir_movimiento_ia(transformacion_a_LAN_hipersimplificado(input("Movimiento: ")))))
    print(traduccion_total_inversa(digitar_movimiento(1)))
