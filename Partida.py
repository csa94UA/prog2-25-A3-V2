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

def partida(jugador1 : Jugador, jugador2 : Jugador) -> bool:

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

    game_over = False
    jaque : bool = False
    turno = 1 if jugador1.color else 0

    while not game_over:
        jugador_actual : Jugador = jugador1 if turno else jugador2
        enemigo : Jugador = jugador1 if not turno else jugador2

        tablero.mostrar_tablero(jugador_actual.color)

        movimiento = digitar_movimiento()



        #Busca la pieza en esa posicion. Si no la encuentra, dará un mensaje de error y repetirá el movimiento
        encontrado : bool = False
        pieza : Union[Pieza,None] = None
        for piezas in jugador_actual.piezas:
            if movimiento[0] == piezas.posicion:
                pieza = piezas
                encontrado = True
                break

        if not encontrado:
            print("Error. No se ha encontrado ninguna pieza.")
            continue

        if movimiento[2].isalpha() and not isinstance(pieza, Peon):
            print("Error. Se ha intentado promocionar con una pieza que no es peon")
            continue

        rey = next((rey for rey in jugador_actual.piezas if isinstance(rey, Rey)), None)

        #Comprobamos si quieren hacer enroque. Si es así se simula y se comprueba su validez
        if movimiento[2].isdigit() and movimiento[2] != 0:

            torre = next((torre for torre in jugador_actual.piezas if isinstance(torre, Torre) \
                          and torre.posicion[0] == 7), None)

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
                #Regresa al bucle con todas las demás comprobaciones hechas

        pos_antigua = pieza.posicion

        if not pieza.mover(movimiento[1], tablero, jugador_actual, enemigo, rey.posicion, movimiento[2]):
            print("El movimiento es inválido (autojaque, movimiento impromio de la pieza, etc")

        #En caso de que sea un peon y se haya digitado una promoción, debemos comprobar si es válida. En caso afirmativo
        #transformamos ese peon a la pieza deseada


        if movimiento[2].isalpha():

            intento : bool = comprobar_promocion(pieza, movimiento[2])

            if not intento:
                print("Error. No se ha podido realizar la promoción")
                continue

        #Vemos si produce la pieza un jaque. En caso afirmativo lo guardamos para el jugador del siguiente turno
        rey = next((rey for rey in enemigo.piezas if isinstance(rey, Rey)), None)
        if rey.posicion in pieza.movimiento_valido(tablero):
            jaque : bool = True
            if tablero.jaque_in(rey.posicion[0], rey.posicion[1], enemigo, jugador_actual):
                break







        turno = 1 - turno



def crear_piezas(color : bool, tablero : Tablero) -> list:

    piezas = []

    fila_p : int = 6 if color else 1
    for j in range(8):
        peon = Peon([fila_p,j],color)
        piezas.append(peon)
        tablero[fila_p][j].pieza = peon

    fila_r : int = 7 if color else 0
    piezas_ext = [Torre([fila_r,0],color), Caballo([fila_r,1],color), Alfil([fila_r,2],color),
                  Reina([fila_r,3],color), Rey([fila_r,4],color),
                  Torre([fila_r,5],color), Caballo([fila_r,6],color), Alfil([fila_r,7],color)]

    for pieza in piezas_ext:
        piezas.append(pieza)
        fila, columna = pieza.posicion
        tablero[fila][columna].pieza = pieza

    return piezas

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

    match (promocion):
        case 'Q':
            pieza = Reina(pieza.posicion, pieza.color)

        case 'R':
            pieza = Torre(pieza.posicion, pieza.color)
            pieza.movido = True

        case 'B':
            pieza = Alfil(pieza.posicion, pieza.color)

        case 'N':
            pieza = Caballo(pieza.posicion, pieza.color)

        case _:
            print("Error. Se ha intentado promocionar a una pieza invalida")
            return False

    return True