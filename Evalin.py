import subprocess

def evaluate_position(fen, engine_path="./stockeje", depth=15):
    engine = subprocess.Popen(
        engine_path,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1
    )
    engine.stdin.write(f"uci\nisready\nposition fen {fen}\ngo depth {depth}\n")
    engine.stdin.flush()

    evaluation = {"type": None, "value": None}
    while True:
        line = engine.stdout.readline().strip()
        if "score cp" in line:
            evaluation = {"Tipo": "Centipawns", "Ventaja en Centipawns": int(line.split("score cp")[1].split()[0])}
        elif "score mate" in line:
            evaluation = {"Tipo": "Mate", "Mate en": int(line.split("score mate")[1].split()[0])}
        elif line.startswith("bestmove"):
            engine.stdin.write("quit\n")
            engine.stdin.flush()
            engine.terminate()
            return evaluation
