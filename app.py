import random
import requests

TOKEN_API = "AQUIVAMITOKENEPICO"
HEADERS = {"Authorization": f"Bearer {TOKEN_API}"}
BASE = "https://lichess.org/api"

def movimiento_ia(fen : str) -> tuple[str, int] | str:
    parametros = {
        "fen": fen,
        "multiPv": 3
    }
    print(f'{BASE}/cloud-eval?fen={fen}&multiPv=3')
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

def descargar_partida_en_json(game_id : str) -> dict:
    parametros = {
        "moves": "true",
        "pgnInJson": "true"
    }

    r = requests.get(f'{BASE}/game/export/{game_id}', headers=HEADERS, params=parametros)
    r.raise_for_status()
    return r.json()

def formar_estudio(nombre : str) -> str:
    datos = {
        "name": nombre,
        "visibility": "private"
    }

    r = requests.post(f"{BASE}/study", headers=HEADERS, data=datos)
    r.raise_for_status()
    return r.json()["id"]