"""
Modulo destinado a guardar una partida.

Esta destinado a guardar las partidas que están a mitad o terminadas. Para guardarlas se empleará el archivo .json gracias
a su estructura de diccionario y la partida se almacenara en formato FEN por su facilidad de ser traducido.

Clase:
    GuardarPartida
"""

from typing import Self, Union
import json

class GuardarPartida:

    def __init__(self, jugador1 : str, jugador2 : str, ) -> None:
        self.jugador_b : str = jugador1
        self.jugador_n : str = jugador2
        self.mov_LAN : list = []
        self.fen : list = []
        self.resultado : str = '0-0'

    def __iadd__(self, other : list[str,str]) -> Self:
        self.mov_LAN.append(other[0])
        self.fen.append(other[1])
        return self

    def resultado_partida(self, resultado : str) -> None:
        self.resultado = resultado
        return None

    def transfomracion_a_json(self, archivo : str) -> None:
        informacion = {
            'jugador_blanco' : self.jugador_b,
            'jugador_negro' : self.jugador_n,
            'jugadas' : self.mov_LAN,
            'tablero' : self.fen,
            'resultado' : self.resultado
        }

        with open(f"{archivo}.json", 'w') as escritura:
            json.dump(informacion, escritura, ident = 4)

        return None

    def transformacion_a_pgn(self) -> str:
        pgn = [
            f'[White "{self.jugador_b}"]',
            f'[Black "{self.jugador_n}"]',
            f'[Result "{self.resultado}"]',
            f'[FEN "{self.fen}"]',
            ""
        ]

        movimientos : str = ""
        for i, jugada in enumerate(self.mov_LAN):
            if i % 2:
                movimientos += f"{jugada} "
            else:
                movimientos += f"{(i // 2) + 1}. {jugada} "

        movimientos += self.resultado
        pgn.append(movimientos)

        return '\n'.join(pgn)

    def json_a_pgn(self, archivo : str):

        with open(f"{archivo}.json", 'r') as lectura:
            partida = json.load(lectura)

        pgn = f'[Event "Partida {partida["jugador_blanco"]} vs {partida["jugador_negro"]}"], '
        f'[White "{partida["jugador_b"]}"], '
        f'[Black "{partida["jugador_negro"]}"], '
        f'[Result "{partida["resultado"]}"], '
        f'[FEN "{partida["fen"][0]}]'

        movimientos = partida["jugadas"]
        for i in range(0, len(movimientos), 2):
            jugada_b = movimientos[i]
            jugada_n = movimientos[i+1] if i+1 < len(movimientos) else ""
            pgn += f"{(i // 2) + 1}. {jugada_b} {jugada_n} "

        pgn += f"\n\n{partida['resultado']}\n"

        with open("partida_convertida.pgn", "w", encoding="utf-8") as f:
            f.write(pgn)