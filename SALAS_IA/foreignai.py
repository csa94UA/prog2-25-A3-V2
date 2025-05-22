import subprocess


def get_best_move(fen):
    # Iniciar Stockfish
    process = subprocess.Popen(
        ["./stockeje"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True  # Para usar strings en vez de bytes
    )

    # Enviar comandos UCI
    commands = f"""
    uci
    position fen {fen}
    go movetime 2000
    quit
    """

    # Enviar comandos y recibir salida
    output, _ = process.communicate(commands)

    # Buscar "bestmove" en la salida
    for line in output.split("\n"):
        if "bestmove" in line:
            return line.split()[1]

    return None

