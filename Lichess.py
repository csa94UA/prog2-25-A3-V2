"""
Modulo que contiene solo una funcion de la api Lichess. Se busca comunicar con su servidao para usar sus bots.
La razón por la que no hay más funciones es debido a las grandes limitaciones y problemas que daba Lichess para poder
usar sus bots. Me decanté ha usar solo un ENDDPOINT que es el que más me interesaba

Funcion:
    - movimiento_ia(fen : str) -> tuple[str, int] | str
    Obtiene aleatorioamente uno de los cinco mejores movimientos valorados por la api
"""

import random
import requests

TOKEN_API = "AQUIVAMITOKENEPICO"
HEADERS = {"Authorization": f"Bearer {TOKEN_API}"}
BASE = "https://lichess.org/api"

def movimiento_ia(fen : str) -> str:
    """
    Función encargada de obtener los mejores movimientos en la situación del tablero.

    Parametros:
    -----------
    fen : str
        Estado del tablero en formato FEN

    Retorna:
    --------
    str
        Devuelve uno de los movimientos si todo funciona bien. En caso contrario muestra un mensaje de error y devuelve '404'
    """
    parametros = {
        "fen": fen,
        "multiPv": 5
    }
    try:
        r = requests.get(f"{BASE}/cloud-eval", headers=HEADERS, params=parametros)
        r.raise_for_status()
        data = r.json()

        movimientos = [entry["moves"].split()[0] for entry in data["pvs"]]

    except requests.RequestException:
        print("Problemas con movimiento IA Lichess: No se ha podido obtener su movimiento. Se procederá a consultar a StockFish")
        return '404'

    else:
        return random.choice(movimientos)