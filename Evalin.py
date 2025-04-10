import subprocess
from typing import Dict, Union, Literal, Optional

# Define un tipo para la evaluación, que puede ser de centipawns o mate
EvaluationType = Dict[
    Literal["Tipo", "Ventaja en Centipawns", "Mate en"],
    Union[str, int, None]
]


def evaluate_position(fen: str, engine_path: str = "./stockeje", depth: int = 15) -> EvaluationType:
    """Evalúa una posición de ajedrez usando un motor de ajedrez UCI.

    Args:
        fen: Cadena FEN que describe la posición del tablero
        engine_path: Ruta al ejecutable del motor de ajedrez
        depth: Profundidad de análisis en movimientos

    Returns:
        Diccionario con el tipo de evaluación (centipawns o mate) y su valor
    """
    # Inicia el proceso del motor de ajedrez
    engine = subprocess.Popen(
        engine_path,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1
    )

    # Envía comandos UCI al motor para evaluar la posición
    engine.stdin.write(f"uci\nisready\nposition fen {fen}\ngo depth {depth}\n")
    engine.stdin.flush()

    # Diccionario para almacenar el resultado de la evaluación
    evaluation: EvaluationType = {"Tipo": None, "Ventaja en Centipawns": None, "Mate en": None}

    # Lee la salida del motor línea por línea
    while True:
        line = engine.stdout.readline().strip()

        # Si la línea contiene evaluación de centipawns
        if "score cp" in line:
            evaluation = {
                "Tipo": "Centipawns",
                "Ventaja en Centipawns": int(line.split("score cp")[1].split()[0]),
                "Mate en": None
            }

        # Si la línea contiene evaluación de mate
        elif "score mate" in line:
            evaluation = {
                "Tipo": "Mate",
                "Ventaja en Centipawns": None,
                "Mate en": int(line.split("score mate")[1].split()[0])
            }

        # Cuando encuentra el mejor movimiento, termina el proceso
        elif line.startswith("bestmove"):
            engine.stdin.write("quit\n")
            engine.stdin.flush()
            engine.terminate()
            return evaluation