from crypt import methods
import requests

URL = 'http://127.0.0.1:5000/'

r = requests.get('http://127.0.0.1:5000')
print(r)
print(r.status_code)
print(r.text)

r = requests.get('http://127.0.0.1:5000/data')
print(r.status_code)
print(r.text)

r = requests.post(f"{URL}/data/dato1?value=valor1")
print(r.status_code)
print(r.text)
print()

r = requests.get(f'{URL}/data/dato1')
print(r.status_code)
print(r.text)
print()

valorN = 123
r = requests.put(f'{URL}/data/dato1?value=valorN')
print(r.status_code)
print(r.text)
print()

r = requests.get(f'{URL}/data/dato1')
print(r.status_code)
print(r.text)
print()

r = requests.delete(f'{URL}/data/dato1')
print(r.status_code)
print(r.text)
print()

r = requests.post(f"{URL}/singup?user=usuario&password=contraseña")
print(r.status_code)
print(r.text)
print()

def mostrar_menu() -> None:
    print("\t-----------Yorkshire Chess-----------")
    print("1. Crear partida")
    print("2. Acceder a información del código")
    print("3. Acceder elemntos de la API")

    return None

def crear_partida() -> None:


    return None

def acceder_metodos_y_clases() -> None:


    return None

def acceder_elementos_api() -> None:


    return None

