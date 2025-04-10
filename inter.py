import subprocess

STOCKFISH_EXECUTABLE = "./stockej"  # Asegúrate de que la ruta sea correcta

def obtener_mejor_movimiento(fen):
    """
    Envia una posición FEN a Stockfish y devuelve el mejor movimiento.
    Devuelve None si no se puede obtener el movimiento.
    """
    try:
        proceso = subprocess.Popen(
            [STOCKFISH_EXECUTABLE],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        proceso.stdin.write("uci\n")
        proceso.stdin.flush()
        # Leer hasta que Stockfish esté listo (envía "readyok")
        while True:
            linea = proceso.stdout.readline().strip()
            if linea == "readyok":
                break

        proceso.stdin.write("ucinewgame\n")
        proceso.stdin.flush()
        proceso.stdin.write(f"position fen {fen}\n")
        proceso.stdin.flush()
        proceso.stdin.write("go depth 10\n")  # Puedes ajustar la profundidad
        proceso.stdin.flush()

        mejor_movimiento = None
        while True:
            linea = proceso.stdout.readline().strip()
            if linea.startswith("bestmove"):
                mejor_movimiento = linea.split()[1]
                break
            elif not linea:
                break  # Fin de la salida

        proceso.stdin.write("quit\n")
        proceso.stdin.flush()
        proceso.wait()
        return mejor_movimiento

    except FileNotFoundError:
        print(f"Error: No se encontró el ejecutable de Stockfish en: {STOCKFISH_EXECUTABLE}")
        return None
    except Exception as e:
        print(f"Ocurrió un error al interactuar con Stockfish: {e}")
        return None

if __name__ == "__main__":
    posiciones_fen = [
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",  # Posición inicial
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",  # Después de 1. e4
        "rnbqkbnr/pppppppp/8/8/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2",  # Después de 1. e4 Nf3
        "4k3/8/8/8/8/8/8/4K3 w - - 0 1",  # Rey blanco y negro solos
    ]

    for fen in posiciones_fen:
        mejor_movimiento = obtener_mejor_movimiento(fen)
        if mejor_movimiento:
            print(f"Para la posición FEN: {fen}")
            print(f"Stockfish recomienda el mejor movimiento: {mejor_movimiento}\n")
        else:
            print(f"No se pudo obtener el mejor movimiento para la posición FEN: {fen}\n")