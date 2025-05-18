import pandas as pd
import os

# Ruta de los CSV
DATA_DIR = os.path.join(os.path.dirname(__file__), "datos")
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------------
# Funciones de creación
# ---------------------------

def crear_tabla_usuarios():
    return pd.DataFrame([
        {"id": 1, "nombre": "Julio", "correo": "julio@gmail.com", "elo": 1500, "pais": "España"},
        {"id": 2, "nombre": "Jorge", "correo": "jorge@gmail.com", "elo": 1200, "pais": "España"}
    ])

def crear_tabla_partidas_finalizadas():
    return pd.DataFrame([
        {"id": 1, "jugador_blanco": 1, "jugador_negro": 2, "resultado": "1-0", "duracion": 3600},
        {"id": 2, "jugador_blanco": 2, "jugador_negro": 1, "resultado": "½-½", "duracion": 1800}
    ])

def crear_tabla_partidas_sin_terminar():
    return pd.DataFrame([
        {"id": 1, "partida_id": 1, "numero_jugada": 1, "movimiento_LAN": "Pe2-e4", "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1", "centipawns": 20},
        {"id": 2, "partida_id": 1, "numero_jugada": 2, "movimiento_LAN": "Pe7-e5", "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2", "centipawns": 10},
        {"id": 3, "partida_id": 1, "numero_jugada": 3, "movimiento_LAN": "Ng1-f3", "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2", "centipawns": 30}
    ])

# ---------------------------
# Función para guardar CSVs
# ---------------------------

def guardar_tablas(datos: "DataFrame", nombre : str) -> None:
    datos.to_csv(os.path.join(DATA_DIR, f"{nombre}.csv"))
    return None

# ---------------------------
# Función para cargar CSVs si existen
# ---------------------------

def cargar_tablas():
    tablas = {}
    for nombre in ["usuarios", "partidas_finalizadas", "partidas_sin_acabar"]:
        ruta = os.path.join(DATA_DIR, f"{nombre}.csv")
        if os.path.exists(ruta):
            tablas[nombre] = pd.read_csv(ruta)
            print(f"📥 Cargado desde archivo: {nombre}.csv")
        else:
            print(f"⚠️ No se encontró {nombre}.csv, se usará tabla vacía o generada.")
    return tablas

def cargar_usuarios() -> pd.DataFrame:
    if os.path.exists(f"{DATA_DIR}/usuarios.csv"):
        return pd.read_csv(f"{DATA_DIR}/usuarios.csv")
    # Creamos un DataFrame vacío con las columnas esperadas
    return pd.DataFrame(columns=["id", "nombre", "email", "hash", "elo", "pais"])

def guardar_usuarios(df: pd.DataFrame) -> None:
    df.to_csv(f"{DATA_DIR}/usuarios.csv", index=False)

def cargar_partidas_finalizadas() -> pd.DataFrame:
    if os.path.exists(f"{DATA_DIR}/partidas_finalizadas.csv"):
        return pd.read_csv(f"{DATA_DIR}/partidas_finalizadas.csv")

    return pd.DataFrame(columns=["id","jugador_b","jugador_n","fen","victoria"])

def cargar_patidas_sin_finalizar() -> pd.DataFrame:
    if os.path.exists(f"{DATA_DIR}/partidas_sin_acabar.csv"):
        return pd.read_csv(f"{DATA_DIR}/partidas_sin_acabar.csv")

    return pd.DataFrame(columns=["id","jugador_b","jugador_n","fen"])

# ---------------------------
# Main
# ---------------------------

def main():
    # Cargar tablas si existen
    tablas = cargar_tablas()

    # Si alguna tabla no existe, la generamos
    tablas.setdefault("usuarios", crear_tabla_usuarios())
    tablas.setdefault("partidas_finalizadas", crear_tabla_partidas_finalizadas())
    tablas.setdefault("partidas_sin_acabar", crear_tabla_partidas_sin_terminar())

    # Vista previa
    for nombre, df in tablas.items():
        print(f"\n🔎 {nombre.capitalize()}:\n", df.head())

    # Guardar
    guardar_tablas(tablas)

if __name__ == "__main__":
    main()
