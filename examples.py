import getpass
import requests
import time
from typing import Any, Type,Dict,List,Tuple,Optional,Union


BASE_URL = "http://localhost:5000" 
usuario_id:str = None
usuario_username:str = None

def solicitar_parametro(
    nombre: str,
    tipo_dato: Type,
    lon_min: int = 0,
    is_password: bool = False
) -> Any:
    """
    Solicita un valor por consola para una variable, validando su tipo y longitud mínima.

    Parámetros:
    -----------
    nombre : str
        Descripción del dato a solicitar (ejemplo: "Contraseña", "Edad").
    tipo_dato : Type
        Tipo de dato esperado (ej: str, int, float).
    lon_min : int, opcional
        Longitud mínima que debe tener la entrada (solo aplicable a texto). Por defecto es 0.
    is_password : bool, opcional
        Si es True, oculta la entrada del usuario (como contraseñas). Por defecto es False.

    Retorna:
    --------
    Any
        El valor introducido por el usuario, convertido al tipo especificado.
    """
    while True:
        prompt: str = f"\n{nombre} (mínimo {lon_min} caracteres): " if lon_min else f"\n{nombre}: "

        entrada: str = (
            getpass.getpass(prompt) if is_password else input(prompt)
        )

        if isinstance(entrada, str) and len(entrada) < lon_min:
            print(f"La longitud debe ser al menos de {lon_min} caracteres.")
            continue

        try:
            valor = tipo_dato(entrada)
            return valor
        except (ValueError, TypeError):
            print(f"El valor ingresado no es válido para el tipo {tipo_dato.__name__}. Intenta nuevamente.")


def menu_registro() -> str:
    global usuario_id,usuario_username
    """
    Muestra el menú de registro. Permite al usuario registrarse, iniciar sesión o ver el ranking.
    Retorna el access token si el inicio de sesión o registro fue exitoso.
    """
    while True:
        print("\n--- MENÚ DE REGISTRO ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver ranking")
        print("4. Salir")
        
        opcion: str = input("Selecciona una opción: ")

        if opcion == "1":
            username = solicitar_parametro("Nombre de usuario", str, lon_min=3)
            password = solicitar_parametro("Contraseña", str, lon_min=8, is_password=True)

            response = requests.post(f"{BASE_URL}/registrar", json={
                "username": username,
                "password": password
            })
            
            datos = response.json()
            usuario_username = username
            usuario_id = datos["user_id"]
            if response.status_code == 201:
                print(datos["mensaje"])
                return datos["acces_token"]
            else:
                print(f"Error: {datos.get('error', 'Error desconocido.')}")

        elif opcion == "2":
            username = solicitar_parametro("Nombre de usuario", str)
            password = solicitar_parametro("Contraseña", str, is_password=True)

            response = requests.post(f"{BASE_URL}/iniciarsesion", json={
                "username": username,
                "password": password
            })

            datos = response.json()
            if response.status_code == 201:
                print(datos["mensaje"])
                return datos["access_token"]
            else:
                print(f"Error: {datos.get('error', 'Credenciales incorrectas.')}")

        elif opcion == "3":
            ranking()

        elif opcion == "4":
            print("Saliendo del sistema...")
            return False

        else:
            print("Opción inválida. Intenta de nuevo.")


def menu_amigos(token: str) -> None:
    while True:
        print("\n--- MENÚ DE AMIGOS ---")
        print("1. Mostrar amigos")
        print("2. Ver perfil de amigo")
        print("3. Enviar solicitud de amistad")
        print("4. Ver solicitudes pendientes")
        print("5. Aceptar solicitud")
        print("6. Eliminar amigo")
        print("7. Chat con amigo")
        print("8. Volver al menú principal")
        opcion = solicitar_parametro("Selecciona una opción",str)

        if opcion == "1":
            mostrar_amigos(token)
        elif opcion == "2":
            ver_perfil_amigo(token)
        elif opcion == "3":
            enviar_solicitud(token)
        elif opcion == "4":
            ver_solicitudes(token)
        elif opcion == "5":
            aceptar_solicitud(token)
        elif opcion == "6":
            eliminar_amigo(token)
        elif opcion == "7":
            chat_amigo(token)
        elif opcion == "8":
            break
        else:
            print("Opción inválida.")


def mostrar_amigos(token: str) -> None:
    url = f"{BASE_URL}/amigos"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    amigos = data.get("amigos", [])

    if not amigos:
        print("No tienes amigos aún.")
        return

    print("\n--- Lista de amigos ---")
    for i, amigo in enumerate(amigos):
        print(f"{i + 1}. {amigo}")


def ver_perfil_amigo(token: str) -> None:
    amigos = obtener_amigos(token)
    if not amigos:
        print("No tienes amigos para ver su perfil.")
        return

    print("\n--- Lista de amigos ---")
    for i, amigo in enumerate(amigos):
        print(f"{i + 1}. {amigo}")

    idx = solicitar_parametro("Selecciona el número del amigo",int) - 1
    if idx < 0 or idx >= len(amigos):
        print("Selección inválida.")
        return

    username = amigos[idx]
    url = f"{BASE_URL}/amigos/perfil/{username}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    datos = response.json().get("perfil")
    print("\n=== Perfil del Usuario ===")
    print(f"Nombre de usuario : {datos["username"]}")
    print(f"Puntos ELO        : {datos["elo"]}")
    print(f"Partidas jugadas  : {datos["partidas_jugadas"]}")


def enviar_solicitud(token: str) -> None:
    username = solicitar_parametro("Nombre del usuario al que enviar solicitud",str)
    url = f"{BASE_URL}/amigos/solicitud"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"destinatario_username": username}
    response = requests.post(url, json=data, headers=headers)
    print(response.json())


def ver_solicitudes(token: str) -> None:
    solicitudes = obtener_solicitudes(token)
    if not solicitudes:
        print("No tienes solicitudes pendientes.")
        return

    print("\n--- Solicitudes recibidas ---")
    for i, s in enumerate(solicitudes):
        print(f"{i + 1}. {s['remitente']}")


def aceptar_solicitud(token: str) -> None:
    solicitudes = obtener_solicitudes(token)
    if not solicitudes:
        print("No tienes solicitudes para aceptar.")
        return

    print("\n--- Solicitudes recibidas ---")
    for i, s in enumerate(solicitudes):
        print(f"{i + 1}. {s['remitente']}")

    idx = solicitar_parametro("Selecciona el número de la solicitud a aceptar",int) - 1
    if idx < 0 or idx >= len(solicitudes):
        print("Selección inválida.")
        return

    remitente = solicitudes[idx]["remitente"]
    url = f"{BASE_URL}/amigos/aceptar"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"remitente_username": remitente}
    response = requests.post(url, json=data, headers=headers)
    print(response.json())


def eliminar_amigo(token: str) -> None:
    amigos = obtener_amigos(token)
    if not amigos:
        print("No tienes amigos para eliminar.")
        return

    print("\n--- Lista de amigos ---")
    for i, amigo in enumerate(amigos):
        print(f"{i + 1}. {amigo}")

    idx = solicitar_parametro("Selecciona el número del amigo a eliminar",int) - 1
    if idx < 0 or idx >= len(amigos):
        print("Selección inválida.")
        return

    amigo_id = amigos[idx]
    url = f"{BASE_URL}/amigos/eliminar"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"amigo_id": amigo_id}
    response = requests.delete(url, json=data, headers=headers)
    print(response.json())


def chat_amigo(token: str) -> None:
    amigos = obtener_amigos(token)
    if not amigos:
        print("No tienes amigos para chatear.")
        return

    print("\n--- Lista de amigos ---")
    for i, amigo in enumerate(amigos):
        print(f"{i + 1}. {amigo}")

    idx = solicitar_parametro("Selecciona el número del amigo",int) - 1
    if idx < 0 or idx >= len(amigos):
        print("Selección inválida.")
        return

    amigo_username = amigos[idx]

    url_historial = f"{BASE_URL}/amigos/{amigo_username}/chat"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url_historial, headers=headers)
    mensajes = response.json()

    print("\n--- Historial de chat ---")
    for msg in mensajes:
        print(f"[{msg['timestamp']}] {msg['emisor']} -> {msg['contenido']}")

    while True:
        nuevo = solicitar_parametro("Escribe un mensaje (o no escribas nada para terminar) ",str)
        copia = nuevo
        if copia.lower().strip() == "":
            break
        url_mensaje = f"{BASE_URL}/amigos/{amigo_username}/mensaje"
        data = {"contenido": nuevo}
        resp = requests.post(url_mensaje, json=data, headers=headers)
        print(resp.json())


def obtener_amigos(token: str) -> list:
    url = f"{BASE_URL}/amigos"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    amigos = data.get("amigos", [])

    return amigos


def obtener_solicitudes(token: str) -> list:
    url = f"{BASE_URL}/amigos/solicitudes"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data.get("solicitudes", [])


def menu_retos(token):
    while True:
        print("\n--- Menú de Retos ---")
        print("1. Ver retos")
        print("2. Enviar reto a amigo")
        print("3. Aceptar reto")
        print("4. Rechazar reto")
        print("5. Volver al menú principal")

        opcion = solicitar_parametro("Elige una opción",str)

        if opcion == "1":
            ver_retos(token)
        elif opcion == "2":
            enviar_reto(token)
        elif opcion == "3":
            aceptar_reto(token)
        elif opcion == "4":
            rechazar_reto(token)
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")


def ver_retos(token):
    response = requests.get(f"{BASE_URL}/retos", headers={"Authorization": f"Bearer {token}"})
    if response.ok:
        retos = response.json()["retos"]
        if retos:
            print("\nRetos recibidos:")
            for i, reto in enumerate(retos):
                print(f"{i + 1}. De: {reto['retador']}")
        else:
            print("No tienes retos pendientes.")
    else:
        print("Error al obtener los retos:", response.json().get("error", "Error desconocido"))


def enviar_reto(token):

    amigos = obtener_amigos(token)

    if not amigos:
        print("No tienes amigos disponibles para retar.")
        return

    print("\nAmigos disponibles:")
    for i, amigo in enumerate(amigos):
        print(f"{i + 1}. {amigo}")

    idx = solicitar_parametro("Selecciona el número del amigo a retar",int) - 1
    if idx < 0 or idx >= len(amigos):
        print("Selección inválida.")
        return

    username_amigo = amigos[idx]

    resp = requests.post(f"{BASE_URL}/retos/enviar/{username_amigo}", headers={"Authorization": f"Bearer {token}"})
    print(resp.json().get("mensaje", resp.json().get("error", "Error desconocido")))


def aceptar_reto(token):
    retos_resp = requests.get(f"{BASE_URL}/retos", headers={"Authorization": f"Bearer {token}"})
    if not retos_resp.ok:
        print("Error al obtener los retos.")
        return

    retos = retos_resp.json().get("retos", [])
    if not retos:
        print("No tienes retos pendientes.")
        return

    print("\nRetos disponibles:")
    for i, reto in enumerate(retos):
        print(f"{i + 1}. De: {reto['retador']}")

    idx = solicitar_parametro("Selecciona el número del reto a aceptar",int) - 1
    if idx < 0 or idx >= len(retos):
        print("Selección inválida.")
        return

    retador_username = retos[idx]["retador"]

    resp = requests.post(f"{BASE_URL}/retos/aceptar/{retador_username}", headers={"Authorization": f"Bearer {token}"})
    print(resp.ok)

    datos = resp.json()
    print(datos.get("mensaje",datos.get("error", "Error desconocido")))


def rechazar_reto(token):
    retos_resp = requests.get(f"{BASE_URL}/retos", headers={"Authorization": f"Bearer {token}"})
    if not retos_resp.ok:
        print("Error al obtener los retos.")
        return

    retos = retos_resp.json().get("retos", [])
    if not retos:
        print("No tienes retos pendientes.")
        return

    print("\nRetos disponibles:")
    for i, reto in enumerate(retos):
        print(f"{i + 1}. De: {reto['retador']}")

    idx = solicitar_parametro("Selecciona el número del reto a rechazar",int) - 1
    if idx < 0 or idx >= len(retos):
        print("Selección inválida.")
        return

    retador_username = retos[idx]["retador"]

    resp = requests.post(f"{BASE_URL}/retos/rechazar/{retador_username}", headers={"Authorization": f"Bearer {token}"})
    datos = resp.json()
    print(datos.get("mensaje",datos.get("error", "Error desconocido")))

def menu_partidas(token: str) -> None:
    """
    Menú de interacción con partidas activas e historial.
    Permite ver historial, ver una partida (reproduce), ver estado y jugar turno.
    """
    while True:
        print("\n--- MENÚ PARTIDAS ---")
        print("1. Mostrar historial de partidas")
        print("2. Ver una partida")
        print("3. Ver estado de una partida activa")
        print("4. Jugar un turno en una partida activa")
        print("5. Rendirse de una partida")
        print("6. Volver al menú principal")

        opcion = solicitar_parametro("Selecciona una opción",str)

        if opcion == "1":
            mostrar_historial(token)
        elif opcion == "2":
            ver_una_partida(token)
        elif opcion == "3":
            ver_estado_partida(token)
        elif opcion == "4":
            jugar_turno(token)
        elif opcion == "5":
            rendirse(token)
        elif opcion == "6":
            break
        else:
            print("Opción inválida. Intenta de nuevo.")


def obtener_partidas_activas(token: str) -> list[dict]:
    url = f"{BASE_URL}/partidas/activas"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def mostrar_historial(token: str) -> None:
    url = f"{BASE_URL}/partidas"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(response.json())


def ver_una_partida(token: str) -> None:
    partidas_activas = obtener_partidas_activas(token)

    url_historial = f"{BASE_URL}/partidas"
    headers = {"Authorization": f"Bearer {token}"}
    response_historial = requests.get(url_historial, headers=headers)
    historial = response_historial.json() if response_historial.ok else []

    partidas_totales = []

    print("\n--- Partidas activas ---")
    for i, partida in enumerate(partidas_activas):
        print(f"{i+1}: Contra {partida['oponente']} | Turno: {partida['turno']} [ACTIVA]")
        partidas_totales.append(partida['sesion_id'])

    offset = len(partidas_activas)
    print("\n--- Partidas finalizadas ---")
    for j, nombre_archivo in enumerate(historial):
        print(f"{offset + j+1}: Archivo: {nombre_archivo} [TERMINADA]")
        partidas_totales.append(nombre_archivo)

    if not partidas_totales:
        print("No tienes partidas para visualizar.")
        return

    indice = solicitar_parametro("Selecciona el número de la partida que quieres ver",int)-1
    if 0 <= indice < len(partidas_totales):
        sesion_id = partidas_totales[indice]
        url = f"{BASE_URL}/partidas/{sesion_id}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        datos = response.json()

        if 'error' in datos:
            print(datos['error'])
        else:
            reproducir_partida(datos,sesion_id)
    else:
        print("Selección inválida.")



def ver_estado_partida(token: str) -> None:
    partidas = obtener_partidas_activas(token)
    if not partidas:
        print("No tienes partidas activas.")
        return

    print("\n--- Partidas activas ---")
    for i, partida in enumerate(partidas):
        print(f"{i+1}: Contra {partida['oponente']} | Turno: {partida['turno']}")

    indice = solicitar_parametro("Selecciona el número de la partida para ver su estado",int)-1
    if 0 <= indice < len(partidas):
        sesion_id = partidas[indice]['sesion_id']
        url = f"{BASE_URL}/partidas/{sesion_id}/estado"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        datos = response.json()

        if 'error' in datos:
            print(datos['error'])
        else:
            print(f"\nTurno: {datos['turno_actual']}")
            print(f"Estado: {datos['estado']}")
            print("Tablero:\n")
            for fila in  datos["tablero"]:
                print(fila)
    else:
        print("Selección inválida.")


def jugar_turno(token: str) -> None:
    partidas = obtener_partidas_activas(token)
    if not partidas:
        print("No tienes partidas activas.")
        return

    print("\n--- Partidas activas ---")
    for i, partida in enumerate(partidas):
        print(f"{i+1}: Contra {partida['oponente']} | Turno: {partida['turno']}")

    indice = solicitar_parametro("Selecciona el número de la partida para jugar tu turno",int)-1
    if 0 <= indice < len(partidas):
        sesion_id = partidas[indice]['sesion_id']
        origen = solicitar_parametro("Posición de origen (ej: e2)",str).split()
        destino = solicitar_parametro("Posición de destino (ej: e4)",str).split()
        promocion = input("\nPromoción (dama, torre, alfil, caballo) o deja vacío: ")
        datos: Dict[str, Any] = {
            "origen": [int(origen[0]), int(origen[1])],
            "destino": [int(destino[0]), int(destino[1])]
        }

        if promocion:
            datos["promocion"] = promocion.lower()

        url = f"{BASE_URL}/partidas/{sesion_id}/mover"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(url, json=datos, headers=headers)
        resultado = response.json()

        if 'error' in resultado:
            print(resultado['error'])
        else:
            print("Resultado del turno:")
            if 'jugador' in resultado:
                print("Tu movimiento:")
                print(resultado["jugador"].get("tablero", ""))
            else:
                print(resultado.get("tablero", ""))

            if 'ia' in resultado:
                print("\nMovimiento de la IA:")
                print(resultado["ia"].get("tablero", ""))
    else:
        print("Selección inválida.")


def rendirse(token: str) -> None:
    partidas = obtener_partidas_activas(token)
    if not partidas:
        print("No tienes partidas activas.")
        return

    print("\n--- Partidas activas ---")
    for i, partida in enumerate(partidas):
        print(f"{i+1}: Contra {partida['oponente']} | Turno: {partida['turno']}")

    indice = solicitar_parametro("Selecciona el número de la partida para jugar tu turno")-1
    if 0 <= indice < len(partidas):
        sesion_id = partidas[indice]['sesion_id']
        datos: Dict[str, bool] = {
            "abandono": True,
        }

        url = f"{BASE_URL}/partidas/{sesion_id}/mover"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(url, json=datos, headers=headers)
        resultado = response.json()

        if 'error' in resultado:
            print(resultado['error'])
        else:
            print("Resultado del turno:")
            if 'jugador' in resultado:
                print("Tu movimiento:")
                print(resultado["jugador"].get("tablero", ""))
            else:
                print(resultado.get("tablero", ""))

            if 'ia' in resultado:
                print("\nMovimiento de la IA:")
                print(resultado["ia"].get("tablero", ""))
    else:
        print("Selección inválida.")



def crear_tablero_vacio() -> List[List[Optional[str]]]:
    """Crea un tablero 8x8 vacío."""
    return [["." for _ in range(8)] for _ in range(8)]


def imprimir_tablero(tablero: List[List[str]]) -> None:
    """Imprime el tablero de forma legible con letras de columna y números de fila."""
    print("\n  a b c d e f g h")
    for i in range(8):
        fila = tablero[i]
        print(f"{8 - i} " + " ".join(fila)+f"{8 - i}")
    print("\n  a b c d e f g h")
    print()


def mover_pieza_en_tablero(tablero: List[List[str]], origen: Tuple[int, int], destino: Tuple[int, int], pieza: str, color: str) -> None:
    """Mueve una pieza de origen a destino en el tablero simulado."""
    simbolo = obtener_simbolo_unicode(pieza, color)
    fila_origen, col_origen = origen
    fila_destino, col_destino = destino
    tablero[fila_origen][col_origen] = "."
    tablero[fila_destino][col_destino] = simbolo


def obtener_simbolo_unicode(pieza: str, color: str) -> str:
    """Devuelve el símbolo Unicode correspondiente a la pieza."""
    unicode_blancas = {
        "Rey": "♔",
        "Reina": "♕",
        "Torre": "♖",
        "Alfil": "♗",
        "Caballo": "♘",
        "Peon": "♙"
    }
    unicode_negras = {
        "Rey": "♚",
        "Reina": "♛",
        "Torre": "♜",
        "Alfil": "♝",
        "Caballo": "♞",
        "Peon": "♟"
    }
    return unicode_blancas.get(pieza, "?") if color == "blanco" else unicode_negras.get(pieza, "?")


def reproducir_partida(datos: Dict[str, Any], nombre_archivo: str, velocidad: float = 1.0) -> None:
    """
    Reproduce una partida guardada paso a paso usando símbolos de piezas Unicode.
    """
    movimientos = datos["movimientos"]

    print(f"\nReproduciendo partida: {nombre_archivo}")
    print(f"{datos['jugador_blanco']['username']} (Blancas) vs {datos['jugador_negro']['username']} (Negras)")
    print(f"Ganador: {datos['ganador']}\n")

    tablero = crear_tablero_vacio()

    for idx, mov in enumerate(movimientos):
        origen = tuple(mov["origen"])
        destino = tuple(mov["destino"])
        pieza = mov["pieza"]
        color = mov["color"]
        captura = mov["captura"]

        print(f"Turno {idx + 1}: {color} mueve {pieza} de {origen} a {destino}", end="")
        if captura:
            print(f" capturando {captura}")
        else:
            print()

        mover_pieza_en_tablero(tablero, origen, destino, pieza, color)
        imprimir_tablero(tablero)
        time.sleep(velocidad)

    print("\n=== Fin de la reproducción ===")


def menu_principal(token: str) -> None:

    global usuario_username,usuario_id

    while True:
        print("\n--- Menú Principal ---")
        print("1. Menú Amigos")
        print("2. Menú Retos")
        print("3. Menú Partidas")
        print("4. Ver mi perfil")
        print("5. Ranking")
        print("6. Posición de un usuario")
        print("7. Salir")

        opcion = solicitar_parametro("Selecciona una opción",str)

        if opcion == "1":
            menu_amigos(token)
        elif opcion == "2":
            menu_retos(token)
        elif opcion == "3":
            menu_partidas(token)
        elif opcion == "4":
            ver_perfil(token,usuario_username)
        elif opcion == "5":
            ranking()
        elif opcion == "6":
            obtener_posicion_usuario()
        elif opcion == "7":
            salir(token)
            token = True
            usuario_username = None
            usuario_id = None
            print("\nHas salido de la sesión.")
            break
        else:
            print("\nOpción inválida.")


def ranking():  
    try:
        top_n = solicitar_parametro("Top a solicitar ", int) or 10
    except ValueError:
        top_n = 10

    response = requests.get(f"{BASE_URL}/ranking", params={"top_n": top_n})
    datos = response.json()

    if response.status_code == 200:
        print("\n--- Ranking ---")
        for i, jugador in enumerate(datos, start=1):
            print(f"{i}. {jugador['username']} (ELO: {jugador['elo']})")
    else:
        print(f"Error: {datos.get('error', 'Error al obtener el ranking.')}")


def obtener_posicion_usuario() -> None:
    username = solicitar_parametro("Nombre de usuario", str, lon_min=3)
    url = f"{BASE_URL}/ranking/posicion/{username}"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            datos = r.json()
            print(f"\nUsuario {datos['username']} está en la posición {datos['posicion']} del ranking.")
        else:
            print("Error:", r.json().get("error", r.text))
    except Exception as e:
        print("Error:", e)


def salir(token: str) -> None:
    url = f"{BASE_URL}/salir"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.post(url, headers=headers)
        datos = r.json()
        print(datos.get("msg", datos))
    except Exception as e:
        print("Error:", e)


def ver_perfil(token: str,usuario_username:str) -> None:
    """
    Muestra el perfil del usuario (usando el endpoint perfil amigo).
    """
    url = f"{BASE_URL}/amigos/perfil/{usuario_username}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            datos = r.json().get("perfil")
            
            print("\n=== Perfil del Usuario ===")
            print(f"Nombre de usuario : {datos["username"]}")
            print(f"Puntos ELO        : {datos["elo"]}")
            print(f"Partidas jugadas  : {datos["partidas_jugadas"]}")
        else:
            print("Error al obtener perfil:", r.json().get("error", r.text))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":

    token:Union[str,bool] = True

    while token:
        token = menu_registro()
        if token:
            menu_principal(token)