"""
Modulo destinado a guardar una partida.

Esta destinado a guardar las partidas que están a mitad o terminadas. Para guardarlas se empleará el archivo .json gracias
a su estructura de diccionario y la partida se almacenara en formato FEN por su facilidad de ser traducido.

Clase:
    GuardarPartida
"""

import json
from typing import Self
from Base_de_datos.operacoines_pandas import upsert_en_curso, finalize_to_csv
from Base_de_datos.operaciones_sqlite import añadir_partida_y_movimientos
from datetime import datetime
import os

DIR_JSON = 'Base_de_datos/datos/archivos_json'

class GuardarPartida:
    """
    Clase encargada de almacenar cada situación de la partida en archivos .json y .csv además de meterlo finalmente a la
    base de datos.

    Atributos:
    ---------
    game_id : str
        Nombre de la partida

    blancas_id : str
        Nombre del jugador blanco

    negras_id : str
        Nombre del jugador negro

    jugadoas : list
        Lista de cada una de las situaciones del tablero junto con su movmiento

    resultado : str
        Resultado de la partida

    inicio : datetime
        Fehca inicio de la partida

    Metodos:
    -------
    __init__(self, game_id : str, jugador1 : str, jugador2 : str,*, en_curso) -> None
        Inicializa un nuevo objeto de la clase GuardarPartida.

    __iadd__(self, other: tuple[str, str]) -> Self
        Añade una nueva jugada al objeto mediante la suma inmediata +=

    cargar_partida_intermedia(self) -> None
        Carga una partida en curso

    agregar_turno(self, mov_LAN: str, fen: str, turno: int) -> None
        Agrega un nuevo turno con su movimiento LAN y el fomrato FEN

    finalizar(self, resultado: str) -> None
        Almacena toda la informacion en un archivo .json y en la base de datos

    _guardar_json(self, final : bool = False) -> None
        Guarda la informacion en un archivo .json

    transformacion_a_pgn(self) -> str
        Transforma su información a pgn

    json_a_pgn(self, archivo : str) -> None
        Transforma un archivo json a pgn
    """

    def __init__(self, game_id : str, jugador1 : str, jugador2 : str,*, en_curso) -> None:
        """
        Inicializa una instancia de la clase GuardarPartida. Si la partida está en curso cargará sus atributos con la
        información que encuentre en el archivo {game_id}_temp.json

        Parametros:
        ----------
        game_id : str
            Nombre de la partida

        jugador1 : str
            Nombre del jugador blanco

        jugador2 : str
            Nombre del jugador negro

        en_curso : bool
            Valor booleano que marca si se está cargando una partida en curso o no
        """
        self.game_id = game_id
        self.blancas_id = jugador1
        self.negras_id = jugador2
        self.jugadas = []
        self.resultado = '0-0'
        self.inicio = datetime.utcnow()

        os.makedirs(DIR_JSON, exist_ok=True)
        self.json_path = os.path.join(DIR_JSON, f"{self.game_id}_temp.json")

        if not en_curso:
            upsert_en_curso(self.game_id, self.blancas_id, self.negras_id, fen=self.jugadas[-1][1] if self.jugadas else "", turno=0, ultimo_mov="")
            self._guardar_json()
        else:
            self.cargar_partida_intermedia()

    def __iadd__(self, other: tuple[str, str]) -> Self:
        """
        Metodo dunder para añadir una nueva jugada.

        Parametros:
        -----------
        other : tuple[str, str]
            tupla que contiene el formato FEN de la partida y su movimiento LAN hipersimplificado

        Retorna:
        --------
        Self
            Retorna su propia instancia actualizada
        """
        self.jugadas.append(other)
        self._guardar_json()
        return self

    def cargar_partida_intermedia(self) -> None:
        """
        Carga una partida intermedia de nombre {game_id}_temp.json
        """
        with open(self.json_path, 'rb') as lectura:
            mucho_bit = lectura.read()
            mucho_texto = mucho_bit.decode('utf-8')
            carga = json.loads(mucho_texto)
            movimientos = carga['movimientos']

        self.jugadas = [(caso['lan'], caso['fen']) for caso in movimientos]

        return None

    def agregar_turno(self, mov_LAN: str, fen: str, turno: int, detencion : bool = False) -> None:
        """
        Agrega nueva infomración de la partida tras terminar el turno

        Parametros:
        -----------
        mov_LAN : str
            Movimiento LAN hipersimplificado digitado en el turno

        fen : str
            Formato FEN del tablero en el turno

        turno : int
            Turno de la partida

        detencion : bool
            Marca si se ha producido una partada en la partida. Si es así, no se añade a .json
        """
        if not detencion:
            self += (mov_LAN, fen)
        upsert_en_curso(self.game_id, self.blancas_id, self.negras_id, fen=fen, turno=turno, ultimo_mov=mov_LAN)

    def finalizar(self, resultado: str) -> None:
        """
        Sube definitivamente la información a un nuevo archivo .json sin el _temp. Ademas, actualiza los CSV y lo inserta
        en la base de datos.

        Parametros:
        -----------
        resultado : str
            Resultado de la partida
        """
        self.resultado = resultado
        duracion = int((datetime.utcnow() - self.inicio).total_seconds())

        self._guardar_json(True)

        finalize_to_csv(self.game_id, self.resultado)

        movimientos = [(i + 1, lan, fen) for i, (lan, fen) in enumerate(self.jugadas)]

        añadir_partida_y_movimientos(self.blancas_id, self.negras_id, self.resultado, duracion, movimientos)

    def _guardar_json(self, final : bool = False) -> None:
        """
        Guarda la información en un archivo json. Si se ha terminado se añade el tiempo que ha tardado

        Parametros:
        -----------
        final : bool
            Valor booleano que marca si se ha terminado la partida
        """
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
        """
        Transforma toda la información que contiene al formato pgn

        Retorna:
        -------
        str
            Retorna la información en formato pgn
        """
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

    def json_a_pgn(self, archivo : str) -> None:
        """
        Transfomra un archivo .json a pgn

        Parametros:
        -----------
        archivo : str
            Nombre del archivo
        """

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