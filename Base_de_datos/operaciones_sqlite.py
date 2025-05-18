"""
Módulo dedicado a la ejecución de diversos comandos sqlite

Proporciona funciones para almacenar, modificar o eliminar informacion de la base de datos de sqlite

funciones:
    - insertar_usuario(nombre : str, correo : str, contraseña_hash : str, pais : str, /, elo : int)
    Registra un nuevo usuario a la base de datos. No pueden existir más de una persona con el mismo nombre

    - modificar_usuario(nombre : str, campo : str, valor : str)
    Modificar algun valor del perfil del usuario. No puede modificar su nombre

    - buscar_usuario(nombre : str)
    Busca al usuario en la base de datos y devuelve toda su informacion

    - obtener_datos_usuario(nombre : str)
    Busca al usuario en la base de datos y devuelve todo exceptuando su contraseña

    - elminar_usuario(nombre : str)
    Elimina el usuario del mismo nombre en la base de datos

    - añadir_partida_y_movimientos(blancas_id : str, negras_id : str, resultado : str, duracion : int, lista_mov : list[int,str,str])
    Añade los movimientos y la información de la partida

    - obtener_partida_usuario(game_id : str)
    Busca la partida con ese id

    - obtener_lista_partidas_usuario(nombre : str)
    Busca todas las partidas del usuario

    - obtener_datos_partida(game_id : str)
    Busca todos los movimientos / situaciones de esa partida

    - crear_partida_en_bd(jugador_blanco : str, jugador_negro : str)
    Inicializa una nueva partida

    - eliminar_partida_en_bd(nombre : str, game_id : str)
    Elimina la partida de la base de datos
"""
import sqlite3
import json

DIR_DATOS = "Base_de_datos/datos/"
DIR_JSON = 'Base_de_datos/datos/archivos_json'

def insertar_usuario(nombre : str, correo : str, contraseña_hash : str, pais : str, /, elo : int = 300) -> None:
    """
    Función encargada de registrar un nuevo usuario dentro de la base de datos.

    Parametros:
    ------------
    nombre : str
        Nombre del usuario

    correo : str
        Correo del usuario

    contraseña_hash : str
        Contraseña del usuario encriptada para mayor seguridad

    pais : str
        Pais en donde reside el usuario

    elo : int
        Elo (o nivel) del jugador. De manera predeterminada su valor es 300
    """
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO usuarios (nombre, correo, contraseña, elo, pais)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, correo, contraseña_hash, elo, pais))
        conn.commit()
        print("Usuario registrado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: nombre de usuario ya registrado.")
    conn.close()

    return None

def modificar_usuario(nombre : str, campo : str, valor : str) -> None:
    """
    Función encargada de modificar algun dato del usuario

    Parametros:
    ------------
    nombre : str
        Nombre del usuario

    campo : str
        Campo que se desea modificar

    valor : str
        Nuevo valor del campo
    """
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()
    cursor.execute(f'''
        UPDATE usuarios
        SET {campo} = ?
        WHERE nombre = ?
    ''', (valor, nombre))
    conn.commit()
    conn.close()

    return None

def buscar_usuario(nombre : str) -> dict:
    """
    Función encargada de buscar el usuario y devolver TODOS sus datos

    Parametros:
    ------------
    nombre : str
        Nombre del usuario

    Retorna:
    --------
    dict
        Devuelve todos los datos del usuario en forma de diccionario
    """
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nombre = ?', (nombre,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def obtener_datos_usuario(nombre : str) -> dict:
    """
    Función encargada de obtener los datos del usuario (exceptuando su contraseña)

    Parametros:
    ------------
    nombre : str
        Nombre del usuario

    Retorna:
    --------
    dict
        Devuelve los datos del usuario en forma de diccionario
    """
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, correo, elo, pais FROM usuarios WHERE nombre=?', (nombre,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def eliminar_usuario(nombre : str) -> None:
    """
    Función encargada de eliminar el perfil del usuario

    Parametros:
    ------------
    nombre : str
        Nombre del usuario
    """
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE nombre = ?', (nombre,))
    conn.commit()
    conn.close()

def añadir_partida_y_movimientos(blancas_id : str, negras_id : str, resultado : str, duracion : int, lista_mov : list[int,str,str]) -> None:
    """
    Función encargada de guardar una partida finalizada en las tablas correspondientes de la base de datos

    Parametros:
    ------------
    blancas_id : str
        Nombre del jugador blanco

    negras_id : str
        Nombre del jugador negro

    resultado : str
        Resultado de la partida

    duracion : int
        Duración de la partida en segundos

    lista_mov : list[int,str,str]
        Lista de movimientos LAN y su resultado en FEN
    """
    nombre_partida = f'{blancas_id}vs{negras_id}'
    eliminar_partida_en_bd(blancas_id, nombre_partida)
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    c = conn.cursor()
    c.execute('''
      UPDATE partidas SET jugador_blanco=?, jugador_negro=?, resultado=?, duracion=?
      WHERE nombre_partida = ?
    ''', (blancas_id, negras_id, resultado, duracion, nombre_partida))

    for num, lan, fen in lista_mov:
        c.execute('''
          INSERT INTO movimientos (partida_id, numero_jugada, movimiento_LAN, fen)
          VALUES (?, ?, ?, ?)
        ''', (nombre_partida, num, lan, fen))

    conn.commit()
    conn.close()

    return None

def obtener_partida_usuario(game_id : str) -> dict:
    """
    Funcion encargada de devolvar una partida concreta al usuario

    Parametros:
    ----------
    game_id : str
        Id del juego

    Retorna:
    --------
    dict
        Retorna un diccionario de la partida con toda su informacion (excepto los movimientos)
    """
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
      SELECT p.jugador_blanco, p.jugador_negro, p.resultado, p.duracion, p.nombre_partida,
       ub.nombre as nombre_blanco, un.nombre AS nombre_negro FROM partidas p
       JOIN usuarios ub ON p.jugador_blanco == ub.nombre
       JOIN usuarios un ON p.jugador_negro == un.nombre
      WHERE p.nombre_partida = ?
    ''', (game_id,))
    partidas = c.fetchone()
    conn.close()
    return partidas

def obtener_lista_partidas_usuario(nombre : str) -> list[dict]:
    """
    Funcion encargada de devolvar todas las partidas que tiene el jugador (terminadas o no)

    Parametros:
    ----------
    nombre : str
        Nombre del usuario

    Retorna:
    --------
    list[dict]
        Retorna una lista de partidas con toda su información (excepto los movimientos)
    """
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
          SELECT p.jugador_blanco, p.jugador_negro, p.resultado, p.duracion, p.nombre_partida
          FROM partidas p
          WHERE p.jugador_blanco=? or p.jugador_negro=?
        ''', (nombre,nombre))
    partidas = c.fetchall()
    conn.close()
    return partidas

def obtener_datos_partida(game_id : str) -> list[dict]:
    """
    Funcion encargada de devolver todas los movimientos de la partida

    Parametros:
    -----------
    game_id : str
        Id del juego

    Retorna:
    --------
    list[dict]
        Devuelve una lista de diccionarios con cada movimiento y situación del tablero en cada turno
    """
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
      SELECT numero_jugada, movimiento_LAN AS lan, fen FROM movimientos
      WHERE partida_id = ?
      ORDER BY numero_jugada ASC
    ''', (game_id,))
    movimientos = [{'lan': lan, 'fen': fen} for _,lan,fen in c.fetchall()]

    c.close()
    return movimientos

def crear_partida_en_bd(jugador_blanco : str, jugador_negro : str) -> None:
    """
    Funcion que inicializa una partida nueva en la base de datos

    Parametros:
    ----------
    jugador_blanco : str
        Nombre del jugador blanco

    jugador_negro : str
        Nombre del jugador negro
    """
    try:
        conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()
        c.execute('''
           INSERT INTO partidas (jugador_blanco, jugador_negro, resultado, duracion, nombre_partida)
           VALUES (?, ?, ?, ?, ?)
        ''', (jugador_blanco, jugador_negro, 'x-x', 0, f'{jugador_blanco}vs{jugador_negro}'))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Ya existe la partida")
    conn.close()

    return None

def eliminar_partida_en_bd(nombre : str, game_id : str) -> None:
    """
    Funcion que elimina una partida de la base de datos

    Parametros:
    -----------
    nombre : str
        Nombre del usuario

    game_id : int
        Id del juego
    """
    try:
        print(nombre)
        print(game_id)
        conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()
        c.execute('''
           DELETE FROM movimientos WHERE partida_id=?
        ''', (game_id,))
        print(obtener_datos_partida(game_id))
        c.execute('''
           DELETE FROM partidas WHERE nombre_partida=? and (jugador_blanco=? or jugador_negro=?)
        ''', (game_id, nombre, nombre))
        conn.commit()
    except sqlite3.IntegrityError:
        print("No existe dicha partida")
    conn.close()

    return None

if __name__ == '__main__':
    datos = buscar_usuario("Julio")
    print(datos.keys())
    partidas = obtener_lista_partidas_usuario("Julio")
    print(partidas)
    print(len(partidas))
    print(partidas[0]['nombre_partida'])
    for i,partida in enumerate(partidas):
        print(f"{i + 1}. Partida: {partida['nombre_partida']}")
        print(partida.keys())
        print("jugador_blanco: ",partida['jugador_blanco'])
        print('Jugador_negro: ',partida['jugador_negro'])
        print('Duracion: ', partida['duracion'])
        print('Nombre partida: ', partida['nombre_partida'])
    movimiento = obtener_datos_partida("JuliovsJorge")
    print(movimiento)
    partida = obtener_partida_usuario("JuliovsJorge")
    datos: dict = {
        'jugador_blanco': partida['jugador_blanco'],
        'jugador_negro': partida['jugador_negro'],
        'duracion': partida['duracion'],
        'resultado': partida['resultado'],
        'movimientos': movimiento
    }
    with open(f'{DIR_JSON}/{partida['nombre_partida']}.json', 'w') as escritura:
        json.dump(datos, escritura, indent=4)
    #eliminar_partida("Julio","JuliovsJulio")