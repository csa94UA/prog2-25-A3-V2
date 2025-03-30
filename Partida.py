from Piezas import Caballo, Alfil, Rey, Reina, Peon, Torre, Pieza
from Tablero import Tablero
from Jugador import Jugador
from random import randint
from typing import Union
from aflabeto_FEN import digitar_movimiento
"""
Modulo para la ejecucion de una partida, ya sea JcJ, JcE o EcE.

Este modulo proporciona funciones para el intercambio de turnos, manejo de excepciones e
inicialización de la partida.

Funciones:
    - partida(jugador1 : Jugador, jugador2 : Jugador) -> bool: Simula la partida y determina el ganador
    - crear_piezas(color : bool, tablero : Tablero) -> list[Pieza]: Inicializa el tablero y las fichas de cada jugador

"""

def partida(jugador1 : Jugador, jugador2 : Jugador) -> Union["Jugador",None]:

    #Establecemos un inicio de turno aleatorio
    if randint(0,1000) < 499:
        jugador1.color = 1
        jugador2.color = 0
    else:
        jugador2.color = 1
        jugador1.color = 0

    tablero = Tablero() #Cargamos tablero

    #Insertamos las piezas en el tablero y en el inventario del jugador
    jugador1.piezas = crear_piezas(jugador1.color, tablero)
    jugador2.piezas = crear_piezas(jugador2.color, tablero)

    game_over : bool = False
    jaque : bool = False
    turno = 1 if jugador1.color else 0
    jugador_actual : Union["Jugador",None] = None

    print("Inicialización correcta")

    while not game_over:
        jugador_actual = jugador1 if turno else jugador2
        enemigo : Jugador = jugador1 if not turno else jugador2

        tablero.mostrar_tablero(jugador_actual.color)

        print("Tablero mostrado")

        if comprobar_tablas(tablero, jugador_actual, enemigo):
            jugador_actual = None #Nadie gana
            print("Nadie gana")
            break

        print("Se digita movimiento")
        movimiento = digitar_movimiento(jugador_actual.color)

        if jaque:
            intento : bool = caso_jaque(tablero, jugador_actual, enemigo, movimiento)

            if not intento:
                continue

            else:
                jaque = True if comprobar_jaque_enemigo(tablero, jugador_actual, enemigo, None) else False
                turno = 1 - turno

        #Busca la pieza en esa posicion. Si no la encuentra, dará un mensaje de error y repetirá el movimiento

        pieza : Union["Pieza",None] = encontrar_pieza(tablero, jugador_actual, enemigo, movimiento[0])

        if pieza is None:
            print("Error. No se ha encontrado ninguna pieza.")
            continue

        if str(movimiento[2]).isalpha() and not isinstance(pieza, Peon):
            print("Error. Se ha intentado promocionar con una pieza que no es peon")
            continue

        rey = next((rey for rey in jugador_actual.piezas if isinstance(rey, Rey)), None)

        #Comprobamos si quieren hacer enroque. Si es así se simula y se comprueba su validez
        if type(movimiento[2]) == int and movimiento[2] in [1,2]:

            torre = next((torre for torre in jugador_actual.piezas if isinstance(torre, Torre) \
                          and torre.posicion[0] in [0,7]), None)

            if torre is None:
                print("No se ha encontrado una torre para hacer enroque")
                continue

            pos_rey = rey.posicion
            pos_torre = torre.posicion

            intento = comprobar_enroque_corto(tablero, enemigo, rey, torre) if movimiento[2] == 1 else \
                comprobar_enroque_largo(tablero, enemigo, rey, torre)

            if not intento:
                rey.posicion = pos_rey
                torre.posicion = pos_torre
                print("No ha sido posible hacer el enroque")
                continue

            else:
                jaque: bool = comprobar_jaque_enemigo(tablero, jugador_actual, enemigo, torre)

                if tablero.jaque_in(rey.posicion[0], rey.posicion[1], enemigo, jugador_actual):
                    break

        pos_antigua = pieza.posicion

        if not pieza.mover(movimiento[1], tablero, jugador_actual, enemigo, rey.posicion, str(movimiento[2])):
            print("El movimiento es inválido (autojaque, movimiento impromio de la pieza, etc")

        if isinstance(pieza, Torre) or isinstance(pieza, Rey) or isinstance(pieza, Peon):
            pieza.movido = True

        #En caso de que sea un peon y se haya digitado una promoción, debemos comprobar si es válida. En caso afirmativo
        #transformamos ese peon a la pieza deseada

        if str(movimiento[2]).isalpha():

            intento : bool = comprobar_promocion(pieza, movimiento[2], jugador_actual)

            if not intento:
                print("Error. No se ha podido realizar la promoción")
                continue

        #Vemos si produce la pieza un jaque. En caso afirmativo lo guardamos para el jugador del siguiente turno
        jaque : bool = comprobar_jaque_enemigo(tablero, jugador_actual, enemigo, pieza)

        if jaque and tablero.jaque_in(rey.posicion[0], rey.posicion[1], enemigo, jugador_actual):
            break

        turno = 1 - turno

    return jugador_actual



def crear_piezas(color : int, tablero : Tablero) -> list:

    piezas = []

    fila_p : int = 6 if color else 1
    for j in range(8):
        peon = Peon((fila_p,j),color)
        piezas.append(peon)
        tablero[fila_p][j].pieza = peon

    fila_r : int = 7 if color else 0
    piezas_ext = [Torre((fila_r,0),color), Caballo((fila_r,1),color), Alfil((fila_r,2),color),
                  Reina((fila_r,3),color), Rey((fila_r,4),color),
                  Torre((fila_r,5),color), Caballo((fila_r,6),color), Alfil((fila_r,7),color)]

    for pieza in piezas_ext:
        piezas.append(pieza)
        fila, columna = pieza.posicion
        tablero[fila][columna].pieza = pieza

    return piezas

def encontrar_pieza(tablero : "Tablero", jugador : "Jugador", enemgio : "Jugador",
                    origen : tuple[int]) -> Union["Pieza",None]:

    for piezas in jugador.piezas:
        if origen == tuple(piezas.posicion):
            print(piezas.movimiento_valido(tablero))
            print(piezas.posicion)
            return piezas

    return None

def comprobar_enroque_corto(tablero : "Tablero", enemigo : "Jugador", rey : "Rey",
                            torre : "Torre") -> bool:

    if not rey.enroque() or not torre.enroque():
        return False

    intermedias = abs(rey.posicion[1] - torre.posicion[1])
    fila = 7 if rey.color else 0

    for j in range(1, intermedias + 1):
        columna : int = rey.posicion[1] + j
        if tablero.amenazas(enemigo, fila, columna):
            return False

        if tablero[fila][columna].pieza is not None:
            return False

    rey.posicion = (fila, 6)
    rey.movido = True
    tablero[fila][4].pieza = None
    tablero[fila][6].pieza = rey

    torre.posicion = (fila, 5)
    torre.movido = True
    tablero[fila][7].pieza = None
    tablero[fila][5].pieza = torre

    return True

def comprobar_enroque_largo(tablero : "Tablero", enemigo : "Jugador", rey : "Rey",
                            torre : "Torre") -> bool:

    if not rey.enroque() or not torre.enroque():
        return False

    intermedias = abs(rey.posicion[1] - torre.posicion[1])
    fila = 7 if rey.color else 0

    for j in range(1, intermedias + 1):
        columna: int = rey.posicion[1] - j
        if tablero.amenazas(enemigo, fila, columna):
            return False

        if tablero[fila][columna].pieza is not None:
            return False

    rey.posicion = (fila, 2)
    rey.movido = True
    tablero[fila][4].pieza = None
    tablero[fila][2].pieza = rey

    torre.posicion = (fila, 3)
    torre.movido = True
    tablero[fila][0].pieza = None
    tablero[fila][3].pieza = torre

    return True

def comprobar_promocion(pieza : "Peon", promocion : Union[str,int], jugador_actual : "Jugador") -> bool:

    indice = jugador_actual.piezas.index(pieza)

    match (promocion):
        case 'Q':
            pieza = Reina(pieza.posicion, pieza.color)
            jugador_actual.piezas[indice] = pieza

        case 'R':
            pieza = Torre(pieza.posicion, pieza.color)
            pieza.movido = True
            jugador_actual.piezas[indice] = pieza

        case 'B':
            pieza = Alfil(pieza.posicion, pieza.color)
            jugador_actual.piezas[indice] = pieza

        case 'N':
            pieza = Caballo(pieza.posicion, pieza.color)
            jugador_actual.piezas[indice] = pieza

        case _:
            print("Error. Se ha intentado promocionar a una pieza invalida")
            return False

    return True

def comprobar_jaque_enemigo(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador",
                            pieza : Union["Pieza",None]) -> bool:

    rey_enemigo = next((rey for rey in enemigo.piezas if isinstance(rey, Rey)), None)

    if rey_enemigo is None:
        return True

    if pieza is None:
        return True if tablero.amenazas(jugador_actual, rey_enemigo.posicion[0], rey_enemigo.posicion[1]) else False

    return True if rey_enemigo.posicion in pieza.movimiento_valido(tablero) else False

def caso_jaque(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador", movimiento : tuple) -> bool:

    if type(movimiento[2]) == int and movimiento[2] in [1,2]:
        print("Error. Se ha intentado hacer un enroque en medio de un jaque")
        return False

    pieza : Union["Pieza",None] = encontrar_pieza(tablero, jugador_actual, enemigo, movimiento[0])
    if pieza is None:
        print("Error. No se ha encontrado ninguna pieza.")
        return False

    if movimiento[2].isalpha() and not isinstance(pieza, Peon):
        print("Error. Se ha intentado promocionar una pieza que no es peón.")
        return False

    rey = next((rey for rey in jugador_actual.piezas if isinstance(rey, Rey)), None)
    if rey is None:
        print("Error. No se ha encontrado el rey")
        return False

    if not pieza.mover(movimiento[1], tablero, jugador_actual, enemigo, rey.posicion, str(movimiento[2])):
        print("El movimiento es inválido (autojaque, movimiento impromio de la pieza, etc")
        return False

    return True

def comprobar_tablas(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador") -> bool:

    if len(jugador_actual.piezas) != 1 or len(enemigo.piezas) != 1:
        return False

    rey = next((rey for rey in jugador_actual.piezas if isinstance(rey, Rey)), None)
    if rey is None:
        print("Error: No se encontró el rey del jugador.")
        return True

    if tablero.amenazas(enemigo, rey.posicion[0], rey.posicion[1]):
        return False

    # Verificamos si al menos una pieza tiene un movimiento legal.
    # Se asume que 'movimiento_valido' ya filtra los movimientos que producirían autojaque.
    for pieza in jugador_actual.piezas:
        movimientos = pieza.movimiento_valido(tablero)
        if movimientos:  # Si hay al menos un movimiento válido
            return False

    return True

if __name__ == "__main__":
    jug1 = Jugador("Carlos",1000)
    jug2 = Jugador("Jorgis",2300)
    partida(jug1,jug2)