import os
import json
from typing import Dict, List, Optional, Union
from datetime import datetime

from usuario.usuario import Usuario
from juego.usuarioIA import UsuarioIA
from juego.sesion_juego import SesionDeJuego 
from config import PATH_SOLICITUDES, PATH_RETOS, PATH_CHATS


def _ruta_chat(user1_id: str, user2_id: str) -> str:
    """
    Construye la ruta única del archivo JSON que almacena el chat entre dos usuarios.
    Los IDs se ordenan para evitar duplicados en diferente orden.

    Args:
        user1_id (str): ID del primer usuario.
        user2_id (str): ID del segundo usuario.

    Returns:
        str: Ruta del archivo de chat.
    """
    ids_ordenados: List[str] = sorted([user1_id, user2_id])
    return os.path.join(PATH_CHATS, f"{ids_ordenados[0]}_{ids_ordenados[1]}.json")


def _ruta_retos(username: str) -> str:
    """
    Devuelve la ruta del archivo de retos del usuario.

    Parámetros:
    -----------
    username : str
        ID del usuario.

    Retorna:
    --------
    str
        Ruta al archivo JSON que contiene los retos pendientes.
    """
    return os.path.join(PATH_RETOS, f"{username}.json")


def _ruta_solicitudes(username: str) -> str: 
    """
    Devuelve la ruta del archivo de solicitudes del usuario.

    Parámetros:
    -----------
    username : str
        ID del usuario.

    Retorna:
    --------
    str
        Ruta completa al archivo de solicitudes.
    """
    return os.path.join(PATH_SOLICITUDES, f"{username}.json")


def enviar_solicitud_amistad(remitente: Usuario, destinatario_username: str) -> Dict[str, str]:
    """
    Envía una solicitud de amistad desde el usuario remitente al destinatario especificado.

    Parámetros:
    -----------
    remitente : Usuario
        Usuario que envía la solicitud de amistad.
    destinatario_username : str
        Nombre del usuario que recibirá la solicitud.

    Retorna:
    --------
    Dict[str, str]
        Diccionario indicando si la solicitud fue enviada o ya existía, o si hubo un error.
    """
    destinatario: Optional[Usuario] = Usuario.cargar_por_username(destinatario_username)
    if not destinatario:
        return {"error": "El usuario no existe."}
    
    # Impedir solicitudes a cuentas IA
    if isinstance(destinatario, UsuarioIA):
        return {"error": "No puedes enviar solicitudes de amistad a una cuenta de IA."}
    
    if remitente.user_id in destinatario.amigos:
        return {"mensaje": f"{destinatario_username} ya es tu amigo."}

    ruta: str = _ruta_solicitudes(destinatario.user_id)
    solicitudes: List[Dict[str, str]] = []

    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            solicitudes = json.load(f)

    if any(s["user_id"] == remitente.user_id for s in solicitudes):
        return {"mensaje": "Ya has enviado una solicitud a este usuario."}

    solicitudes.append({
        "remitente": remitente.username,
        "user_id": remitente.user_id
    })

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(solicitudes, f, indent=4)

    return {"mensaje": f"Solicitud enviada a {destinatario.username}."}


def aceptar_solicitud(usuario_username: str, remitente_username: str) -> None:
    """
    Acepta una solicitud de amistad enviada por otro usuario.

    Parámetros:
    -----------
    usuario_username : str
        Nombre de usuario que está aceptando la solicitud.
    remitente_username : str
        Nombre del usuario que envió la solicitud.

    Lanza:
    ------
    ValueError
        Si el usuario, remitente o la solicitud no existen, o si no se pudo completar la operación.
    """
    usuario: Optional[Usuario] = Usuario.cargar_por_username(usuario_username)
    if not usuario:
        raise ValueError("Usuario no encontrado.")

    ruta: str = _ruta_solicitudes(usuario.user_id)
    if not os.path.exists(ruta):
        raise ValueError("No tienes solicitudes de amistad.")

    with open(ruta, "r", encoding="utf-8") as f:
        solicitudes: List[Dict[str, str]] = json.load(f)

    # Buscar la solicitud del remitente
    solicitud: Optional[Dict[str, str]] = next((s for s in solicitudes if s["remitente"] == remitente_username), None)
    if not solicitud:
        raise ValueError("No se encontró una solicitud de ese remitente.")

    remitente: Optional[Usuario] = Usuario.cargar_por_username(remitente_username)
    if not remitente:
        raise ValueError("El remitente ya no existe.")

    if not agregar_amigo(usuario, remitente.username):
        raise ValueError("No se pudo agregar como amigo.")

    # Eliminar la solicitud aceptada
    solicitudes = [s for s in solicitudes if s["remitente"] != remitente_username]

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(solicitudes, f, indent=4)


def mostrar_perfil_amigo(usuario: Usuario, username_amigo: str) -> Dict[str, Union[str, int]]:
    """
    Devuelve el perfil de un amigo, incluyendo nombre de usuario, ELO y cantidad de partidas jugadas.

    Parámetros:
    -----------
    usuario : Usuario
        Usuario actual que consulta el perfil del amigo.
    username_amigo : str
        Nombre de usuario del amigo a consultar.

    Retorna:
    --------
    Dict[str, Union[str, int]]
        Diccionario con información del amigo.

    Lanza:
    ------
    ValueError
        Si el usuario no existe o no es un amigo del usuario actual.
    """
    amigo: Optional[Usuario] = Usuario.cargar_por_username(username_amigo)
    if not amigo:
        raise ValueError("Usuario no encontrado.")

    if amigo.user_id not in usuario.amigos:
        raise ValueError("Este usuario no es tu amigo.")

    return {
        "username": amigo.username,
        "elo": amigo.elo,
        "partidas_jugadas": len(amigo.historial)
    }


def agregar_amigo(usuario: Usuario, username_amigo: str) -> bool:
    """
    Agrega un usuario como amigo de manera mutua si ambos cumplen las condiciones.

    Parámetros:
    -----------
    usuario : Usuario
        Usuario actual que desea agregar un amigo.
    username_amigo : str
        Nombre del usuario que se desea agregar.

    Retorna:
    --------
    bool
        True si se agregó exitosamente, False si hubo algún problema.
    """
    if username_amigo == usuario.username:
        return False

    amigo: Optional[Usuario] = Usuario.cargar_por_username(username_amigo)
    if not amigo:
        return False

    if amigo.user_id in usuario.amigos:
        return False

    usuario.amigos.append(amigo.user_id)
    amigo.amigos.append(usuario.user_id)

    usuario.guardar()
    amigo.guardar()
    return True


def eliminar_amigo(usuario: Usuario, amigo_id: str) -> bool:
    """
    Elimina la amistad entre el usuario actual y otro usuario.

    Parámetros:
    -----------
    usuario : Usuario
        Usuario que quiere eliminar un amigo.
    amigo_id : str
        ID del amigo que se desea eliminar.

    Retorna:
    --------
    bool
        True si se eliminó correctamente, False si no se encontró o no era amigo.
    """
    amigo: Optional[Usuario] = Usuario.cargar(amigo_id)
    if not amigo:
        return False

    if amigo.user_id not in usuario.amigos:
        return False

    usuario.amigos.remove(amigo.user_id)
    if usuario.user_id in amigo.amigos:
        amigo.amigos.remove(usuario.user_id)

    usuario.guardar()
    amigo.guardar()
    return True


def mostrar_amigos(usuario_id: str) -> Dict[str, Union[List[str], str, Dict[str, str]]]:
    """
    Devuelve la lista de amigos de un usuario a partir de su nombre de usuario.

    Parámetros:
    -----------
    usuario_id : str
        Nombre de usuario del usuario que quiere ver su lista de amigos.

    Retorna:
    --------
    Dict[str, Union[List[str], str]]
        Diccionario con la lista de amigos (usernames) o mensaje de error.
    """
    usuario: Optional[Usuario] = Usuario.cargar_por_username(usuario_id)
    if not usuario:
        return {"error": "Usuario no encontrado."}

    if not usuario.amigos:
        return {"amigos": [], "mensaje": "No tienes amigos añadidos."}

    lista_amigos: List[str] = []
    for amigo_id in usuario.amigos:
        datos_amigo: Optional[Usuario] = Usuario.cargar(amigo_id)
        if datos_amigo:
            lista_amigos.append(datos_amigo.username)

    return {"amigos": lista_amigos}


def enviar_reto_a_amigo(retador_username: str, username_amigo: str) -> None:
    """
    Envía un reto de partida al amigo especificado si no hay uno pendiente.

    Parámetros:
    -----------
    retador_username : str
        Nombre del usuario que envía el reto.
    username_amigo : str
        Nombre del amigo que recibirá el reto.

    Retorna:
    --------
    None

    Lanza:
    ------
    ValueError
        Si el usuario se reta a sí mismo, el amigo no existe, no son amigos,
        o ya se ha enviado un reto previamente.
    """
    if username_amigo == retador_username:
        raise ValueError("No puedes retarte a ti mismo.")

    retador: Optional[Usuario] = Usuario.cargar_por_username(retador_username)
    amigo: Optional[Usuario] = Usuario.cargar_por_username(username_amigo)

    if not retador or not amigo:
        raise ValueError("El usuario no existe.")

    # Si es IA, iniciar automáticamente la partida
    if isinstance(amigo, UsuarioIA):
        return SesionDeJuego(retador, amigo)

    if amigo.user_id not in retador.amigos:
        raise ValueError("Este usuario no es tu amigo.")

    ruta: str = _ruta_retos(amigo.user_id)
    retos: List[Dict[str, str]] = []

    # Leer retos existentes si hay archivo
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            retos = json.load(f)

    if any(r["user_id"] == retador.user_id for r in retos):
        raise ValueError("Ya has enviado un reto a este usuario.")

    retos.append({
        "retador": retador.username,
        "user_id": retador.user_id
    })

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(retos, f, indent=4)


def aceptar_reto(usuario_username: str, retador_username: str) -> SesionDeJuego:
    """
    Acepta un reto enviado por otro usuario e inicia una sesión de juego.

    Parámetros:
    -----------
    usuario_username : str
        Nombre de usuario que acepta el reto.
    retador_username : str
        Nombre del usuario que envió el reto.

    Retorna:
    --------
    SesionDeJuego
        Instancia de la sesión de juego entre el usuario y el retador.

    Lanza:
    ------
    ValueError
        Si alguno de los usuarios no existe, no hay retos o no se encuentra el reto especificado.
    """
    usuario: Optional[Usuario] = Usuario.cargar_por_username(usuario_username)
    retador: Optional[Usuario] = Usuario.cargar_por_username(retador_username)

    if not usuario:
        raise ValueError("El usuario no existe.")
    if not retador:
        raise ValueError("El retador no existe.")

    ruta: str = _ruta_retos(usuario.user_id)
    if not os.path.exists(ruta):
        raise ValueError("No tienes retos pendientes.")

    with open(ruta, "r", encoding="utf-8") as f:
        retos: List[Dict[str, str]] = json.load(f)

    seleccionado = next((r for r in retos if r["user_id"] == retador.user_id), None)

    if not seleccionado:
        raise ValueError("No se encontró el reto del usuario especificado.")
    
    # Eliminar el reto aceptado del archivo
    retos.remove(seleccionado)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(retos, f, indent=4)

    return SesionDeJuego(retador, usuario)


def rechazar_reto(usuario_username: str, retador_username: str) -> None:
    """
    Rechaza un reto pendiente de otro usuario.

    Parámetros:
    -----------
    usuario_username : str
        Nombre del usuario que rechaza el reto.
    retador_username : str
        Nombre del usuario que envió el reto.

    Lanza:
    ------
    ValueError
        Si alguno de los usuarios no existe, no hay retos o no se encuentra el reto.
    """
    usuario: Optional[Usuario] = Usuario.cargar_por_username(usuario_username)
    retador: Optional[Usuario] = Usuario.cargar_por_username(retador_username)

    if not usuario:
        raise ValueError("El usuario no existe.")
    if not retador:
        raise ValueError("El retador no existe.")

    ruta: str = _ruta_retos(usuario.user_id)
    if not os.path.exists(ruta):
        raise ValueError("No tienes retos pendientes.")

    with open(ruta, "r", encoding="utf-8") as f:
        retos: List[Dict[str, str]] = json.load(f)

    seleccionado = next((r for r in retos if r["user_id"] == retador.user_id), None)

    if not seleccionado:
        raise ValueError("No se encontró el reto del usuario especificado.")

    # Eliminar el reto rechazado del archivo
    retos.remove(seleccionado)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(retos, f, indent=4)


def obtener_retos(username: str) -> List[Dict[str, str]]:
    """
    Devuelve la lista de retos pendientes para un usuario.

    Parámetros:
    -----------
    username : str
        Nombre de usuario.

    Retorna:
    --------
    List[Dict[str, str]]
        Lista de retos pendientes con datos de los retadores.
        Si no hay archivo, se retorna una lista vacía.
    """
    user: Optional[Usuario] = Usuario.cargar_por_username(username)
    if not user:
        return []

    ruta: str = _ruta_retos(user.user_id)
    if not os.path.exists(ruta):
        return []

    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)
    
def enviar_mensaje(emisor: Usuario, receptor_username: str, contenido: str) -> Dict[str, str]:
    """
    Envía un mensaje desde un usuario emisor a otro receptor, solo si ambos son amigos.
    El mensaje se guarda en un archivo JSON correspondiente al chat entre ambos.

    Args:
        emisor (Usuario): Instancia del usuario que envía el mensaje.
        receptor_username (str): Nombre de usuario del receptor.
        contenido (str): Texto del mensaje a enviar.

    Returns:
        Dict[str, str]: Diccionario con el resultado de la operación:
            - En caso de éxito: {"mensaje": "Mensaje enviado correctamente."}
            - En caso de error: {"error": "Descripción del error"}
    """
    receptor: Optional[Usuario] = Usuario.cargar_por_username(receptor_username)
    if receptor is None:
        return {"error": "El receptor no existe."}

    if receptor.user_id not in emisor.amigos:
        return {"error": "No puedes enviar mensajes a alguien que no es tu amigo."}

    ruta: str = _ruta_chat(emisor.user_id, receptor.user_id)
    chat: List[Dict[str, str]] = []

    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            chat = json.load(f)

    mensaje: Dict[str, str] = {
        "emisor": emisor.username,
        "receptor": receptor.username,
        "contenido": contenido,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
    }

    chat.append(mensaje)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(chat, f, indent=4)

    return {"mensaje": "Mensaje enviado correctamente."}


def obtener_chat(usuario: Usuario, otro_username: str) -> Union[List[Dict[str, str]], Dict[str, str]]:
    """
    Obtiene el historial completo de mensajes entre el usuario y otro usuario amigo.
    Devuelve un listado de mensajes o un error si no son amigos o el usuario no existe.

    Args:
        usuario (Usuario): Instancia del usuario que solicita el chat.
        otro_username (str): Nombre de usuario del otro participante del chat.

    Returns:
        Union[List[Dict[str, str]], Dict[str, str]]:
            - Lista de mensajes (cada mensaje es un dict con claves: emisor, receptor, contenido, timestamp)
            - Diccionario con error en caso de que el otro usuario no exista o no sean amigos.
    """
    otro: Optional[Usuario] = Usuario.cargar_por_username(otro_username)
    if otro is None:
        return {"error": "El otro usuario no existe."}

    if otro.user_id not in usuario.amigos:
        return {"error": "No puedes ver el chat con alguien que no es tu amigo."}

    ruta: str = _ruta_chat(usuario.user_id, otro.user_id)

    if not os.path.exists(ruta):
        return []

    with open(ruta, "r", encoding="utf-8") as f:
        chat: List[Dict[str, str]] = json.load(f)

    return chat