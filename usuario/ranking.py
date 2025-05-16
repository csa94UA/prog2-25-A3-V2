import os
import json
from typing import List, Dict, Optional

from config import PATH_USUARIOS  # Usamos la ruta configurada centralmente

def obtener_ranking(top_n: int = 10) -> List[Dict[str, any]]:
    """
    Devuelve una lista con los top N usuarios ordenados por ELO (descendente).

    Parámetros:
    -----------
    top_n : int
        Número de usuarios a devolver en el ranking.

    Retorna:
    --------
    List[Dict[str, any]]
        Lista de usuarios con campos: username, user_id y elo.
    """
    usuarios: List[Dict[str, any]] = []

    for archivo in os.listdir(PATH_USUARIOS):
        if archivo.endswith(".json"):
            ruta: str = os.path.join(PATH_USUARIOS, archivo)
            with open(ruta, "r", encoding="utf-8") as f:
                datos: Dict[str, any] = json.load(f)
                usuarios.append({
                    "username": datos["username"],
                    "user_id": datos["user_id"],
                    "elo": datos.get("elo", 1000)
                })

    # Ordenamos por ELO de forma descendente
    usuarios.sort(key=lambda u: u["elo"], reverse=True)
    return usuarios[:top_n]


def obtener_posicion_usuario(username: str) -> Optional[int]:
    """
    Devuelve la posición (1-indexada) del usuario en el ranking global por ELO.

    Parámetros:
    -----------
    username : str
        Nombre de usuario cuya posición se desea conocer.

    Retorna:
    --------
    Optional[int]
        Posición del usuario (empezando desde 1) o None si no se encuentra.
    """
    usuarios: List[Dict[str, any]] = []

    for archivo in os.listdir(PATH_USUARIOS):
        if archivo.endswith(".json"):
            ruta: str = os.path.join(PATH_USUARIOS, archivo)
            with open(ruta, "r", encoding="utf-8") as f:
                datos: Dict[str, any] = json.load(f)
                usuarios.append({
                    "username": datos["username"],
                    "user_id": datos["user_id"],
                    "elo": datos.get("elo", 1200)
                })

    # Ordenamos por ELO
    usuarios.sort(key=lambda u: u["elo"], reverse=True)

    # Buscamos la posición (indexada desde 1)
    for idx, usuario in enumerate(usuarios, start=1):
        if usuario["username"] == username:
            return idx

    return None
