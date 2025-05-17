"""
Módulo dedicado a la ejecución de diversos comandos de la librería pandas. Se utiliza como intermidiario entre base de datos,
archivos .json y las partidas. Almacenan alguna información util en .csv

Proporciona funciones para almacenar y eliminar información de los .csv

funciones:
    - load_en_curso() -> pd.DataFrame
    Inicializa el archivo en_curso.csv si no existe. En caso contrario devuelve dicho archivo

    - save_en_curso(df: pd.DataFrame) -> None
    Guarda solo la última situación de la partida en el achivo en_curso.csv en la fila correspondiente

    - upsert_en_curso(game_id: str, blancas : str, negras : str, fen : str, turno : int, ultimo_mov : str) -> None
    Crea un nuevo dataframe con la información de la última situación de la partida que más tarde se guardará en un CSV

    - finalize_to_csv(game_id : str, resultado : str) -> None
    Guarda el último estado de la partida ya terminada en un nuevo archvo CSV y elimina la información que habia de dicha
    partida en el archivo en_curso.csv
"""
import pandas as pd
import os
from datetime import datetime

DIR_DATOS = "Base_de_datos/datos/"

def load_en_curso() -> pd.DataFrame:
    """
    Funcion encargada de cargar el archivo csv en_curso en caso de existir. Si no lo crea desde cero.

    Retorna:
    -------
    pd.DataFrame
        Retorna el dataframe con toda la información del archivo en_curso.csv
    """
    try:
        en_curso = pd.read_csv(f'{DIR_DATOS}/en_curso.csv')
    except FileNotFoundError:
        en_curso = pd.DataFrame(columns=[
            'game_id','jugador_blanco','jugador_negro','fen','turno','ultimo_mov'
        ])
    finally:
        en_curso = en_curso.astype({
            "game_id": str,
            'jugador_blanco': str,
            'jugador_negro': str,
            "fen": str,
            "turno": int,
            "ultimo_mov": str
        })
        return en_curso

def save_en_curso(df : pd.DataFrame) -> None:
    """
    Funcion que guarda el estado del dataframe al archivo en_curso.csv o historico.csv

    Parametros:
    ----------
    df : pd.DataFrame
        DataFrame con toda la información del anterior archivo csv y la nueva informacion
    """
    os.makedirs(DIR_DATOS, exist_ok=True)
    df.to_csv(f'{DIR_DATOS}/en_curso.csv', index=False)

def upsert_en_curso(game_id: str, blancas : str, negras : str, fen : str, turno : int, ultimo_mov : str) -> None:
    """
    Funcion que guarda el último estado de la partida en el dataframe que mas tarde será guardado en un archivo CSV

    Parametros:
    ----------
    game_id : str
        Nombre de la partida

    blancas : str
        Nombre del jugador blanco

    negras : str
        Nombre del jugador negro

    fen : str
        Formato FEN del tablero

    turno : int
        Turno de la partida

    ultimo_mov : str
        Ultimo movimiento en fomrato LAN hipersimplificado
    """
    df = load_en_curso()
    if game_id in df["game_id"].astype(str).values:
        mascara = df["game_id"].astype(str) == game_id
        df.loc[mascara, "fen"] = fen
        df.loc[mascara, "turno"] = turno
        df.loc[mascara, "ultimo_mov"] = ultimo_mov
    else:
        df = pd.concat([df, pd.DataFrame([{"game_id": game_id, "jugador_blanco": blancas, "jugador_negro": negras, "fen": fen,
            "turno": turno, "ultimo_mov": ultimo_mov}])], ignore_index=True)
    save_en_curso(df)

def finalize_to_csv(game_id : str, resultado : str) -> None:
    """
    Funcion que guarda el estado último de la partida ya terminada y lo almacena en historico.csv

    Parametros:
    ----------
    game_id : str
        Nombre del juego

    resultado : str
        Resultado de la partida
    """
    df = load_en_curso()
    row = df[df["game_id"].astype(str)==game_id]

    if row.empty:
        return

    row = row.assign(resultado=resultado, fin=datetime.utcnow().isoformat())

    try:
        hist = pd.read_csv(f'{DIR_DATOS}/historico.csv')
    except FileNotFoundError:
        hist = pd.DataFrame()
    hist = pd.concat([hist, row], ignore_index=True)
    hist.to_csv(f'{DIR_DATOS}/historico.csv', index=False)

    df = df[df["game_id"].astype(str)!=game_id]
    save_en_curso(df)
