import pandas as pd
import os
from datetime import datetime

DIR_DATOS = "Base_de_datos/datos/"

# Carga el CSV en memoria
def load_en_curso() -> pd.DataFrame:
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

def save_en_curso(df: pd.DataFrame):
    os.makedirs(DIR_DATOS, exist_ok=True)
    df.to_csv(f'{DIR_DATOS}/en_curso.csv', index=False)

def upsert_en_curso(game_id: str, blancas : str, negras : str, fen : str, turno : int, ultimo_mov : str):
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

def finalize_to_csv(game_id : str, resultado : str):
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
    # Y eliminar de en_curso
    df = df[df["game_id"].astype(str)!=game_id]
    save_en_curso(df)
