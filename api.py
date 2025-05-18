from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt
from typing import Dict,Optional,Union,Any,List,Tuple
from datetime import timedelta,datetime


from usuario.registro import registrar_usuario,iniciar_sesion
from usuario.usuario import Usuario
from usuario.ranking import obtener_ranking, obtener_posicion_usuario
from usuario.friend_manager import mostrar_perfil_amigo, enviar_solicitud_amistad, aceptar_solicitud, mostrar_amigos, eliminar_amigo,enviar_reto_a_amigo,aceptar_reto,rechazar_reto,obtener_retos,enviar_mensaje,obtener_chat,obtener_solicitudes_amistad
from utiles.file_menager import cargar_partida
from juego.sesion_juego import SesionDeJuego
from juego.usuarioIA import UsuarioIA 
from config import JWT_PASSWORD

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_PASSWORD
app.config["JWT_BLACKLIST_ENABLED"] = True

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

jwt = JWTManager(app)

blacklist = set()
sesiones_activas: Dict[str, SesionDeJuego] = {}

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist


@app.route('/', methods=['GET'])
def raiz() -> tuple[Dict[str, str], int]:
    """
    Endpoint sencillo en la raíz que devuelve un mensaje básico de estado.

    Returns:
        tuple[Dict[str, str], int]: Mensaje JSON y código HTTP 200.
    """
    return {"mensaje": "API funcionando correctamente"}, 200


@app.route('/salir', methods=['POST'])
@jwt_required()
def salirr():
    jti = get_jwt()["jti"] 
    blacklist.add(jti) 
    return jsonify({"msg": "Logout exitoso"}), 200


@app.route('/registrar', methods=['POST'])
def registrar_usuarioo() -> Dict[str, str]:
    """
    Endpoint para registrar un nuevo usuario.
    Recibe JSON con 'username' y 'password'.
    Valida que el usuario no exista y que la contraseña sea segura.
    Retorna mensaje de éxito o error.
    """
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    try:
        nuevo_usuario: Optional[Usuario] = registrar_usuario(username, password)
        acces_token = create_access_token(identity=nuevo_usuario.username)
        return jsonify({
            "mensaje": f"Usuario '{nuevo_usuario.username}' registrado correctamente.",
            "acces_token": acces_token,
            "user_id":nuevo_usuario.user_id
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/iniciarsesion', methods=['POST'])
def iniciar_sesionn():
    """
    Endpoint para iniciar sesión.
    Recibe JSON con 'username' y 'password'.
    Valida credenciales y devuelve access token si es correcto.
    """
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    try:
        usuario: Optional[Usuario] = iniciar_sesion(username, password)
        access_token = create_access_token(identity=usuario.username)
        return jsonify({
            "mensaje": f"Inicio de sesión exitoso para {usuario.username}",
            "access_token": access_token,
            "user_id":usuario.user_id
        }),201
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    

@app.route("/ranking", methods=["GET"])
def obtener_rankingg():
    """
    Endpoint para obtener el ranking de usuarios por ELO.

    Query Params:
    -------------
    top_n : int (opcional)
        Número de usuarios a retornar (por defecto 10).

    Retorna:
    --------
    JSON con la lista de los mejores usuarios por ELO.
    """
    try:
        top_n = int(request.args.get("top_n", 10))
        ranking = obtener_ranking(top_n)
        return jsonify(ranking), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route("/ranking/posicion/<string:username>", methods=["GET"])
def obtener_posicion_usuarioo(username: str):
    """
    Endpoint que devuelve la posición de un usuario en el ranking global por ELO.

    Parámetros de URL:
    ------------------
    username : str
        Nombre del usuario a consultar.

    Retorna:
    --------
    JSON con la posición o mensaje de error si no se encuentra.
    """
    try:
        posicion = obtener_posicion_usuario(username)
        if posicion is not None:
            return jsonify({"username": username, "posicion": posicion}), 200
        else:
            return jsonify({"error": "Usuario no encontrado."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/amigos', methods=['GET'])
@jwt_required()
def mostrar_amigoss():
    """
    Endpoint para obtener la lista de amigos de un usuario específico.

    Parámetros:
    -----------
    usuario_id : str (en la URL)
        ID del usuario del que se desea obtener la lista de amigos.

    Requiere autenticación JWT.

    Retorna:
    --------
    JSON con la lista de amigos o un mensaje de error.
    """
    try:
        identidad = get_jwt_identity()
        resultado = mostrar_amigos(identidad)

        if "error" in resultado:
            return jsonify({"error": resultado["error"]}), 404

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    

@app.route("/amigos/perfil/<string:username_amigo>", methods=["GET"])
@jwt_required()
def mostrar_perfil_amigoo(username_amigo: str):
    """
    Endpoint para obtener el perfil de un amigo del usuario autenticado.

    Parámetros de ruta:
    -------------------
    username_amigo : str
        Nombre de usuario del amigo cuyo perfil se desea consultar.

    Retorna:
    --------
    JSON con los datos del perfil del amigo o mensaje de error.
    """
    try:
        identidad = get_jwt_identity()
        usuario: Optional[Usuario] = Usuario.cargar_por_username(identidad)

        if not usuario:
            return jsonify({"error": "Usuario autenticado no encontrado."}), 404

        resultado = mostrar_perfil_amigo(usuario, username_amigo)
        return jsonify({"perfil":resultado}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500


@app.route('/amigos/solicitudes', methods=['GET'])
@jwt_required()
def solicitudes_amistad() -> Optional[List[Dict[str, str]]]:
    """
    Endpoint que devuelve todas las solicitudes de amistad pendientes
    para el usuario autenticado usando la función obtener_solicitudes_amistad.

    Requiere:
    ---------
    JWT token válido.

    Retorna:
    --------º
    200 OK: Lista de solicitudes.
    404 Not Found: Si el usuario no existe.
    500 Internal Server Error: Error inesperado.
    """
    try:
        username: str = get_jwt_identity()
        solicitudes: List[Dict[str, str]] = obtener_solicitudes_amistad(username)
        return jsonify({"solicitudes":solicitudes}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:

        return jsonify({"error": f"Error al obtener solicitudes: {str(e)}"}), 500

@app.route("/amigos/solicitud", methods=["POST"])
@jwt_required()
def enviar_solicitud_amistadd() -> Dict[str, Union[str, Dict]]:
    try:
        data = request.get_json()
        if not data or "destinatario_username" not in data:
            return jsonify({"error": "Falta el nombre de usuario destinatario."}), 400

        destinatario_username = data["destinatario_username"]
        usuario_actual_username = get_jwt_identity()

        remitente = Usuario.cargar_por_username(usuario_actual_username)
        if remitente is None:
            return jsonify({"error": "Usuario remitente no encontrado."}), 404

        resultado = enviar_solicitud_amistad(remitente, destinatario_username)

        if "error" in resultado:
            return jsonify(resultado), 400

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
    

@app.route("/amigos/aceptar", methods=["POST"])
@jwt_required()
def aceptar_solicitudd() -> Dict[str, Union[str, Dict]]:
    try:
        data = request.get_json()
        if not data or "remitente_username" not in data:
            return jsonify({"error": "Falta el nombre de usuario remitente."}), 400

        remitente_username = data["remitente_username"]
        usuario_username = get_jwt_identity()

        aceptar_solicitud(usuario_username, remitente_username)

        return jsonify({"mensaje": f"Solicitud de {remitente_username} aceptada."}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
    

@app.route("/amigos/eliminar", methods=["DELETE"])
@jwt_required()
def eliminar_amigoo() -> Dict[str, Union[str, Dict]]:
    try:
        data = request.get_json()
        if not data or "amigo_id" not in data:
            return jsonify({"error": "Falta el ID del amigo a eliminar."}), 400

        amigo_id = data["amigo_id"]
        usuario_username = get_jwt_identity()
        usuario: Usuario = Usuario.cargar_por_username(usuario_username)

        if not usuario:
            return jsonify({"error": "Usuario no encontrado."}), 404

        eliminado = eliminar_amigo(usuario, amigo_id)
        if not eliminado:
            return jsonify({"error": "No se pudo eliminar al amigo (no encontrado o no era amigo)."}), 400

        return jsonify({"mensaje": "Amigo eliminado correctamente."}), 200

    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
    

@app.route("/partidas", methods=["GET"])
@jwt_required()
def mostrar_historiall() -> Dict[str, Any]:
    try:
        usuario_username = get_jwt_identity()
        usuario: Usuario = Usuario.cargar_por_username(usuario_username)

        if not usuario:
            return jsonify({"error": "Usuario no encontrado."}), 404

        resultado = usuario.mostrar_historial()
        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
    

app.route("/partidas/<string:nombre_sesion>", methods=["GET"])
@jwt_required()
def cargar_partidaa(nombre_sesion: str) -> Dict[str, Any]:
    try:
        if nombre_sesion in sesiones_activas:
            nombre_sesion ="temp/"+ nombre_sesion+"_temp"
        datos_partida = cargar_partida(nombre_sesion)
        return jsonify(datos_partida), 200
    except FileNotFoundError:
        return jsonify({"error": "La partida no existe."}), 404
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
    

@app.route("/retos", methods=["GET"])
@jwt_required()
def obtener_retoss() -> tuple:
    try:

        username: str = get_jwt_identity()
        
        retos: List[Dict[str, str]] = obtener_retos(username)
        
        return jsonify({"retos": retos}), 200
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


@app.route("/retos/enviar/<string:username_amigo>", methods=["POST"])
@jwt_required()
def enviar_reto_a_amigoo(username_amigo: str):
    try:
        retador_username: str = get_jwt_identity()
        
        sesion = enviar_reto_a_amigo(retador_username, username_amigo)
        if sesion:
            nombre_sesion = f"{username_amigo}_vs_{retador_username}"
            nombre_sesion = f"partida_{nombre_sesion}"

            if nombre_sesion in sesiones_activas:
                return jsonify({"error": "Esta sesión ya está activa."}), 400

            sesiones_activas[nombre_sesion] = sesion

            return jsonify({
                "mensaje": f"Reto aceptado. Partida iniciada entre {username_amigo} y {retador_username}. ",
                "sesion_id": nombre_sesion,
                "turno": sesion.turno,
                "jugador_blanco": sesion.jugador_blanco.username,
                "jugador_negro": sesion.jugador_negro.username
            }), 200
        return jsonify({"mensaje": f"Reto enviado a {username_amigo} correctamente."}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
    

@app.route("/retos/rechazar/<string:retador_username>", methods=["POST"])
@jwt_required()
def rechazar_retoo(retador_username: str):
    try:
        usuario_username: str = get_jwt_identity()

        rechazar_reto(usuario_username, retador_username)
        return jsonify({"mensaje": f"Reto de {retador_username} rechazado correctamente."}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
    

@app.route("/retos/aceptar/<string:retador_username>", methods=["POST"])
@jwt_required()
def aceptar_retoo(retador_username: str):
    try:
        usuario_username: str = get_jwt_identity()

        sesion: SesionDeJuego = aceptar_reto(usuario_username, retador_username)

        nombre_sesion = f"{usuario_username}_vs_{retador_username}"
        nombre_sesion = f"partida_{nombre_sesion}"

        if nombre_sesion in sesiones_activas:
            return jsonify({"error": "Esta sesión ya está activa."}), 400

        sesiones_activas[nombre_sesion] = sesion
        mensaje = "Reto aceptado. Partida iniciada entre "+usuario_username+" y "+retador_username+"."
        return jsonify({"mensaje":mensaje}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


@app.route("/partidas/<string:sesion_id>/mover", methods=["POST"])
@jwt_required()
def jugar_turnoo(sesion_id: str):
    """
    Endpoint para ejecutar un turno en una partida activa.

    Si después del movimiento del usuario es turno de una IA,
    este endpoint también ejecuta el movimiento de la IA y devuelve el estado completo.

    Parámetros:
    -----------
    sesion_id : str
        Identificador de la sesión activa (clave del diccionario global).

    Cuerpo JSON esperado:
    ---------------------
    {
        "origen": [fila, columna],
        "destino": [fila, columna],
        "promocion": "dama" | "torre" | "alfil" | "caballo" (opcional),
        "abandono": true (opcional)
    }

    Retorna:
    --------
    JSON con el resultado del turno (y el de la IA si aplica) o mensaje de error.
    """
    try:
        identidad: str = get_jwt_identity()

        if sesion_id not in sesiones_activas:
            return jsonify({"error": "Sesión no encontrada."}), 404

        sesion = sesiones_activas[sesion_id]

        usernames = {sesion.jugador_blanco.username, sesion.jugador_negro.username}
        if identidad not in usernames:
            return jsonify({"error": "No tienes permiso para jugar en esta partida."}), 403

        if sesion.terminado:
            return jsonify({"error": "La partida ya ha terminado."}), 400

        datos = request.get_json()

        if datos.get("abandono") is True:
            resultado = sesion.jugar_turno("abandono")
            return jsonify(resultado), 200

        if "origen" not in datos or "destino" not in datos:
            return jsonify({"error": "Debes especificar origen y destino del movimiento."}), 400

        origen: Tuple[int, int] = tuple(datos["origen"])
        destino: Tuple[int, int] = tuple(datos["destino"])
        promocion: str = datos.get("promocion")

        resultado_usuario = sesion.jugar_turno((origen, destino), promocion)

        if resultado_usuario.get("estado") == "terminado":
            return jsonify(resultado_usuario), 200

        siguiente_jugador = sesion.jugador_blanco if sesion.turno_actual == "blanco" else sesion.jugador_negro

        if isinstance(siguiente_jugador, UsuarioIA):
            resultado_ia = sesion.jugar_turno()

            return jsonify({
                "jugador": resultado_usuario,
                "ia": resultado_ia
            }), 200

        return jsonify(resultado_usuario), 200

    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
    
@app.route("/partidas/<string:sesion_id>/estado", methods=["GET"])
@jwt_required()
def estado_partidaa(sesion_id: str):
    """
    Devuelve el estado actual del tablero de una partida activa.

    Parámetros:
    -----------
    sesion_id : str
        ID único de la sesión de juego.

    Retorna:
    --------
    JSON con el tablero en texto, turno actual y estado general.
    """
    try:
        identidad: str = get_jwt_identity()

        if sesion_id not in sesiones_activas:
            return jsonify({"error": "La sesión no existe o ya terminó."}), 404

        sesion = sesiones_activas[sesion_id]

        jugadores = [sesion.jugador_blanco.username, sesion.jugador_negro.username]
        if identidad not in jugadores:
            return jsonify({"error": "No tienes acceso a esta partida."}), 403

        return jsonify({
            "jugador_blanco": sesion.jugador_blanco.username,
            "jugador_negro": sesion.jugador_negro.username,
            "turno_actual": sesion.turno_actual,
            "tablero": sesion.tablero.obtener_tablero_como_texto(),
            "estado": "terminado" if sesion.terminado else "en curso"
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


@app.route("/partidas/activas", methods=["GET"])
@jwt_required()
def partidas_activas_usuarioo():
    identidad = get_jwt_identity()
    activas = []
    for sesion_id, sesion in sesiones_activas.items():
        if identidad in (sesion.jugador_blanco.username, sesion.jugador_negro.username):
            activas.append({
                "sesion_id": sesion_id,
                "oponente": sesion.jugador_negro.username if identidad == sesion.jugador_blanco.username else sesion.jugador_blanco.username,
                "turno": sesion.turno_actual
            })
    return jsonify(activas), 200


@app.route('/amigos/<string:receptor_username>/mensaje', methods=['POST'])
@jwt_required()
def enviar_mensajee(receptor_username: str) -> tuple[Dict[str, str], int]:
    """
    Endpoint para enviar un mensaje a un amigo.
    El receptor se especifica en la URL, el contenido del mensaje en el body JSON.

    Args:
        receptor_username (str): Nombre de usuario del receptor (amigo).

    Request JSON:
        {
            "contenido": "texto del mensaje"
        }

    Returns:
        tuple[Dict[str, str], int]: Respuesta JSON con mensaje de éxito o error y código HTTP.

    """
    try:
        data: Optional[Dict[str, str]] = request.get_json()
        if not data or "contenido" not in data:
            return {"error": "Falta el campo 'contenido' en el cuerpo de la solicitud."}, 400
        
        contenido: str = data["contenido"]

        emisor_user: Optional[str] = get_jwt_identity()
        if not emisor_user:
            return {"error": "Usuario no autenticado."}, 401
        
        emisor: Optional[Usuario] = Usuario.cargar_por_username(emisor_user)
        if emisor is None:
            return {"error": "Usuario emisor no encontrado."}, 404

        resultado: Dict[str, str] = enviar_mensaje(emisor, receptor_username, contenido)

        if "error" in resultado:
            return resultado, 400

        return resultado, 200

    except Exception as e:
        return {"error": f"Error interno del servidor: {str(e)}"}, 500
    

@app.route('/amigos/<string:otro_username>/chat', methods=['GET'])
@jwt_required()
def obtener_chatt(otro_username: str) -> tuple[Union[List[Dict[str, str]], Dict[str, str]], int]:
    """
    Endpoint para obtener el historial completo de mensajes con otro usuario amigo.
    El otro usuario se especifica en la URL.

    Args:
        otro_username (str): Nombre de usuario del otro participante del chat.

    Returns:
        tuple[Union[List[Dict[str, str]], Dict[str, str]], int]: 
            - Lista de mensajes con estructura: 
              [{"emisor": str, "receptor": str, "contenido": str, "timestamp": str}, ...]
            - En caso de error, diccionario con mensaje y código HTTP correspondiente.
    """
    try:
        emisor_user: Optional[str] = get_jwt_identity()
        if not emisor_user:
            return {"error": "Usuario no autenticado."}, 401
        
        usuario: Optional[Usuario] = Usuario.cargar_por_username(emisor_user)
        if usuario is None:
            return {"error": "Usuario no encontrado."}, 404

        resultado: Union[List[Dict[str, str]], Dict[str, str]] = obtener_chat(usuario, otro_username)

        if isinstance(resultado, dict) and "error" in resultado:
            return resultado, 400

        return resultado, 200

    except Exception as e:
        return {"error": f"Error interno del servidor: {str(e)}"}, 500

if __name__ == "__main__":
    app.run(debug=True)