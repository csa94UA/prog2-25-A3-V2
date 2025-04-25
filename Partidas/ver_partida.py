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

        except ValueError as error_valor:
            print(error_valor)
        except TypeError:
            print("No has digitado un número")
        else:
            break
        finally:
            continue

    for turno, fen in enumerate(partida[indice]["partida"]):
        tablero = Tablero.creacion_con_FEN(fen)
        print(tablero)
        reloj = pygame.time.Clock()
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    break
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RIGHT:
                        min(indice + 1, len(partida[indice]) - 1)
                    elif evento.key == pygame.K_LEFT:
                        max(indice - 1, 0)

            reloj.tick(30)

    pygame.quit()

    return None

def cargar_partida_json(archivo : str) -> str:
    with open(f"{archivo}.json", 'r') as lectura:
        return json.load(lectura)

def enlistar_partida(partidas : list[dict], jugador_actual : Jugador, enemigo : Jugador) -> None:
    for i,partida in enumerate(partidas):
        print(f"{i}: {partida[f'{jugador_actual}']} contra {partida[f'{enemigo}']}. Resultado -> {partida['Resultado']}")

    return None