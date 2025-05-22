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
        print("""
╔════════════════════════════════════╗
║          MENÚ DE REGISTRO          ║
╠════════════════════════════════════╣
║ 1. Registrar usuario               ║
║ 2. Iniciar sesión                  ║
║ 3. Ver ranking                     ║
║ 4. Salir                           ║
╚════════════════════════════════════╝
        """)

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
                return datos["access_token"]
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
        print("""
╔════════════════════════════════════════════╗
║              MENÚ DE AMIGOS                ║
╠════════════════════════════════════════════╣
║ 1. Mostrar amigos                          ║
║ 2. Ver perfil de amigo                     ║
║ 3. Enviar solicitud de amistad             ║
║ 4. Ver solicitudes pendientes              ║
║ 5. Aceptar solicitud                       ║
║ 6. Eliminar amigo                          ║
║ 7. Chat con amigo                          ║
║ 8. Volver al menú principal                ║
╚════════════════════════════════════════════╝
        """)

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

    print("""
╔══════════════════════════════╗
║        LISTA DE AMIGOS       ║
╠══════════════════════════════╣
    """)

    for i, amigo in enumerate(amigos):
        print(f"  {i + 1}. {amigo}")

    print("╚══════════════════════════════╝")

def ver_perfil_amigo(token: str) -> None:
    amigos = obtener_amigos(token)
    if not amigos:
        print("No tienes amigos para ver su perfil.")
        return

    print("""
╔══════════════════════════════╗
║        LISTA DE AMIGOS       ║
╠══════════════════════════════╣
    """)

    for i, amigo in enumerate(amigos):
        print(f"  {i + 1}. {amigo}")

    print("╚══════════════════════════════╝")
    idx = solicitar_parametro("Selecciona el número del amigo",int) - 1
    if idx < 0 or idx >= len(amigos):
        print("Selección inválida.")
        return

    username = amigos[idx]
    url = f"{BASE_URL}/amigos/perfil/{username}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    datos = response.json().get("perfil")
    print("""
╔════════════════════════════════╗
║        PERFIL DEL USUARIO      ║
╠════════════════════════════════╣
    """)
    print(f"  Nombre de usuario : {datos['username']}")
    print(f"  Puntos ELO        : {datos['elo']}")
    print(f"  Partidas jugadas  : {datos['partidas_jugadas']}")
    print("╚════════════════════════════════╝")


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

    print("""
╔════════════════════════════════╗
║      SOLICITUDES RECIBIDAS     ║
╠════════════════════════════════╣
    """)

    for i, s in enumerate(solicitudes):
        print(f"  {i + 1}. {s['remitente']}")

    print("╚════════════════════════════════╝")


def aceptar_solicitud(token: str) -> None:
    solicitudes = obtener_solicitudes(token)
    if not solicitudes:
        print("No tienes solicitudes para aceptar.")
        return

    print("""
╔════════════════════════════════╗
║      SOLICITUDES RECIBIDAS     ║
╠════════════════════════════════╣
    """)

    for i, s in enumerate(solicitudes):
        print(f"  {i + 1}. {s['remitente']}")

    print("╚════════════════════════════════╝")


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

    print("""
╔══════════════════════════════╗
║        LISTA DE AMIGOS       ║
╠══════════════════════════════╣
    """)

    for i, amigo in enumerate(amigos):
        print(f"  {i + 1}. {amigo}")

    print("╚══════════════════════════════╝")
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

    print("""
╔══════════════════════════════╗
║        LISTA DE AMIGOS       ║
╠══════════════════════════════╣
    """)

    for i, amigo in enumerate(amigos):
        print(f"  {i + 1}. {amigo}")

    print("╚══════════════════════════════╝")

    idx = solicitar_parametro("Selecciona el número del amigo",int) - 1
    if idx < 0 or idx >= len(amigos):
        print("Selección inválida.")
        return

    amigo_username = amigos[idx]

    url_historial = f"{BASE_URL}/amigos/{amigo_username}/chat"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url_historial, headers=headers)
    mensajes = response.json()

    print("""
╔════════════════════════════════════════════════════════╗
║                  HISTORIAL DE CHAT                     ║
╠════════════════════════════════════════════════════════╣
    """)

    for msg in mensajes:
        timestamp = msg['timestamp']
        emisor = msg['emisor']
        contenido = msg['contenido']
        print(f"[{timestamp}] {emisor:<15} → {contenido}")

    print("╚════════════════════════════════════════════════════════╝")


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
        print("""
╔══════════════════════════════════╗
║          MENÚ DE RETOS           ║
╠══════════════════════════════════╣
║ 1. Ver retos                     ║
║ 2. Enviar reto a amigo o IA      ║
║ 3. Aceptar reto                  ║
║ 4. Rechazar reto                 ║
║ 5. Volver al menú principal      ║
╚══════════════════════════════════╝
""")

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
            print("""
╔══════════════════════════════╗
║       RETOS RECIBIDOS        ║
╠══════════════════════════════╣
            """)

            for i, reto in enumerate(retos):
                print(f"  {i + 1}. De: {reto['retador']}")

            print("╚══════════════════════════════╝")

        else:
            print("No tienes retos pendientes.")
    else:
        print("Error al obtener los retos:", response.json().get("error", "Error desconocido"))


def enviar_reto(token):

    amigos = obtener_amigos(token)

    IAS_existentes = ["IAMohammed(1)", "IAJulio(2)", "IAVicente(3)","IASofia(4)", "IACarlos(5)"]

    if not amigos and not IAS_existentes:
        print("No tienes amigos disponibles para retar.")
        return

    opciones_disponibles = amigos + IAS_existentes

    print("""
╔════════════════════════════════════════════════╗
║      OPCIONES DISPONIBLES PARA RETAR           ║
╠════════════════════════════════════════════════╣
    """)

    for i, nombre in enumerate(opciones_disponibles):
        tipo = "IA" if nombre in IAS_existentes else "Amigo"
        print(f"  {i + 1}. {nombre:<20} ({tipo})")

    print("╚════════════════════════════════════════════════╝")

    idx = solicitar_parametro("Selecciona el número del jugador o IA a retar", int) - 1
    if idx < 0 or idx >= len(opciones_disponibles):
        print("Selección inválida.")
        return

    username_objetivo = opciones_disponibles[idx]

    resp = requests.post(f"{BASE_URL}/retos/enviar/{username_objetivo}", headers={"Authorization": f"Bearer {token}"})
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

    print("""
╔════════════════════════════════╗
║        RETOS DISPONIBLES       ║
╠════════════════════════════════╣
    """)

    for i, reto in enumerate(retos):
        print(f"  {i + 1}. De: {reto['retador']}")

    print("╚════════════════════════════════╝")


    idx = solicitar_parametro("Selecciona el número del reto a aceptar",int) - 1
    if idx < 0 or idx >= len(retos):
        print("Selección inválida.")
        return

    retador_username = retos[idx]["retador"]

    resp = requests.post(f"{BASE_URL}/retos/aceptar/{retador_username}", headers={"Authorization": f"Bearer {token}"})

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

    print("""
╔════════════════════════════════╗
║        RETOS DISPONIBLES       ║
╠════════════════════════════════╣
    """)

    for i, reto in enumerate(retos):
        print(f"  {i + 1}. De: {reto['retador']}")

    print("╚════════════════════════════════╝")


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
        print("""
╔════════════════════════════════════════════════════╗
║                 MENÚ DE PARTIDAS                   ║
╠════════════════════════════════════════════════════╣
║ 1. Mostrar historial de partidas                   ║
║ 2. Ver una partida                                 ║
║ 3. Ver estado de una partida activa                ║
║ 4. Jugar un turno en una partida activa            ║
║ 5. Rendirse de una partida                         ║
║ 6. Volver al menú principal                        ║
╚════════════════════════════════════════════════════╝
        """)

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
    """
    Muestra el historial de partidas finalizadas del usuario autenticado.
    
    Parámetros:
    -----------
    token : str
        Token JWT del usuario autenticado.
    """
    url = f"{BASE_URL}/partidas"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    usuario = data.get("usuario")
    partidas = data.get("partidas", [])

    print(f"\n╔══════════════════════════════════════════════════════════════════════════╗")
    print(f"║ Historial de {usuario:<60}║")                                                
    print(f"╠════╦════════════╦═══════════════════════╦════════════════╦═══════════════╣")
    print(f"║ No ║   Fecha    ║     Jugador Blanco    ║ Jugador Negro  ║ Ganador       ║")
    print(f"╠════╬════════════╬═══════════════════════╬════════════════╬═══════════════╣")
    
    if not partidas:
        print("║                       No hay partidas finalizadas.                       ║")
    else:
        for i, partida in enumerate(partidas, start=1):
            fecha = partida.get("fecha", "N/A")
            blanco = partida.get("jugador_blanco", "N/A")
            negro = partida.get("jugador_negro", "N/A")
            ganador = partida.get("ganador", "empate")

            print(f"║ {str(i)[:2]:<2} ║ {fecha[:10]:<10} ║ {blanco[:21]:<21} ║ {negro[:14]:<14} ║ {ganador[:13]:<13} ║")

    print(f"╚════╩════════════╩═══════════════════════╩════════════════╩═══════════════╝")




def ver_una_partida(token: str) -> None:
    url_historial = f"{BASE_URL}/partidas"
    headers = {"Authorization": f"Bearer {token}"}
    response_historial = requests.get(url_historial, headers=headers)
    historial = response_historial.json()["partidas"] if response_historial.ok else []
    if not historial:
        print("No tienes partidas finalizadas para visualizar.")
        return

    print("""
╔══════════════════════════════════════════════╗
║           PARTIDAS FINALIZADAS               ║
╠══════════════════════════════════════════════╣
    """)

    for j, nombre_archivo in enumerate(historial):
        print(f"  {j + 1}: Archivo: {nombre_archivo['nombre_archivo']} [TERMINADA]")

    print("╚══════════════════════════════════════════════╝")

    indice = solicitar_parametro("Selecciona el número de la partida que quieres ver", int) - 1
    if 0 <= indice < len(historial):
        nombre_archivo = historial[indice]
        print(f"Reproduciendo partida: {nombre_archivo['nombre_archivo']}")
        url = f"{BASE_URL}/partidas/{nombre_archivo['nombre_archivo']}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        print(response.text)
        datos = response.json()

        if 'error' in datos:
            print(datos['error'])
        elif "movimientos" in datos:
            reproducir_partida(datos, nombre_archivo)
        else:
            print("No se pudo reproducir la partida seleccionada.")
    else:
        print("Selección inválida.")



def ver_estado_partida(token: str) -> None:
    partidas = obtener_partidas_activas(token)
    if not partidas:
        print("No tienes partidas activas.")
        return

    print("""
╔═════════════════════════════════════════════════╗
║                PARTIDAS ACTIVAS                 ║
╠═════════════════════════════════════════════════╣
    """)

    for i, partida in enumerate(partidas):
        print(f"  {i + 1}: Contra {partida['oponente']:<15} | Turno: {partida['turno']} [ACTIVA]")

    print("╚═════════════════════════════════════════════════╝")
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
            print(datos["tablero"])

    else:
        print("Selección inválida.")


def jugar_turno(token: str) -> None:
    partidas = obtener_partidas_activas(token)
    if not partidas:
        print("No tienes partidas activas.")
        return

    print("""
╔═════════════════════════════════════════════════╗
║                PARTIDAS ACTIVAS                 ║
╠═════════════════════════════════════════════════╣
    """)

    for i, partida in enumerate(partidas):
        print(f"  {i + 1}: Contra {partida['oponente']:<15} | Turno: {partida['turno']} [ACTIVA]")

    print("╚═════════════════════════════════════════════════╝")

    indice = solicitar_parametro("Selecciona el número de la partida para jugar tu turno",int)-1
    if 0 <= indice < len(partidas):
        sesion_id = partidas[indice]['sesion_id']
        origen = solicitar_parametro("Posición de origen (ej: e2)",str).strip()
        destino = solicitar_parametro("Posición de destino (ej: e4)",str).strip()
        promocion = input("\nPromoción (dama, torre, alfil, caballo) o deja vacío: ")
        datos: Dict[str, Any] = {
            "origen": origen,
            "destino": destino
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

    print("""
╔═════════════════════════════════════════════════╗
║                PARTIDAS ACTIVAS                 ║
╠═════════════════════════════════════════════════╣
    """)

    for i, partida in enumerate(partidas):
        print(f"  {i + 1}: Contra {partida['oponente']:<15} | Turno: {partida['turno']} [ACTIVA]")

    print("╚═════════════════════════════════════════════════╝")
    indice = solicitar_parametro("Selecciona el número de la partida para jugar tu turno",int)-1
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


def colocar_piezas_iniciales_en_tablero(tablero: list[list[str]]) -> None:
    """Coloca las piezas de ajedrez en su posición inicial usando símbolos Unicode."""
    # Piezas blancas
    piezas_blancas = ["Torre", "Caballo", "Alfil", "Reina", "Rey", "Alfil", "Caballo", "Torre"]
    piezas_negras = ["Torre", "Caballo", "Alfil", "Reina", "Rey", "Alfil", "Caballo", "Torre"]

    # Fila 1 blancas
    for col, pieza in enumerate(piezas_blancas):
        tablero[7][col] = obtener_simbolo_unicode(pieza, "blanco")
    # Fila 2 blancas
    for col in range(8):
        tablero[6][col] = obtener_simbolo_unicode("Peon", "blanco")
    # Fila 7 negras
    for col in range(8):
        tablero[1][col] = obtener_simbolo_unicode("Peon", "negro")
    # Fila 8 negras
    for col, pieza in enumerate(piezas_negras):
        tablero[0][col] = obtener_simbolo_unicode(pieza, "negro")



def imprimir_tablero(tablero: List[List[str]]) -> None:
    print("\n    a   b   c   d   e   f   g   h")
    print("  ╔" + "═══╦" * 7 + "═══╗")

    for i in range(8):
        fila = tablero[i]
        fila_str = " ║ ".join(fila)
        print(f"{8 - i} ║ {fila_str} ║ {8 - i}")
        if i < 7:
            print("  ╠" + "═══╬" * 7 + "═══╣")
        else:
            print("  ╚" + "═══╩" * 7 + "═══╝")

    print("    a   b   c   d   e   f   g   h\n")



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
    colocar_piezas_iniciales_en_tablero(tablero)

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
        print("""
╔════════════════════════════════════════════════════════════════╗
║                     ╔═══════════════════╗                      ║
║                     ║  YORKSHIRE CHESS  ║                      ║
║                     ╚═══════════════════╝                      ║
╠════════════════════════════════════════════════════════════════╣
║                         MENÚ PRINCIPAL                         ║
╠════════════════════════════════════════════════════════════════╣
║ 1. Menú Amigos                                                 ║
║ 2. Menú Retos                                                  ║
║ 3. Menú Partidas                                               ║
║ 4. Ver mi perfil                                               ║
║ 5. Ranking                                                     ║
║ 6. Posición de un usuario                                      ║
║ 7. Salir                                                       ║
╚════════════════════════════════════════════════════════════════╝
        """)

        opcion = solicitar_parametro("Selecciona una opción",str)

        if opcion == "1":
            menu_amigos(token)
        elif opcion == "2":
            menu_retos(token)
        elif opcion == "3":
            menu_partidas(token)
        elif opcion == "4":
            ver_mi_perfil(token)
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
        print("""
╔════════════════════════════╗
║         RANKING            ║
╠════╦════════════════╦══════╣
║ Nº ║ Usuario        ║  ELO ║
╠════╬════════════════╬══════╣""")

        for i, jugador in enumerate(datos, start=1):
            print(f"║ {i:<2} ║ {jugador['username']:<14} ║ {jugador['elo']:<4} ║")

        print("╚════╩════════════════╩══════╝")

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


def ver_mi_perfil(token: str) -> None:
    """
    Muestra el perfil del usuario autenticado.
    """
    url = f"{BASE_URL}/perfil"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            datos = r.json().get("perfil")
            print("""
╔════════════════════════════════╗
║        MI PERFIL               ║
╠════════════════════════════════╣
            """)
            print(f"  Nombre de usuario : {datos['username']}")
            print(f"  Puntos ELO        : {datos['elo']}")
            print(f"  Partidas jugadas  : {datos['partidas_jugadas']}")
            print("╚════════════════════════════════╝")
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