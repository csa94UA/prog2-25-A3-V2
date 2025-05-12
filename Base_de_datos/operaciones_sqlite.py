import sqlite3

DIR_DATOS = "Base_de_datos/datos/"

def insertar_usuario(nombre, correo, contraseña_hash, pais, /, elo = 300):
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
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

def modificar_usuario(nombre, campo, nuevo_valor):
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        UPDATE usuarios
        SET {campo} = ?
        WHERE nombre = ?
    ''', (nuevo_valor, nombre))
    conn.commit()
    conn.close()
    print(f"Usuario '{nombre}' actualizado: {campo} = {nuevo_valor}")

def buscar_usuario(nombre):
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nombre = ?', (nombre,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def eliminar_usuario(nombre):
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE nombre = ?', (nombre,))
    conn.commit()
    conn.close()
    print(f"Usuario '{nombre}' eliminado.")

def insert_partida_and_moves(blancas_id, negras_id, resultado, duracion, moves_list):
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    c = conn.cursor()
    c.execute('''
      INSERT INTO partidas (jugador_blanco, jugador_negro, resultado, duracion)
      VALUES (?, ?, ?, ?)
    ''', (blancas_id, negras_id, resultado, duracion))
    partida_id = c.lastrowid

    for num, lan, fen in moves_list:
        c.execute('''
          INSERT INTO movimientos (partida_id, numero_jugada, movimiento_LAN, fen)
          VALUES (?, ?, ?, ?, ?)
        ''', (partida_id, num, lan, fen))

    conn.commit()
    conn.close()

def get_partidas_usuario(usuario_id):
    conn = sqlite3.connect(f'{DIR_DATOS}/DB.db')
    c = conn.cursor()
    c.execute('''
      SELECT * FROM partidas
      WHERE jugador_blanco=? OR jugador_negro=?
    ''', (usuario_id, usuario_id))
    partidas = c.fetchall()
    conn.close()
    return partidas