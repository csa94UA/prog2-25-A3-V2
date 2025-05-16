import json
import os.path
from random import randint
from typing import Optional

import requests
from Base_de_datos.operacoines_pandas import load_en_curso
from Partidas.Partida import partida
from Jugador import Jugador
from Partidas.ver_partida import visualizar_partida_antigua

URL = 'http://127.0.0.1:5000/'
DIR_DATOS = "Base_de_datos/datos/"

def mostrar_menu() -> None:
    print("\t-----------Yorkshire Chess-----------")
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Ver perfil")
    print("4. Modificar perfil")
    print("5. Eliminar perfil")
    print("6. Crear partida")
    print("7. Cargar partida")
    print("8. Ver partida")
    print("9. Eliminar partida")
    print("10. Mirar documentación del juego (muy recomendado)")
    print("11. Salir")

    return None

def crear_partida(token : str, cargar = False) -> None:
    bot : bool = False

    jug1_nombre = input("Digite su nombre jugador 1: ")
    jug1_contraseña = input("Digite su contraseña jugador 1: ")
    if verificar_usuario(jug1_nombre, jug1_contraseña):
        print("Credenciales invalidas")
        return None

    opcion : str = input("Desea jugar contra la IA? (S/N) ")
    if opcion.isalpha() and opcion.upper() == 'S':
        jug2_nombre : str = "StockFish"
        bot = True
    else:
        jug2_nombre = input("Digite su nombre jugador 2: ")
        jug2_contraseña = input("Digite su contraseña jugador 2: ")
        if verificar_usuario(jug2_nombre, jug2_contraseña):
            print("Credenciales invalidas")
            return None

    # Crear objetos Jugador
    jugador1 = Jugador(jug1_nombre, 0)
    jugador2 = Jugador(jug2_nombre, 0)

    if not cargar:
        if randint(0, 1000) < 499:
            jugador1.color = 1
            jugador2.color = 0
        else:
            jugador1.color = 0
            jugador2.color = 1
        print("Malo de la peli: ",jugador2.nombre)
        respuesta = requests.post(f'{URL}/partida?contrincante={jugador2.nombre}&color={jugador1.color}',
                                  headers= {'Authorization': 'Bearer ' + (token if token else '')})
        print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
        if respuesta.status_code == 200:
            partida(jugador1, jugador2, bot)
    else:
        pd = load_en_curso()

        game_id_1 = f'{jug1_nombre}vs{jug2_nombre}'
        game_id_2 = f'{jug2_nombre}vs{jug1_nombre}'

        if game_id_1 in pd["game_id"].astype(str).values:
            jugador1.color = 1
            jugador2.color = 0
            partida(jugador1, jugador2, bot, en_curso=True)

        elif game_id_2 in pd["game_id"].astype(str).values:
            jugador1.color = 0
            jugador2.color = 1
            partida(jugador2, jugador1, bot, en_curso=True)

    return None

def ver_partida(token : str) -> None:
    partidas = mostrar_partidas(token)

    if partidas is None:
        return None

    while True:
        try:
            opcion = int(input("Digite el número de la partida que desea ver: "))

            if not (-1 < opcion <= len(partidas)):
                print("Opcion incorrecta")
                continue

        except ValueError:
            print("No has digitado un número")
            continue
        except TypeError:
            print("No has digitado un número")
            continue

        break

    if opcion == 0:
        return None

    game_id = partidas[opcion - 1]['nombre_partida']

    respuesta = requests.get(f'{URL}/partida/json?id={game_id}', headers={'Authorization': 'Bearer ' + (token if token else '')})
    print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
    if respuesta.status_code != 200:
        return None

    visualizar_partida_antigua(game_id)

    return None

def eliminar_partida(token : str) -> None:
    partidas = mostrar_partidas(token)

    if partidas is None:
        return None

    while True:
        try:
            opcion = int(input("Digite el número de la partida que desea ver: "))

            if not (-1 < opcion <= len(partidas)):
                print("Opcion incorrecta")
                continue

        except ValueError:
            print("No has digitado un número")
            continue
        except TypeError:
            print("No has digitado un número")
            continue

        break

    if opcion == 0:
        return None

    game_id = partidas[opcion - 1]['nombre_partida']

    respuesta = requests.delete(f'{URL}/partida?id={game_id}',headers={'Authorization': 'Bearer ' + (token if token else '')})
    print(f"Estado: {respuesta.status_code}.  {respuesta.text}")

    return None

def mostrar_partidas(token : str) -> list[dict] | None:
    respuesta = requests.get(f'{URL}/partida', headers={'Authorization': 'Bearer ' + (token if token else '')})
    if respuesta.status_code != 200:
        print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
        return None

    partidas = json.loads(respuesta.text)

    print("Se han encontrado las siguientes partidas: \n")
    print("0. Salir")
    for i, partida in enumerate(partidas):
        print(f"{i + 1}. Partida: {partida['nombre_partida']}")

    return partidas

def verificar_usuario(usuario : str, contraseña : str) -> bool:
    respuesta = requests.get(f"{URL}/login?user={usuario}&password={contraseña}")
    return False if respuesta.status_code == 200 else True

def mostrar_documentacion_juego() -> None:
    
    with open('tutorial.txt', 'r') as tutorial:
        for linea in tutorial:
            print(linea)
    
    return None

def menu() -> None:
    token : str = ''

    while True:
        mostrar_menu()
        opcion = input("¿Qué opción desea? ")
        if opcion.isdigit() and 0 < int(opcion) < 12:
            opcion = int(opcion)
        else:
            print("No has digitado una opción correcta.")
            continue

        match opcion:
            case 1:
                usuario: str = input("Ingrese el nombre de usuario: ")
                correo: str = input(f"Ingrese su correo electronico {usuario}: ")
                pais: str = input("¿De qué país eres?: ")
                contraseña: str = input("Ingrese la contraseña: ")
                respuesta = requests.post(f"{URL}/signup?user={usuario}&password={contraseña}&email={correo}&pais={pais}")
                print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
            case 2:
                usuario = input("Ingrese el nombre de usuario: ")
                contraseña = input("Ingrese la contraseña: ")
                respuesta = requests.get(f"{URL}/login?user={usuario}&password={contraseña}")
                print(f"Estado: {respuesta.status_code}.  {respuesta.text if respuesta.status_code != 200 else ''}")
                token = respuesta.json()['access token'] if respuesta.status_code == 200 else None
            case 3:
                respuesta = requests.get(f"{URL}/perfil", headers= {'Authorization': 'Bearer ' + (token if token else '')})
                print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
            case 4:
                campo = input("¿Qué campo quieres modificar? (contraseña, pais, correo): ")
                valor = input("¿Que nuevo valor quieres añadir?: ")
                respuesta = requests.put(f"{URL}/perfil?campo={campo}&valor={valor}", headers= {'Authorization': 'Bearer ' + (token if token else '')})
                print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
            case 5:
                contraseña = input("Digite su contraseña para confirmar: ")
                respuesta = requests.delete(f"{URL}/perfil?password={contraseña}", headers= {'Authorization': 'Bearer ' + (token if token else '')})
                print(f"Estado: {respuesta.status_code}.  {respuesta.text}")
            case 6:
                crear_partida(token)
            case 7:
                crear_partida(token,True)
            case 8:
                ver_partida(token)
            case 9:
                eliminar_partida(token)
            case 10:
                mostrar_documentacion_juego()
            case _:
                print("Saliendo")
                break

    return  None

if __name__ == '__main__':
    menu()