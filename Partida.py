"""
Modulo para la ejecucion de una partida, ya sea JcJ, JcE o EcE.

Este modulo proporciona funciones para el intercambio de turnos, manejo de excepciones e
inicialización de la partida.

Funciones:
    - partida(jugador1 : Jugador, jugador2 : Jugador) -> bool: Simula la partida y determina el ganador
    - crear_piezas(color : bool, tablero : Tablero) -> list[Pieza]: Inicializa el tablero y las fichas de cada jugador

"""

from Piezas import Caballo, Alfil, Rey, Reina, Peon, Torre
from Tablero import Tablero
from Jugador import Jugador
from random import randint
from aflabeto_FEN import digitar_movimiento

def partida(jugador1 : Jugador, jugador2 : Jugador):

    if randint(0,1000) < 499:
        jugador1.color = 1
        jugador2.color = 0
    else:
        jugador2.color = 1
        jugador1.color = 0

    tablero = Tablero()

    jugador1.piezas = crear_piezas(jugador1.color, tablero)
    jugador2.piezas = crear_piezas(jugador2.color, tablero)

    game_over = False
    turno = 1 if jugador1.color else 0

    while not game_over:
        jugador_actual = jugador1 if turno else jugador2

        tablero.mostrar_tablero(jugador_actual.color)

        movimiento = digitar_movimiento(tablero, jugador_actual)



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


