"""
Modulo principal del proyecto encargado de encapsular todas las funciones de Flask y sus ENDPOINTS

En ella se perimte hacer las funciones básicas de manejo de usuarios (registro, inicio sesion, modificar datos, ver datos
y eliminar perfil). Además, se incluyen ENDPOINTS dedicados a la gestión de partidas como exportación de partidas a json,
inicializar partida en base de datos y más.

Funciones:
    - singup() -> tuple[str,int]
    Registra un nuevo usuario a la base de datos

    - login() -> tuple[str, int] | tuple[dict[str,Any], int]
    Inicia sesíon del usuario registrado en la base de datos

    - obtener_perfil() -> tuple[str,int] | tuple[dict,int]
    Retorna la información del usuario

    - modificar_perfil() -> tuple[str,int]
    Modifica los datos del usuario de la base de datos

    - eliminar_perfil() -> tuple[str,int]
    Elimina el perfil del usuario de la base de datos

    - obtener_partida_json() -> tuple[str,int]
    Exporta una partida concreta almacenada dentro de la base de datos a json para otras funciones

    - crear_partida() -> tuple[str,int]
    Inicializa en la base de datos una nueva partida

    - eliminar_partida() -> tuple[str,int]
    Elimina una partida concreta de la base de datos

    - obtener_partidas() -> tuple[str,int] | tuple[list[dict],int]
    Retorna un conjunto de partidas del usuario que están almacenadas en la base de datos
"""

import os
from typing import Any
from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import hashlib
from Base_de_datos.operaciones_sqlite import *
from init import inicializar_bd

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "ContraseñaSuperSecreta"
jwt = JWTManager(app)

users = {}
data = {}

@app.route('/signup', methods=['POST'])
def singup() -> tuple[str,int]:
    """
    Registra un nuevo usuario y lo inserta dentro de la base de datos.

    Obtiene los parametros 'users', 'password', 'email', y 'pais' desde los argumentos de la petición de request.args()
    Si no faltan datos y no existe otro usuario con el mismo nombre en la base de datos se registra dicho usuario y retorna
    el codigo 200. En caso contrario retornara un mensaje de error y su código de error

    Retorna:
    --------
    tuple[str,int]
        Devuelve el mensaje de estado y su código correspondiente
    """
    nombre = request.args.get('user')
    contraseña = request.args.get('password')
    correo = request.args.get('email')
    pais = request.args.get('pais')

    if not all([nombre, contraseña, correo, pais]):
        return "Faltan campos", 400

    hashed = hashlib.sha256(contraseña.encode()).hexdigest()
    try:
        insertar_usuario(nombre, correo, hashed, pais)
    except sqlite3.IntegrityError:
        return "Usuario ya existe", 409

    return f"Usuario {nombre} registrado", 200

@app.route('/login', methods=['GET'])
def login() -> tuple[str, int] | tuple[dict[str,Any], int]:
    """
    Inicia sesion el usuario y se devuelve su token JWT

    Obtiene los parametros 'users' y 'password' desde los argumentos de la petición de request.args() Si no faltan datos
    y resulta que digita su contraseña tras haberse registrardo devolvera el token JWT y su código de estoad 200.
    En caso contrario retornara un mensaje de error y su código de error

    Retorna:
    --------
    tuple[str, int] | tuple[dict[str,Any], int]
        Retorna el par (respuesta, codigo). Si todo va bien devuelve el toquen en forma de diccionario y su codigo de estado
        correspondiente
    """
    nombre = request.args.get('user', '')
    contraseña = request.args.get('password', '')
    hashed = hashlib.sha256(contraseña.encode()).hexdigest()

    if not all([nombre, contraseña]):
        return f"Faltan campos: nombre y/o contraseña",400

    datos = buscar_usuario(nombre)
    if datos and datos['contraseña'] == hashed:
        return {'access token': create_access_token(identity=nombre)}, 200

    return 'Credenciales invalidas', 401

@app.route('/perfil', methods=['GET'])
@jwt_required()
def obtener_perfil() -> tuple[str,int] | tuple[dict,int]:
    """
    Busca los datos del usuario

    Se obtiene el nombre del usuario con su token y se accede a sus datos almacenados dentro de la base de datos.

    Retorna:
    --------
    tuple[str,int] | tuple[dict,int]
        Devuelve un diccionario de los datos encontrados y su codigo de estado si lo encuentra en la base de datos. En
        caso contrario se devuelve el texto de error y su codigo correspondiente.
    """
    nombre = get_jwt_identity()
    datos = obtener_datos_usuario(nombre)
    if not datos:
        return 'No se ha encontrado al usuario', 404

    return dict(datos),200

@app.route('/perfil', methods=['PUT'])
@jwt_required()
def modificar_perfil() -> tuple[str,int]:
    """
    Modifica los datos del usuario (solo un campo a la vez)

    Se obtiene el nombre del usuario con su token y se obtienen los parametros 'campo' y 'valor' a traves de la petición
    de requests.args(). Seguidamente se modifica en el campo correspondiente y se añade el nuevo valor

    Retorna:
    --------
    tuple[str,int]
        Devuelve el par (respuesta,codigo).
    """
    nombre = get_jwt_identity()
    campo = request.args.get('campo', '')
    valor = request.args.get('valor', '')
    datos = buscar_usuario(nombre)

    if campo == 'contraseña':
        valor = hashlib.sha256(valor.encode()).hexdigest()

    if not campo in datos.keys():
        return 'Campo no encontrado', 401
    if valor in datos[campo]:
        return 'Valor repetido', 401

    modificar_usuario(nombre, campo, valor)

    return f"Usuario '{nombre}' actualizado: {campo} = {valor if campo != 'contraseña' else '********'}", 200

@app.route('/perfil', methods=['DELETE'])
@jwt_required()
def eliminar_perfil() -> tuple[str,int]:
    """
    Elimina al usuario de la base de datos

    Se obtiene el nombre del usuario con su token y se obtiene el parametro 'password' a traves de la petición
    de requests.args(). Seguidamente se elimina el perfil del usuario de la base de datos

    Retorna:
    --------
    tuple[str,int]
        Devuelve el par (respuesta,codigo).
    """
    nombre = get_jwt_identity()
    contraseña = request.args.get('password', '')
    hashed = hashlib.sha256(contraseña.encode()).hexdigest()
    datos = buscar_usuario(nombre)

    if hashed != datos['contraseña']:
        return 'La contraseña es incorrecta', 401

    eliminar_usuario(nombre)

    return 'Usuario eliminado con éxito', 200

@app.route('/partida/json', methods=['GET'])
@jwt_required()
def obtener_partida_json() -> tuple[str,int]:
    """
    Busca la partida elegida por el usuario lo devuelve en forma de diccionario.

    Se obtiene el nombre del usuario con su token y se obtiene el parametro 'id' a traves de la petición
    de requests.args(). Seguidamente se obtiene la partida del mismo id del usuario y sus respectivos movimientos. Por último,
    lo transforma en un diccionario y crea el archivo .json con toda la información.

    Retorna:
    --------
    tuple[str,int]
        Devuelve el par (respuesta,codigo).
    """
    nombre = get_jwt_identity()
    game_id = request.args.get('id', '')

    if not game_id:
        return 'Falta id partida', 400

    if not os.path.exists(f'{DIR_JSON}'):
        os.makedirs(DIR_JSON, exist_ok=True)

    partida = obtener_partida_usuario(game_id)
    if not partida:
        return f'No se ha encontrado partidas de {nombre}', 404

    movimientos = obtener_datos_partida(game_id)
    if not movimientos:
        return f'No se han encontrado datos de la partida', 404

    datos: dict = {
        'jugador_blanco': partida['jugador_blanco'],
        'jugador_negro': partida['jugador_negro'],
        'duracion': partida['duracion'],
        'resultado': partida['resultado'],
        'movimientos': movimientos
    }
    print(os.path.exists(f'{DIR_JSON}/{game_id}.json'))

    print(datos)
    print(movimientos)

    if os.path.exists(f'{DIR_JSON}/{game_id}.json'):
        os.remove(f'{DIR_JSON}/{game_id}.json')
        print("Eliminando mierda")

    with open(f'{DIR_JSON}/{game_id}.json', 'w') as escritura:
        json.dump(datos, escritura, indent=4)

    return 'Se ha exportado correctamente', 200

@app.route('/partida', methods=['POST'])
@jwt_required()
def crear_partida() -> tuple[str,int]:
    """
    Inicializa una nueva partida en la base de datos

    Se obtiene el nombre del usuario con su token y se obtienen los parametros 'contrincante' y 'color' a traves de la petición
    de requests.args(). Seguidamente se crea el id del juego y se crea en la base de datos.

    Retorna:
    --------
    tuple[str,int]
        Devuelve el par (respuesta,codigo).
    """
    contrincante = request.args.get('contrincante', '')
    color = request.args.get('color', '')
    usuario = get_jwt_identity()

    if not contrincante:
        return 'Falta contrincante', 400

    jugador_blanco = usuario if color else contrincante
    jugador_negro = contrincante if color else usuario

    crear_partida_en_bd(jugador_blanco, jugador_negro)

    return 'Partida creada con exito', 200

@app.route('/partida', methods=['DELETE'])
@jwt_required()
def eliminar_partida() -> tuple[str,int]:
    """
    Elimina una partida almacenada en la base de datos

    Se obtiene el nombre del usuario con su token y se obtiene el parametro 'id' a traves de la petición
    de requests.args(). Seguidamente se elimina el juego que contiene la id y el usuario como uno de los jugadores.

    Retorna:
    --------
    tuple[str,int]
        Devuelve el par (respuesta,codigo).
    """
    game_id = request.args.get('id', '')
    usuario = get_jwt_identity()

    if not game_id:
        return 'Falta id partida', 400

    try:
        eliminar_partida_en_bd(usuario, game_id)
    except sqlite3.InternalError:
        return 'No se ha podido eliminar la partida', 404

    return 'Patida eliminada con éxito', 200

@app.route('/partida', methods=['GET'])
@jwt_required()
def obtener_partidas() -> tuple[str,int] | tuple[list[dict],int]:
    """
    Obtiene todas las partidas del usuario registradas en la base de datos

    Se obtiene el nombre del usuario con su token y se retorna todas las partidas del usuario si se han encontrado. En caso
    contrario se devuelve el texto de error y su código correspondiente.

    Retorna:
    --------
    tuple[str,int] | tuple[list[dict],int]
        Devuelve el par (respuesta,codigo) si algo ha salido mal. En caso contrario se retorna la lista de partidas del usuario
        y el codigo 200.
    """
    usuario = get_jwt_identity()

    partidas = obtener_lista_partidas_usuario(usuario)

    if not partidas:
        return f'No se han encontrado partidas de {usuario}', 404

    return [dict(partida) for partida in partidas], 200

if __name__ == "__main__":
    inicializar_bd()
    app.run(debug=True)