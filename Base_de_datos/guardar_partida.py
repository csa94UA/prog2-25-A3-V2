"""
Modulo destinado a guardar una partida.

Esta destinado a guardar las partidas que están a mitad o terminadas. Para guardarlas se empleará el archivo .json gracias
a su estructura de diccionario y la partida se almacenara en formato FEN por su facilidad de ser traducido.

Clase:
    GuardarPartida
"""

import json
from Base_de_datos.operacoines_pandas import upsert_en_curso, finalize_to_csv
from Base_de_datos.operaciones_sqlite import añadir_partida_y_movimientos
from datetime import datetime
import os

DIR_JSON = 'Base_de_datos/datos/archivos_json'

class GuardarPartida:

    def __init__(self, game_id : str, jugador1 : str, jugador2 : str,*, en_curso) -> None:
        self.game_id = game_id
        self.blancas_id = jugador1
        self.negras_id = jugador2
        self.jugadas = []
        self.resultado = '0-0'
        self.inicio = datetime.utcnow()

        os.makedirs(DIR_JSON, exist_ok=True)
        self.json_path = os.path.join(DIR_JSON, f"{self.game_id}_temp.json")
        print("En curso: ", en_curso)
        if not en_curso:
            print(self.jugadas)
            upsert_en_curso(self.game_id, self.blancas_id, self.negras_id, fen=self.jugadas[-1][1] if self.jugadas else "", turno=0, ultimo_mov="")
            self._guardar_json()
        else:
            self.cargar_partida_intermedia()

    def __iadd__(self, other: tuple[str, str]):
        self.jugadas.append(other)
        self._guardar_json()
        return self

    def cargar_partida_intermedia(self) -> None:
        with open(self.json_path, 'rb') as lectura:
            mucho_bit = lectura.read()
            mucho_texto = mucho_bit.decode('utf-8')
            carga = json.loads(mucho_texto)
            movimientos = carga['movimientos']

        self.jugadas = [(caso['lan'], caso['fen']) for caso in movimientos]

        return None

    def agregar_turno(self, mov_LAN: str, fen: str, turno: int):
        self += (mov_LAN, fen)
        upsert_en_curso(self.game_id, self.blancas_id, self.negras_id, fen=fen, turno=turno, ultimo_mov=mov_LAN)

    def finalizar(self, resultado: str):
        self.resultado = resultado
        duracion = int((datetime.utcnow() - self.inicio).total_seconds())

        self._guardar_json(True)

        finalize_to_csv(self.game_id, self.resultado)

        movimientos = [(i + 1, lan, fen) for i, (lan, fen) in enumerate(self.jugadas)]
        añadir_partida_y_movimientos(self.blancas_id, self.negras_id, self.resultado, duracion, movimientos)

    def resultado_partida(self, resultado : str) -> None:
        self.resultado = resultado
        return None

    def _guardar_json(self, final = False):
        informacion = {
            "jugador_blanco": self.blancas_id,
            "jugador_negro": self.negras_id,
            "fecha_inicio": self.inicio.isoformat(),
            "fecha_fin": datetime.utcnow().isoformat() if final else None,
            "resultado": self.resultado,
            "movimientos": [{"lan": lan, "fen": fen} for lan, fen in self.jugadas]
        }

        with open(self.json_path, 'w') as escritura:
            json.dump(informacion, escritura, indent=4)

        return None

    def transformacion_a_pgn(self) -> str:
        pgn = [
            f'[White "{self.blancas_id}"]',
            f'[Black "{self.negras_id}"]',
            f'[Result "{self.resultado}"]',
            f'[FEN "{self.jugadas[0]}"]',
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
        f'[White "{partida["jugador_blanco"]}"], '
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