import subprocess


def get_best_move(fen, engine_path="./stockeje", depth=15):
    """
    Obtiene el mejor movimiento para una posición FEN usando Stockfish.

    Args:
        fen (str): Posición en formato FEN.
        engine_path (str): Ruta al ejecutable de Stockfish.
        depth (int): Profundidad de análisis (default: 15).

    Returns:
        str: Mejor movimiento en formato UCI (e.g., "e2e4"), o None si hay error.
    """
    try:
        engine = subprocess.Popen(
            engine_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )

        # Configuración inicial
        engine.stdin.write("uci\n")
        engine.stdin.write("isready\n")
        engine.stdin.flush()

        # Esperar "readyok"
        while True:
            if "readyok" in engine.stdout.readline():
                break

        # Analizar posición
        engine.stdin.write(f"position fen {fen}\n")
        engine.stdin.write(f"go depth {depth}\n")
        engine.stdin.flush()

        # Capturar "bestmove"
        while True:
            line = engine.stdout.readline().strip()
            if line.startswith("bestmove"):
                move = line.split()[1]
                return move if move != "(none)" else None

    except Exception as e:
        print(f"Error en get_best_move: {e}")
        return None
    finally:
        if 'engine' in locals():
            engine.stdin.write("quit\n")
            engine.stdin.flush()
            engine.terminate()