"""
Modulo para la ejecucion de una partida, ya sea JcJ, JcE o EcE.

Este modulo proporciona funciones para el intercambio de turnos, manejo de excepciones e
inicialización de la partida.

Funciones:
    - partida(jugador1 : Jugador, jugador2 : Jugador) -> bool: Simula la partida y determina el ganador
    - crear_piezas(color : bool, tablero : Tablero) -> list[Pieza]: Inicializa el tablero y las fichas de cada jugador

"""

from Piezas import Caballo, Alfil, Rey, Reina, Peon, Torre, Pieza
from Tablero import Tablero
from Jugador import Jugador
from random import randint
from typing import Union
from aflabeto_FEN import digitar_movimiento

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

        #Comprobamos que dicha pieza puede moverse a esa posición. En caso contrario se regresa al bucle del principio.
        if not movimiento[1] in pieza.movimiento_valido(tablero):
            print("Error. LA posición desitno no está dentro de los movimientos validos de la pieza")
            continue

        #Simulamos que movemos la pieza a la casilla destino y comprobamos primero si se produce un jaque inmediato.
        #en caso de que se produzca, el movimiento queda inválido. Se debe tener mucho cuidado Y NO AFECTAR AL TABLERO.

        pos_antigua : tuple = pieza.posicion
        pieza.posicion = movimiento[1]
        rey = next((rey for rey in jugador_actual.piezas if isinstance(rey,Rey)), None)
        if tablero.amenazas(enemigo, rey.posicion[0], rey.posicion[1]):
            print("Error. Tu movimiento provoca o no impide un jaque")
            pieza.posicion = pos_antigua
            continue

        #En caso de que sea un peon y se haya digitado una promoción, debemos comprobar si es válida. En caso afirmativo
        #transformamos ese peon a la pieza deseada
        if movimiento[2] is not None:

            if not pieza.posicion[0] == 0 and not pieza.posicion[0] == 7:
                print("Error. No se encuentra en el otro lado del tablero")
                pieza.posicion = pos_antigua
                continue

            if not isinstance(pieza,Peon):
                print("Error. Intento de hacer promoción con una pieza que no es peón")
                pieza.posicion = pos_antigua
                continue

            match(movimiento[2]):
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
                    continue

        #Vemos si produce la pieza un jaque. En caso afirmativo lo guardamos para el jugador del siguiente turno
        rey = next((rey for rey in enemigo.piezas if isinstance(rey, Rey)), None)
        if rey.posicion in pieza.movimiento_valido(tablero):
            jaque : bool = True
        








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


