import requests
from Partidas import partida
from Jugador import Jugador

URL = 'http://127.0.0.1:5000/'

def mostrar_menu() -> None:
    print("\t-----------Yorkshire Chess-----------")
    print("1. Crear partida")
    print("2. Documentación acerca del juego (muy remomendado)")
    print("3. Acceder elemntos de la API (registrarse, acceder a información, etc)")
    print("4. Salir")

    return None

def crear_partida() -> None:
    bot : bool = False

    jug1_nombre = input("Digite su nombre jugador 1: ")
    jug1_contraseña = input("Digite su contraseña jugador 1: ")
    if verificar_usuario(jug1_nombre, jug1_contraseña):
        print("Credenciales invalidas")
        return None

    opcion : str = input("Desea jugar contra la IA? (S/N)")
    if opcion.isalpha() and opcion.upper() in ['S','N']:
        jug2_nombre : str = "StockFish"
        bot = True
    else:
        jug2_nombre = input("Digite su nombre jugador 2: ")
        jug2_contraseña = input("Digite su contraseña jugador 2: ")
        if verificar_usuario(jug2_nombre, jug2_contraseña):
            print("Credenciales invalidas")
            return None

    # Crear objetos Jugador (aquí puedes complementar con otros atributos si los necesitas)
    jugador1 = Jugador(jug1_nombre, 0)
    jugador2 = Jugador(jug2_nombre, 0)

    # Iniciar la partida usando la función 'partida' existente
    print("Iniciando partida...")
    partida(jugador1, jugador2, bot)

    return None

def verificar_usuario(usuario : str, contraseña : str) -> bool:
    respuesta = requests.get(f"{URL}/login?user={usuario}&password={contraseña}")
    return False if respuesta.status_code == 200 else True

def mostrar_documentacion_juego() -> None:
    
    with open('tutorial.txt', 'r') as tutorial:
        for linea in tutorial:
            print(linea)
    
    return None

def acceder_elementos_api() -> None:
    while True:
        print("\n------------Menú de API-----------")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Listar de datos registrados")
        print("4. Agregar dato")
        print("5. Consultar un dato")
        print("6. Actualizar los datos")
        print("7. Eliminar un dato")
        print("8. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
        
        if opcion.isdigit() and 0 < int(opcion) < 9:
            opcion = int(opcion)
        else:
            print("Opción incorrecta o invalida")
            continue

        match opcion:
            case 1:
                usuario = input("Ingrese el nombre de usuario: ")
                contraseña = input("Ingrese la contraseña: ")
                respuesta = requests.post(f"{URL}/signup?user={usuario}&password={contraseña}")
                print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
            case 2:
                usuario = input("Ingrese el nombre de usuario: ")
                contraseña = input("Ingrese la contraseña: ")
                respuesta = requests.get(f"{URL}/login?user={usuario}&password={contraseña}")
                print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
            case 3:
                respuesta = requests.get(f"{URL}/data")
                print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
            case 4:
                id_dato = input("Ingrese el ID para el dato a agregar: ")
                valor = input("Ingrese el valor: ")
                respuesta = requests.post(f"{URL}/data/{id_dato}?value={valor}")
                print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
            case 5:
                id_dato = input("Ingrese el ID del dato a consultar: ")
                respuesta = requests.get(f"{URL}/data/{id_dato}")
                print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
            case 6:
                id_dato = input("Ingrese el ID del dato a actualizar: ")
                valor = input("Ingrese el nuevo valor: ")
                respuesta = requests.put(f"{URL}/data/{id_dato}?value={valor}")
                print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
            case 7:
                id_dato = input("Ingrese el ID del dato a eliminar: ")
                respuesta = requests.delete(f"{URL}/data/{id_dato}")
                print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
            case 8:
                print("Volviendo al menú principal.")
                break
            case _:
                print("Opción incorrecta o invalida")

    return None

def menu() -> None:
    while True:
        mostrar_menu()
        opcion = input("¿Qué opción desea? ")
        if opcion.isdigit() and 0 < int(opcion) < 5:
            opcion = int(opcion)
        else:
            print("No has digitado una opción correcta.")
            continue

        match opcion:
            case 1:
                crear_partida()
            case 2:
                mostrar_documentacion_juego()
            case 3:
                acceder_elementos_api()
            case _:
                print("Saliendo...")
                break

    return  None

if __name__ == '__main__':
    menu()