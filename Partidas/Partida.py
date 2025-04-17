"""
Modulo para la ejecucion de una partida, ya sea JcJ, JcE o EcE.

Este modulo proporciona funciones para el intercambio de turnos, manejo de excepciones e
inicialización de la partida.

Funciones:
    - partida(jugador1 : Jugador, jugador2 : Jugador) -> Jugador:
    Simula la partida y determina el ganador. Es la funcion nucleo de todo el programa.

    - crear_piezas(color : bool, tablero : Tablero) -> list[Pieza]:
    Inicializa el tablero y las fichas de cada jugador.

    - encontrar_pieza(tablero : "Tablero", jugador : "Jugador", origen : tuple[int]) -> Union["Pieza",None]:
    Busca la pieza digitada dentro de del conjunto de piezas del jugador. Si lo encuentra devuelve dicha pieza.

    - comprobar_enroque_corto(tablero : "Tablero", enemigo : "Jugador", rey : "Rey", torre : "Torre") -> bool:
    En caso de digitar un enroque corto comprueba si es posible.

    - comprobar_enroque_largo(tablero : "Tablero", enemigo : "Jugador", rey : "Rey", torre : "Torre") -> bool:
    Igual que con el enroque corto solo que para el caso de enroque largo.

    - comprobar_promocion(pieza : "Peon", promocion : Union[str,int], jugador_actual : "Jugador") -> bool:
    Comprueba si la promocion es valido. En caso afirmativo se intercambia el peon por la pieza deseada (dentro de
    las permitidas).

    - comprobar_jaque_enemigo(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador", pieza : Union["Pieza",None]) -> bool:
    Comprueba si el movimiento que hemos realizado provoca un jaque al rey enemigo.

    - caso_jaque(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador", movimiento : tuple) -> bool:
    Determina si tu movimiento evita el jaque. Solo se activa cuando se ejecuta el caso especial de jaque.

    - comprobar_tablas(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador") -> bool:
    Comprueba si se ha producido un empate (por el momento solo devuelve True si solo hay en el tablero los reyes).
"""

from Piezas import Caballo, Alfil, Rey, Reina, Peon, Torre, Pieza
from Jugador import Jugador
from random import randint
from typing import Union
from Partidas.aflabeto_FEN import digitar_movimiento
from Tablero import Tablero


def partida(jugador1 : Jugador, jugador2 : Jugador) -> Union["Jugador",None]:
    """
    Es la función principal de este archivo. En ella se trata toda la logica general de una partida de ajedrez (trato de
    turnos, manejo de movimientos especiales, manejo de errores, etc.).

    Parametros:
    -----------
    jugador_1 : Jugador -> Representa el primer jugador

    jugador_2 : Jugador -> Representa el segundo jugador

    Retorna:
    ----------
    Jugador
        Devuelve el jugador que ha ganado. Si hay empate devuelve None.
    """

    #Establecemos un inicio de turno aleatorio
    if randint(0,1000) < 499:
        jugador1.color = 1
        jugador2.color = 0
    else:
        jugador2.color = 1
        jugador1.color = 0

    tablero = Tablero() #Cargamos tablero

    #Insertamos las piezas en el tablero y en el inventario del jugador
    jugador1.piezas = crear_piezas(jugador1.color, tablero, jugador2)
    jugador2.piezas = crear_piezas(jugador2.color, tablero, jugador1)

    game_over : bool = False
    jaque : bool = False
    turno = 1 if jugador1.color else 0
    jugador_actual : Union["Jugador",None] = None
    while not game_over:
        jugador_actual = jugador1 if turno else jugador2
        enemigo : Jugador = jugador1 if not turno else jugador2

        tablero.mostrar_tablero(jugador_actual.color)

        if comprobar_tablas(tablero, jugador_actual, enemigo):
            jugador_actual = None #Nadie gana
            print("Nadie gana")
            break

        print(f"\nTurno de {jugador_actual.nombre}")

        movimiento = digitar_movimiento(jugador_actual.color)

        if jaque:
            intento : bool = caso_jaque(tablero, jugador_actual, enemigo, movimiento)

            if not intento:
                continue

            else:
                jaque = True if comprobar_jaque_enemigo(tablero, jugador_actual, enemigo, None) else False
                turno = 1 - turno

        rey = next((rey for rey in jugador_actual.piezas if isinstance(rey, Rey)), None)

        #Comprobamos si quieren hacer enroque. Si es así se simula y se comprueba su validez
        if type(movimiento[2]) == int and movimiento[2] in [1,2]:

            if movimiento[2] == 1:
                torre = next((torre for torre in jugador_actual.piezas if isinstance(torre, Torre) \
                          and torre.posicion[1] == 7), None)
            else:
                torre = next((torre for torre in jugador_actual.piezas if isinstance(torre, Torre) \
                              and torre.posicion[1] == 0), None)

            if torre is None:
                print("No se ha encontrado una torre para hacer enroque")
                continue

            pos_rey = rey.posicion
            pos_torre = torre.posicion

            intento : bool = comprobar_enroque_corto(tablero, enemigo, rey, torre) if movimiento[2] == 1 else \
                comprobar_enroque_largo(tablero, enemigo, rey, torre)

            if not intento:
                rey.posicion = pos_rey
                torre.posicion = pos_torre
                print("No ha sido posible hacer el enroque")
                continue

            jaque: bool = comprobar_jaque_enemigo(tablero, jugador_actual, enemigo, torre)

            pos_rey_enemigo = enemigo.encontrar_rey()

            if jaque and tablero.jaque_in(pos_rey_enemigo[0], pos_rey_enemigo[1], enemigo, jugador_actual):
                break

            turno = 1 - turno
            continue

        # Busca la pieza en esa posicion. Si no la encuentra, dará un mensaje de error y repetirá el movimiento

        pieza: Union["Pieza", None] = encontrar_pieza(tablero, jugador_actual, movimiento[0])

        if pieza is None:
            print("Error. No se ha encontrado ninguna pieza.")
            continue

        if str(movimiento[2]).isalpha() and not isinstance(pieza, Peon):
            print("Error. Se ha intentado promocionar con una pieza que no es peon")
            continue

        # pos_antigua = pieza.posicion

        if not pieza.mover(movimiento[1], tablero, jugador_actual, enemigo, str(movimiento[2])):
            print("El movimiento es inválido (autojaque, movimiento impromio de la pieza, etc)")
            continue

        if isinstance(pieza, Torre) or isinstance(pieza, Rey) or isinstance(pieza, Peon):
            pieza.movido = True

        #En caso de que sea un peon y se haya digitado una promoción, debemos comprobar si es válida. En caso afirmativo
        #transformamos ese peon a la pieza deseada

        if str(movimiento[2]).isalpha():

            intento : bool = comprobar_promocion(pieza, movimiento[2], jugador_actual, tablero)

            if not intento:
                print("Error. No se ha podido realizar la promoción")
                continue

        #Vemos si produce la pieza un jaque. En caso afirmativo lo guardamos para el jugador del siguiente turno
        rey = next((rey for rey in enemigo.piezas if isinstance(rey, Rey)), None)
        jaque : bool = comprobar_jaque_enemigo(tablero, jugador_actual, enemigo, pieza)

        if jaque and tablero.jaque_in(rey.posicion[0], rey.posicion[1], enemigo, jugador_actual):
            break

        turno = 1 - turno

    print("Ha ganado el jugador", jugador_actual.nombre)
    print("Felicidades!!!!!")

    return jugador_actual



def crear_piezas(color : int, tablero : Tablero, enemigo : "Jugador") -> list["Pieza"]:
    """
    Función que inicializa las piezas de un jugador al comenzar una partida. Tiene en cuanta el color del jugador para
    colocar las piezas en su lugar.

    Parametros:
    -----------
    color : int -> Color del jugador a quien se le van a crear las piezas.

    tablero : Tablero -> Tablero en sí para guardar la posición de las piezas creadas.

    Retorna:
    ----------
    list[Pieza]
        Retorna la lista de piezas que se han creado y que se asignaran al jugador correspondiente
    """

    piezas = []

    fila_p : int = 6 if color else 1
    for j in range(8):
        peon = Peon((fila_p,j),color)
        piezas.append(peon)
        tablero[fila_p][j].pieza = peon

    fila_r : int = 7 if color else 0
    piezas_ext = [Torre((fila_r,0),color), Caballo((fila_r,1),color), Alfil((fila_r,2),color),
                  Reina((fila_r,3),color), Rey((fila_r,4),color, enemigo),
                  Alfil((fila_r,5),color), Caballo((fila_r,6),color), Torre((fila_r,7),color)]

    for pieza in piezas_ext:
        piezas.append(pieza)
        fila, columna = pieza.posicion
        tablero[fila][columna].pieza = pieza

    return piezas

def encontrar_pieza(tablero : "Tablero", jugador : "Jugador", origen : tuple[int]) -> Union["Pieza",None]:
    """
    Busca la pieza en la posicion de origen digitada por el jugador. Para lograrlo recorre toda la lista de piezas del
    jugador hasta dar con aquella cuya posicion coincide con la posicion origen digitada anteriormente.

    Parametros:
    -----------
    tablero : Tablero -> Tablero en sí. Solo está para comprobar si es exactamente esa pieza.

    jugador : Jugador -> Jugador que ha digitado el movimiento.

    origen : tuple[int] -> Es la posicion origen digitada por el jugador.

    Retorna:
    ----------
    Pieza
        Retorna la pieza que coincide su posicion con la posicion origen digitada. Si no se encuentra devuelve None.
    """

    for piezas in jugador.piezas:
        if origen == tuple(piezas.posicion):
            return piezas

    return None

def comprobar_enroque_corto(tablero : "Tablero", enemigo : "Jugador", rey : "Rey",
                            torre : "Torre") -> bool:
    """
    Comprueba si el enroque corto es posible. Para ello comprueba cada una de las exigencias que se deben cumplir para
    realizar un enroque. En este caso se comprueba el corto porque se necesita usar la torre de la derecha.

    Parametros:
    -----------
    tablero : Tablero -> Tablero en sí. De ella se obtienen las casillas intermedias entre el rey y la torre.

    enemigo : Jugador -> Jugador de color contrario. Usado para comprobar si sus piezas amenazan las casillas intermedias.

    rey : Rey -> Rey del jugador actual. Necesario para poder comprobar si puede hacer enroque.

    torre : Torre -> Torre del jugador actual. Necesario para poder comprobar si puede hacer enroque.

    Retorna:
    ----------
    bool
        Devuelve True si se ha producido el eroque corto
    """

    if not rey.enroque() or not torre.enroque():
        print("No pueden hacer enroque")
        return False

    intermedias = abs(rey.posicion[1] - torre.posicion[1])
    fila = 7 if rey.color else 0

    for j in range(1, intermedias):
        columna : int = rey.posicion[1] + j
        if tablero.amenazas(enemigo, fila, columna):
            print("Error. una casilla es amenazada por alguna pieza enemiga")
            return False

        if tablero[fila][columna].pieza is not None:
            print("Error. Camino no despejado")
            return False

    rey.posicion = (fila, 6)
    rey.movido = True
    tablero[fila][4].pieza = None
    tablero[fila][6].pieza = rey

    torre.posicion = (fila, 5)
    torre.movido = True
    tablero[fila][7].pieza = None
    tablero[fila][5].pieza = torre

    print("Enroque exitoso")

    return True

def comprobar_enroque_largo(tablero : "Tablero", enemigo : "Jugador", rey : "Rey",
                            torre : "Torre") -> bool:
    """
    Comprueba si el enroque corto es posible. Para ello comprueba cada una de las exigencias que se deben cumplir para
    realizar un enroque. En este caso se comprueba el corto porque se necesita usar la torre de la derecha.

    Parametros:
    -----------
    tablero : Tablero -> Tablero en sí. De ella se obtienen las casillas intermedias entre el rey y la torre.

    enemigo : Jugador -> Jugador de color contrario. Usado para comprobar si sus piezas amenazan las casillas intermedias.

    rey : Rey -> Rey del jugador actual. Necesario para poder comprobar si puede hacer enroque.

    torre : Torre -> Torre del jugador actual. Necesario para poder comprobar si puede hacer enroque.

    Retorna:
    ----------
    bool
        Devuelve True si se ha producido el eroque largo
    """

    if not rey.enroque() or not torre.enroque():
        print("No pueden hacer enroque")
        return False

    intermedias = abs(rey.posicion[1] - torre.posicion[1])
    fila = 7 if rey.color else 0

    for j in range(1, intermedias):
        columna: int = rey.posicion[1] - j
        if tablero.amenazas(enemigo, fila, columna):
            print("Error. una casilla es amenazada por alguna pieza enemiga")
            return False

        if tablero[fila][columna].pieza is not None:
            print("Error. Camino no despejado")
            return False

    rey.posicion = (fila, 2)
    rey.movido = True
    tablero[fila][4].pieza = None
    tablero[fila][2].pieza = rey

    torre.posicion = (fila, 3)
    torre.movido = True
    tablero[fila][0].pieza = None
    tablero[fila][3].pieza = torre

    print("Enroque exitoso")

    return True

def comprobar_promocion(pieza : "Peon", promocion : Union[str,int], jugador_actual : "Jugador", tablero : "Tablero") -> bool:
    """
    Comprueba si la promocion es válida. En caso afirmativo realiza la promoción correspondiente

    Parametros:
    -----------
    pieza : Peon -> Es el peon que se va a promocionar.

    promocion : Union[str,int] -> Promocion digitado por el usuario.

    jugador_actual : Jugador -> Dueño del peon que se va a promocionar

    Retorna:
    ----------
    bool
        Devuelve True si se ha producido la promocion
    """
    indice = jugador_actual.piezas.index(pieza)
    jugador_actual.piezas.remove(pieza)

    match promocion:
        case 'Q':
            pieza = Reina(pieza.posicion, pieza.color)
            jugador_actual.piezas.insert(indice,pieza)
            tablero[pieza.posicion[0]][pieza.posicion[1]].pieza = pieza

        case 'R':
            pieza = Torre(pieza.posicion, pieza.color)
            pieza.movido = True
            jugador_actual.piezas.insert(indice, pieza)
            tablero[pieza.posicion[0]][pieza.posicion[1]].pieza = pieza

        case 'B':
            pieza = Alfil(pieza.posicion, pieza.color)
            jugador_actual.piezas.insert(indice, pieza)
            tablero[pieza.posicion[0]][pieza.posicion[1]].pieza = pieza

        case 'N':
            pieza = Caballo(pieza.posicion, pieza.color)
            jugador_actual.piezas.insert(indice, pieza)
            tablero[pieza.posicion[0]][pieza.posicion[1]].pieza = pieza

        case _:
            print("Error. Se ha intentado promocionar a una pieza invalida")
            jugador_actual.piezas.insert(indice, pieza)
            return False

    print("Promoción exitosa")

    return True

def comprobar_jaque_enemigo(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador",
                            pieza : Union["Pieza",None]) -> bool:
    """
    Comprueba si el movimiento del jugador actual ha hecho jaque al enemigo.

    Parametros:
    -----------
    tablero : Tablero -> Tablero en sí.

    jugador_actual : Jugador -> Jugador que ha realizado el jaque.

    enemgio : Jugador -> Dueño del rey que se ha puesto en jaque.

    pieza : Pieza -> Pieza que ha sido movido y que podria haber puesto en jaque al enemigo

    Retorna:
    ----------
    bool
        Devuelve True si se ha producido un jaque
    """
    rey_enemigo = next((rey for rey in enemigo.piezas if isinstance(rey, Rey)), None)

    if rey_enemigo is None:
        return True

    if pieza is None:
        return True if tablero.amenazas(jugador_actual, rey_enemigo.posicion[0], rey_enemigo.posicion[1]) else False

    return True if rey_enemigo.posicion in pieza.movimiento_valido(tablero) else False

def caso_jaque(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador", movimiento : tuple) -> bool:
    """
    Función que trata el caso especial de jaque. En ella se tratan todos los casos posibles dentro de un jaque para
    determinar si el movimiento evita el jaque.

    Parametros:
    -----------
    tablero : Tablero -> Tablero en sí.

    jugador_actual : Jugador -> Jugador que ha recibido el jaque

    enemgio : Jugador -> Jugador que ha hecho jaque

    movimiento : tuple -> Movimiento digitado por el jugador actual

    Retorna:
    ----------
    bool
        Retorna True si ha evitado el jaque
    """
    if type(movimiento[2]) == int and movimiento[2] in [1,2]:
        print("Error. Se ha intentado hacer un enroque en medio de un jaque")
        return False

    pieza : Union["Pieza",None] = encontrar_pieza(tablero, jugador_actual, movimiento[0])
    if pieza is None:
        print("Error. No se ha encontrado ninguna pieza.")
        return False

    if str(movimiento[2]).isalpha() and not isinstance(pieza, Peon):
        print("Error. Se ha intentado promocionar una pieza que no es peón.")
        return False

    rey = next((rey for rey in jugador_actual.piezas if isinstance(rey, Rey)), None)
    if rey is None:
        print("Error. No se ha encontrado el rey")
        return False

    if not pieza.mover(movimiento[1], tablero, jugador_actual, enemigo, str(movimiento[2])):
        print("El movimiento es inválido (autojaque, movimiento impromio de la pieza, etc)")
        return False

    return True

def comprobar_tablas(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador") -> bool:
    """
    Comprueba si se ha producido un empate

    Parametros:
    -----------
    tablero : Tablero -> Tablero en sí.

    jugador_actual : Jugador -> Jugador que ha realizado el jaque.

    enemgio : Jugador -> Dueño del rey que se ha puesto en jaque.

    Retorna:
    ----------
    bool
        Devuelve True si son tablas
    """
    if len(jugador_actual.piezas) == 1 or len(enemigo.piezas) == 1:
        return True

    rey = next((rey for rey in jugador_actual.piezas if isinstance(rey, Rey)), None)
    if rey is None:
        print("Error: No se encontró el rey del jugador.")
        return True

    if tablero.amenazas(enemigo, rey.posicion[0], rey.posicion[1]):
        return False

    for pieza in jugador_actual.piezas:
        movimientos = pieza.movimiento_valido(tablero) if not isinstance(pieza, Rey) else []
        if movimientos:
            return False

    return True

if __name__ == "__main__":
    jug1 = Jugador("Carlos",1000)
    jug2 = Jugador("Jorgis",2300)
    partida(jug1,jug2)