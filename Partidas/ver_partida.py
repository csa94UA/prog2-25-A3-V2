"""
Modulo encargado en la visualización de una partida antigua.

Este modulo proporciona funciones destinados a visualizar una partida antigua desde la perspectiva del jugador que lo ve.
Además, incluye una serie de facilidades para desplazarse entre movimientos, visualizar movimientos en fomrato FEN, ver
turnos que tiene la partida, etc.

Funciones:

"""
from typing import Optional
from Tablero import Tablero
import json
import os

DIR_JSON = 'Base_de_datos/datos/archivos_json'

def visualizar_partida_antigua(game_id : str) -> None:
    partida = cargar_partida_json(game_id)
    jugadas = partida.get('movimientos', [])
    fens = [jugada["fen"] for jugada in jugadas]

    turno : int = 0
    total = len(fens)
    print(f"Partida: {partida['jugador_blanco']} vs {partida['jugador_negro']}. Resultado: {partida['resultado']}")

    while True:
        print(f"Jugada {turno + 1}/{len(fens)} — {jugadas[turno]['lan']}")
        print(Tablero.creacion_con_FEN(fens[turno]))

        while True:
            opcion = input("\n[s] Siguiente   [a] Anterior   [q] Salir: ")
            if opcion == 'q':
                break
            elif opcion == 's':
                turno += 1 if turno < total - 1 else 0
                break
            elif opcion == 'a':
                turno -= 1 if turno > 0 else 0
                break
            else:
                print("\nNo has digitado una opción válida\n")

        if opcion == 'q':
            break


    return None

def cargar_partida_json(game_id : str) -> Optional[dict]:
    if not os.path.exists(f"{DIR_JSON}/{game_id}.json"):
        game_id += '_temp'
    try:
        with open(f"{DIR_JSON}/{game_id}.json", 'r') as lectura:
            return json.load(lectura)
    except FileNotFoundError:
        print(f"No se ha encontrado el fichero {game_id}")
        return None

def enlistar_partidas_json() -> list[str]:
    return [fichero[:-5] for fichero in os.listdir(DIR_JSON) if fichero.endswith('_temp.json') or fichero.endswith('.json')]

def visualizar_y_seleccionar_partidas() -> None:
    partidas = enlistar_partidas_json()
    if not partidas:
        print("No se han encontrado partidas\n")
        return None

    print("Se han encontrado las siguientes partidas: ")
    for i, game_id in enumerate(partidas):
        partida = cargar_partida_json(game_id)
        print(f"{i}: {game_id} — {partida['jugador_blanco']} vs {partida['jugador_negro']} ({partida['resultado']})")

    while True:
        try:
            indice = int(input("Introduce el índie de la partida que desea reproducir: "))
            if 0 <= indice < len(partidas):
                break
            else:
                raise ValueError("Error. Has digitado un indice que no existe.")

        except ValueError as indice_incorrecto:
            print(indice_incorrecto)
            continue
        except TypeError:
            print("Error. No has digitado un índice")
            continue

    visualizar_partida_antigua(partidas[indice])

    return None

if __name__ == '__main__':
    visualizar_y_seleccionar_partidas()