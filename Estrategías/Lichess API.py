# Carlos Salas Alarcón - TABLEBASES

# ~ Librerias
import requests
from urllib.parse import quote
from diskcache import Cache
import chess

cache = Cache("tablebase_cache")


def query_tablebase(fen: str) -> str:
    if fen in cache:
        return cache[fen]

    encoded_fen = quote(fen)
    url = f"https://tablebase.lichess.ovh/standard?fen={encoded_fen}"

    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()
        cache[fen] = data

        winning_moves = [m for m in data.get("moves", []) if m.get("category") == "win"]
        if winning_moves:
            return min(winning_moves, key=lambda x: x.get("dtz", float("inf")))['uci']

        drawing_moves = [m for m in data.get("moves", []) if m.get("category") == "draw"]
        return drawing_moves[0]['uci'] if drawing_moves else ''

    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"Error: {e}")
        return ''


def simulate(initial_fen=None):
    board = chess.Board()

    if initial_fen:
        try:
            board.set_fen(initial_fen)
            sanitized_fen = board.fen()
        except ValueError:
            board = chess.Board()

    while not board.is_game_over():
        print("\nPosition:\n", board)

        if board.turn == chess.WHITE:
            while True:
                try:
                    move = chess.Move.from_uci(input("Your move (UCI): "))
                    if move in board.legal_moves:
                        board.push(move)
                        break
                except ValueError:
                    continue
        else:
            current_fen = board.fen()
            best_move = query_tablebase(current_fen)
            if best_move:
                board.push(chess.Move.from_uci(best_move))
                print(f"Bot plays: {best_move}")

    print("\nResult:", board.result())


if __name__ == "__main__":
    initial_fen = input("Initial FEN (Enter for default): ").strip()
    simulate(initial_fen if initial_fen else None)