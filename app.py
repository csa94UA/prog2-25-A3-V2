import requests

TOKEN_API = "AQUIVAMITOKENEPICO"
HEADERS = {"Authorization": f"Bearer {TOKEN_API}"}
BASE = "https://lichess.org/api"

def movimiento_ia(fen : str) -> tuple[str, int] | str:
    parametros = {
        "fen": fen,
        "multiPv": 1
    }
    r = requests.get(f"{BASE}/cloud-eval", headers=HEADERS, params=parametros)
    r.raise_for_status()
    data = r.json()

    if "pvs" in data and data["pvs"]:
        return data["pvs"][0]["moves"].split()[0]
    else:
        return "No se pudo obtener jugada de la IA.", 500

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