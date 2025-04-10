from crypt import methods
import requests
import hashlib
from Partida import partida
from Jugador import Jugador
from main import users, data

URL = 'http://127.0.0.1:5000/'

def mostrar_menu() -> None:
    print("\t-----------Yorkshire Chess-----------")
    print("1. Crear partida")
    print("2. Acceder a información del código")
    print("3. Documentación acerca del juego (muy remomendado)")
    print("4. Acceder elemntos de la API (registrarse, acceder a información, etc)")
    print("5. Salir")

    return None

def crear_partida() -> None:
    
    if len(users.keys()) < 2:
        print("No hay suficientes usuarios registrados como para iniciar una partida (aun no esta implementado JcE)")
        return

    print("Usuarios registrados:")
    for usuario in users.keys():
        print(f"- {usuario}")
        
    jug1_nombre = input("Digite su nombre jugador 1: ")
    jug1_contraseña = input("Digite su contraseña jugador 1: ")
    descodificado = hashlib.sha256(jug1_contraseña.encode()).hexdigest()
    if jug1_nombre not in users and descodificado != users[jug1_nombre]:
        print("Credenciales invalidas")
        return None

    jug2_nombre = input("Digite su nombre jugador 2: ")
    jug2_contraseña = input("Digite su contraseña jugador 2: ")
    descodificado = hashlib.sha256(jug2_contraseña.encode()).hexdigest()
    if jug2_nombre not in users and descodificado != users[jug2_nombre]:
        print("Credenciales invalidas")
        return None

    # Crear objetos Jugador (aquí puedes complementar con otros atributos si los necesitas)
    jugador1 = Jugador(jug1_nombre, 0)
    jugador2 = Jugador(jug2_nombre, 0)

    # Iniciar la partida usando la función 'partida' existente
    print("Iniciando partida...")
    partida(jugador1, jugador2)

    return None

def acceder_metodos_y_clases() -> None:


    return None

def mostrar_documentacion_juego() -> None:
    
    with open('tutorial.txt', 'r') as tutorial:
        for linea in tutorial:
            print(linea)
    
    return None

def acceder_elementos_api() -> None:
    while True:
        print("\n=== Menú de API ===")
        print("1. Registrar usuario (signup)")
        print("2. Iniciar sesión (login)")
        print("3. Listar datos")
        print("4. Agregar dato")
        print("5. Consultar dato")
        print("6. Actualizar dato")
        print("7. Eliminar dato")
        print("8. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()
        
        if opcion.isdigit() and 0 < int(opcion) < 9:
            opcion = int(opcion)
        else:
            print("Opción inválida. Intente nuevamente.")
            continue

        match opcion:
            case 1:
                usuario = input("Ingrese el nombre de usuario: ").strip()
                contraseña = input("Ingrese la contraseña: ").strip()
                resp = requests.post(f"{URL}/signup", params={"usuario": usuario, "contraseña": contraseña})
                print(f"[{resp.status_code}] {resp.text}")
            case 2:
                usuario = input("Ingrese el nombre de usuario: ").strip()
                contraseña = input("Ingrese la contraseña: ").strip()
                resp = requests.get(f"{URL}/login", params={"usuario": usuario, "contraseña": contraseña})
                print(f"[{resp.status_code}] {resp.text}")
            case 3:
                resp = requests.get(f"{URL}/data")
                print(f"[{resp.status_code}] {resp.text}")
            case 4:
                id_data = input("Ingrese el ID para el dato a agregar: ").strip()
                value = input("Ingrese el valor: ").strip()
                resp = requests.post(f"{URL}/data/{id_data}", params={"value": value})
                print(f"[{resp.status_code}] {resp.text}")
            case 5:
                id_data = input("Ingrese el ID del dato a consultar: ").strip()
                resp = requests.get(f"{URL}/data/{id_data}")
                print(f"[{resp.status_code}] {resp.text}")
            case 6:
                id_data = input("Ingrese el ID del dato a actualizar: ").strip()
                value = input("Ingrese el nuevo valor: ").strip()
                resp = requests.put(f"{URL}/data/{id_data}", params={"value": value})
                print(f"[{resp.status_code}] {resp.text}")
            case 7:
                id_data = input("Ingrese el ID del dato a eliminar: ").strip()
                resp = requests.delete(f"{URL}/data/{id_data}")
                print(f"[{resp.status_code}] {resp.text}")
            case 8:
                print("Volviendo al menú principal.")
                break
            case _:
                print("Opción inválida. Intente nuevamente.")

    return None

def menu() -> None:
    while True:
        mostrar_menu()
        opcion = input("¿Qué opción desea? ")
        if opcion.isdigit() and 0 < int(opcion) < 6:
            opcion = int(opcion)
        else:
            print("No has digitado una opción correcta.")
            continue

        match opcion:
            case 1:
                crear_partida()
            case 2:
                acceder_metodos_y_clases()
            case 3:
                mostrar_documentacion_juego()
            case 4:
                acceder_elementos_api()
            case _:
                print("Saliendo...")
                break

    return  None

if __name__ == '__main__':
    menu()