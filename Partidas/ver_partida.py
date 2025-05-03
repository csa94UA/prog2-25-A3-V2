"""
Modulo encargado en la visualización de una partida antigua.

Este modulo proporciona funciones destinados a visualizar una partida antigua desde la perspectiva del jugador que lo ve.
Además, incluye una serie de facilidades para desplazarse entre movimientos, visualizar movimientos en fomrato FEN, ver
turnos que tiene la partida, etc.

Funciones:

"""

from Piezas import Caballo, Alfil, Rey, Reina, Peon, Torre, Pieza
from Jugador import Jugador
from Tablero import Tablero
from aflabeto_FEN import *
from Base_de_datos import guardar_partida
import pygame
import json
import time

def visualizar_partida_antigua(archivo : str, jugador_actual : Jugador, enemigo : Jugador) -> None:
    partida : list[dict] = cargar_partida_json(archivo)
    enlistar_partida(partida, jugador_actual, enemigo)

    while True:
        try:
            indice = int(input("\nDigite el indice de la partida que desea reproducir: "))
            if not(0 <= int(indice) < len(partida)):
                raise ValueError("Error. Has digitado un índice fuera de los límites")
            break
        except ValueError as error_valor:
            print(error_valor)
        except TypeError:
            print("No has digitado un número")

    fens : list[str] = partida[indice]["fens"]
    turno : int = 0
    running : bool = True
    reloj = pygame.time.Clock()

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    turno = min(indice + 1, len(partida[indice]) - 1)
                elif evento.key == pygame.K_LEFT:
                    turno = max(indice - 1, 0)

        tablero = Tablero.creacion_con_FEN(fens[turno])
        print(tablero)
        reloj.tick(30)

    pygame.quit()

    return None

def cargar_partida_json(archivo : str) -> str:
    with open(f"{archivo}.json", 'r') as lectura:
        return json.load(lectura)

def enlistar_partida(partidas : list[dict], jugador_actual : Jugador, enemigo : Jugador) -> None:
    for i,partida in enumerate(partidas):
        print(f"{i}: {partida['jugador_blanco']} contra {partida['jugador_negro']}. Resultado -> {partida['resultado']}")

    return None