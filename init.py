"""
Modulo encargado de inicializar todas las tablas de la base de datos en caso de no existir. También se incluyen algunos
datos ya digitados para probar.

Funcoines:
    - inicializar_bd()
    Inicializa la base de datos con todas las tablas

    - crear_tabla_usuarios()
    Inicializa la tabla Usuarios

    - crear_tabla_partidas()
    Inicializa la tabla Partidas

    - crear_tabla_movimientos()
    Inicializa la tabla movimientos
"""

import sqlite3
from Base_de_datos.operaciones_sqlite import insertar_usuario
import hashlib
import os

DIR_DATOS = "./Base_de_datos/datos"

def inicializar_bd() -> None:
    """
    Funcion encargada de inicializar la base de datos en caso de no existir.
    """
    os.makedirs(DIR_DATOS, exist_ok=True)

    crear_tabla_usuarios()
    crear_tabla_partidas()
    crear_tabla_movimientos()

    insertar_usuario("Julio","julio.srp@gmail.com",hashlib.sha256("123".encode()).hexdigest(), "España")
    insertar_usuario("Jorge", "susybaka@gmail.com", hashlib.sha256("69".encode()).hexdigest(), "Cataluña")

    return None

def crear_tabla_usuarios() -> None:
    """
    Función encargada de inicializar la tabla Usuarios.
    """
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

    return None

def crear_tabla_partidas() -> None:
    """
    Función encargada de inicializar la tabla Partidas.
    """
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

    return None

def crear_tabla_movimientos() -> None:
    """
    Función encargada de inicializar la tabla Movimientos.
    """
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

    return None