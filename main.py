from crypt import methods
from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity, get_jwt
import hashlib

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "ContraseñaSuperSecreta"
jwt = JWTManager(app)

users = {}
data = {}

@app.route('/signup', methods=['POST'])
def singup() -> tuple[str,int]:
    user = request.args.get('user', '')
    if user in users:
        return f"Usuario {user} ya existe", 409
    else:
        contraseña = request.args.get('password', '')
        hashed = hashlib.sha256(contraseña.encode()).hexdigest()
        users[user] = hashed
        return f"Usuario {user} registrado", 200

@app.route('/login', methods=['GET'])
def login():
    user = request.args.get('user', '')
    contraseña = request.args.get('password', '')
    hashed = hashlib.sha256(contraseña.encode()).hexdigest()

    if user in users and users[user] == hashed:
        return create_access_token(identity=user), 200
    else:
        return f"Usuario o contraseña incorrectos", 401

@app.route('/')
def hello_world():
    return "Hola mundo"

@app.route('/data', methods=['GET'])
def get_data() -> tuple[list, int]:
    return list(data.keys()),200

@app.route('/data/<string:id>', methods=['POST'])
def add_data(id : str) -> tuple[str, int]:
    if id not in data:
        data[id] = request.args.get('value', '')
        return f"Dato {id} añadido", 200
    else:
        return f"Dato {id} ya existe", 409

@app.route('/data/<id>', methods=['GET'])
def get_data_id(id : str) -> tuple[str,int]:
    try:
        return data[id], 200
    except KeyError:
        return f"Dato {id} no encontrado", 404

@app.route('/data/<id>', methods=['PUT'])
def update_data(id : str) -> tuple[str,int]:
    if id in data:
        data[id] = request.args.get('value', '')
        return f"Dato {id} actualizado", 200
    else:
        return f"Dato {id} no encontrado", 404

@app.route('/data/<id>', methods=['DELETE'])
def delete_data(id) -> tuple[str,int]:
    if id in data:
        del data[id]
        return f"Dato {id} eliminado", 200
    else:
        return f"Dato {id} no encontrado", 404

if __name__ == "__main__":
    app.run(debug=True)
    get_data()