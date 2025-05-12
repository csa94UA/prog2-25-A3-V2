import sqlite3
from Base_de_datos.operaciones_sqlite import insertar_usuario
import hashlib

DIR_DATOS = "./Base_de_datos/datos"

def inicializar_bd():
    crear_tabla_usuarios()
    crear_tabla_partidas()
    crear_tabla_movimientos()
    crear_tabla_estadisticas()

    contraseña = '123'
    insertar_usuario("Julio","julio.srp@gmail.com", hashlib.sha256(contraseña.encode()).hexdigest(), "España")

def crear_tabla_usuarios():
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            correo TEXT NOT NULL,
            contraseña TEXT NOT NULL,
            elo INTEGER DEFAULT 1500,
            pais TEXT
        )
    ''')
    conn.commit()
    conn.close()

def crear_tabla_partidas():
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jugador_blanco INTEGER NOT NULL,
            jugador_negro INTEGER NOT NULL,
            resultado TEXT,
            duracion INTEGER,
            FOREIGN KEY(jugador_blanco) REFERENCES usuarios(id),
            FOREIGN KEY(jugador_negro) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    conn.close()

def crear_tabla_movimientos():
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partida_id INTEGER NOT NULL,
            numero_jugada INTEGER,
            movimiento_LAN TEXT,
            fen TEXT,
            FOREIGN KEY(partida_id) REFERENCES partidas(id)
        )
    ''')
    conn.commit()
    conn.close()

def crear_tabla_estadisticas():
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estadisticas (
            usuario_id INTEGER PRIMARY KEY,
            victorias INTEGER DEFAULT 0,
            derrotas INTEGER DEFAULT 0,
            tablas INTEGER DEFAULT 0,
            mejores_aperturas TEXT,
            peor_apertura TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    conn.close()

inicializar_bd()