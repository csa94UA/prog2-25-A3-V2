import sqlite3
from Base_de_datos.operaciones_sqlite import insertar_usuario
import hashlib
import os

DIR_DATOS = "./Base_de_datos/datos"

def inicializar_bd():
    os.makedirs(DIR_DATOS, exist_ok=True)

    crear_tabla_usuarios()
    crear_tabla_partidas()
    crear_tabla_movimientos()
    crear_tabla_estadisticas()

    insertar_usuario("Julio","julio.srp@gmail.com",hashlib.sha256("123".encode()).hexdigest(), "España")
    insertar_usuario("Jorge", "susybaka@gmail.com", hashlib.sha256("69".encode()).hexdigest(), "Cataluña")

def crear_tabla_usuarios():
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            nombre TEXT PRIMARY KEY,
            correo TEXT NOT NULL,
            contraseña TEXT NOT NULL,
            elo INTEGER DEFAULT 300,
            pais TEXT
        )
    ''')
    conn.commit()
    conn.close()

def crear_tabla_partidas():
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS partidas (
            nombre_partida TEXT PRIMARY KEY,
            jugador_blanco TEXT NOT NULL,
            jugador_negro TEXT NOT NULL,
            resultado TEXT,
            duracion INTEGER,
            FOREIGN KEY(jugador_blanco) REFERENCES usuarios(nombre) ON DELETE CASCADE,
            FOREIGN KEY(jugador_negro) REFERENCES usuarios(nombre) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

def crear_tabla_movimientos():
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partida_id TEXT NOT NULL,
            numero_jugada INTEGER,
            movimiento_LAN TEXT,
            fen TEXT,
            FOREIGN KEY(partida_id) REFERENCES partidas(nombre_partida) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

def crear_tabla_estadisticas():
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estadisticas (
            usuario_id INTEGER PRIMARY KEY,
            victorias INTEGER DEFAULT 0,
            derrotas INTEGER DEFAULT 0,
            tablas INTEGER DEFAULT 0,
            mejores_aperturas TEXT,
            peor_apertura TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()