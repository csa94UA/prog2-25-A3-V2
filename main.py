import os
import json
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

@app.route('/protegido', methods=['GET'])
@jwt_required()
def protegido():
    usuario = get_jwt_identity()
    return 'nombre' + usuario

@app.route('/signup', methods=['POST'])
def singup() -> tuple[str,int]:
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
    nombre = get_jwt_identity()
    datos = obtener_datos_usuario(nombre)
    if not datos:
        return 'No se ha encontrado al usuario', 404

    return dict(datos),200

@app.route('/perfil', methods=['PUT'])
@jwt_required()
def modificar_perfil() -> tuple[str,int]:
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
    nombre = get_jwt_identity()
    game_id = request.args.get('id', '')

    print("Game_id: ",game_id)

    if not game_id:
        return 'Falta id partida', 400

    if not os.path.exists(f'{DIR_JSON}'):
        os.makedirs(DIR_JSON, exist_ok=True)

    partida = obtener_partida_usuario(game_id)
    print(partida.keys())
    if not partida:
        return f'No se ha encontrado partidas de {nombre}', 404

    movimientos = obtener_datos_partida(game_id)
    print(movimientos)
    if not movimientos:
        return f'No se han encontrado datos de la partida', 404

    datos: dict = {
        'jugador_blanco': partida['jugador_blanco'],
        'jugador_negro': partida['jugador_negro'],
        'duracion': partida['duracion'],
        'resultado': partida['resultado'],
        'movimientos': movimientos
    }

    with open(f'{DIR_JSON}/{game_id}', 'w') as escritura:
        json.dump(datos, escritura, indent=4)

    return 'Se ha exportado correctamente', 200

@app.route('/partida', methods=['POST'])
@jwt_required()
def crear_partida() -> tuple[str,int]:
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
def obtener_partidas():
    usuario = get_jwt_identity()

    partidas = obtener_lista_partidas_usuario(usuario)

    if not partidas:
        return f'No se han encontrado partidas de {usuario}', 404

    return [dict(partida) for partida in partidas], 200

if __name__ == "__main__":
    inicializar_bd()
    app.run(debug=True)