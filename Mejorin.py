import subprocess
from typing import Optional


def get_best_move(fen: str, engine_path: str = "./stockeje", depth: int = 15) -> Optional[str]:
    """Obtiene el mejor movimiento para una posición FEN usando un motor UCI (como Stockfish).

    Args:
        fen: Posición en formato FEN como cadena de texto.
        engine_path: Ruta al ejecutable del motor de ajedrez. Por defecto "./stockeje".
        depth: Profundidad de análisis en movimientos. Por defecto 15.

    Returns:
        El mejor movimiento en formato UCI (ej. "e2e4"), o None si hay error o no hay movimientos.
        Devuelve None también si el motor devuelve "(none)" como mejor movimiento.

    Raises:
        Captura y muestra cualquier excepción que ocurra durante el proceso, devolviendo None en esos casos.
    """
    engine: Optional[subprocess.Popen[str]] = None

    try:
        # Inicializar el proceso del motor de ajedrez
        engine = subprocess.Popen(
            engine_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )

        # Configuración inicial del protocolo UCI
        engine.stdin.write("uci\n")  # Iniciar protocolo UCI
        engine.stdin.write("isready\n")  # Verificar que el motor está listo
        engine.stdin.flush()

        # Esperar confirmación "readyok" del motor
        while True:
            line: str = engine.stdout.readline()
            if "readyok" in line:
                break

        # Enviar posición FEN y comando para analizar
        engine.stdin.write(f"position fen {fen}\n")  # Establecer posición
        engine.stdin.write(f"go depth {depth}\n")  # Iniciar análisis
        engine.stdin.flush()

        # Leer salida del motor hasta encontrar "bestmove"
        while True:
            line = engine.stdout.readline().strip()
            if line.startswith("bestmove"):
                move: str = line.split()[1]  # Extraer el movimiento UCI
                return move if move != "(none)" else None  # Manejar caso sin movimientos

    except Exception as e:
        print(f"Error en get_best_move: {e}")
        return None

    finally:
        # Asegurarse de cerrar el motor correctamente
        if engine is not None:
            engine.stdin.write("quit\n")
            engine.stdin.flush()
            engine.terminate()