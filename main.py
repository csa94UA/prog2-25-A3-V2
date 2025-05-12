from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import hashlib
from typing import Union
from Base_de_datos.base_datos import *

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "ContraseñaSuperSecreta"
jwt = JWTManager(app)

users = cargar_usuarios()
data = {
    "Partidas_finalizadas" : cargar_partidas_finalizadas(),
    "Partidas_sin_acabar" : cargar_patidas_sin_finalizar()
}

@app.route('/signup', methods=['POST'])
def singup() -> tuple[str,int]:
    nombre = request.args.get('user')
    contraseña = request.args.get('password')
    correo = request.args.get('email')
    pais = request.args.get('pais')

    if not all([nombre, contraseña, correo, pais]):
        return "Faltan campos", 400

    if nombre in users["nombre"]:
        return f"Usuario {nombre} ya existe", 409

    hashed = hashlib.sha256(contraseña.encode()).hexdigest()
    users.loc[3] = [3,nombre, hashed, correo]

    return f"Usuario {nombre} registrado", 200

@app.route('/login', methods=['GET'])
def login():
    nombre = request.args.get('user', '')
    contraseña = request.args.get('password', '')
    hashed = hashlib.sha256(contraseña.encode()).hexdigest()

    if not nombre or not contraseña:
        return f"Faltan campos: nombre y/o contraseña",400

    fila = users[users['nombre'] == nombre]

    if fila.empty:
        return "Usuario no encontrado", 404

    contraseña = fila.iloc[0]['contraseña']

    if contraseña == hashed:
        return create_access_token(identity=nombre), 200
    else:
        return f"Usuario o contraseña incorrectos", 401

@app.route('/save', methods=['PUT'])
def save() -> None:
    guardar_tablas(users, "usuarios")
    guardar_tablas(data["Partidas_finalizadas"], "partidas_finalizadas")
    guardar_tablas(data["Partidas_sin_acabar"], "partidas_sin_acabar")

    return None


@app.route('/data', methods=['GET'])
@jwt_required()
def get_data() -> tuple[list, int]:
    return list(data.keys()),200

@app.route('/data/<string:id>', methods=['POST'])
@jwt_required()
def add_data(id : str) -> tuple[str, int]:
    if id not in data:
        data[id] = request.args.get('value', '')
        return f"Dato {id} añadido", 200
    else:
        return f"Dato {id} ya existe", 409

@app.route('/data/<id>', methods=['GET'])
@jwt_required()
def get_data_id(id : str) -> tuple[str,int]:
    try:
        return data[id], 200
    except KeyError:
        return f"Dato {id} no encontrado", 404

@app.route('/data/<id>', methods=['PUT'])
@jwt_required()
def update_data(id : str) -> tuple[str,int]:
    if id in data:
        data[id] = request.args.get('value', '')
        return f"Dato {id} actualizado", 200
    else:
        return f"Dato {id} no encontrado", 404

@app.route('/data/<id>', methods=['DELETE'])
@jwt_required()
def delete_data(id) -> tuple[str,int]:
    if id in data:
        del data[id]
        return f"Dato {id} eliminado", 200
    else:
        return f"Dato {id} no encontrado", 404

@app.route('/game/export', methods=['GET'])
@jwt_required()
def descargar_partida_json() -> Union[str, tuple[str, int]]:
    game_id = request.args.get('game_id', '')
    if not game_id:
        return "Error: Parámetro game_id requerido", 400

    return game_id

@app.route('/cloud-eval', methods=['POST'])
@jwt_required()
def obtener_jugada_ia() -> Union[str, tuple[str, int]]:
    payload = request.get_json()
    fen = payload.get('fen', '')
    if not fen:
        return "Error: Parámetro fen requerido", 400

    return fen

@app.route('/study', methods=['POST'])
@jwt_required()
def crear_estudio_privado() -> Union[str, tuple[str, int]]:
    nombre = request.args.get('nombre', '')
    if not nombre:
        return "Error: Falta el nombre del estudio", 400

    return nombre

if __name__ == "__main__":
    app.run(debug=True)