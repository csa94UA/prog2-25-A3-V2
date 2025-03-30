from crypt import methods
import requests

r = requests.get('http://127.0.0.1:5000')
print(r)
print(r.status_code)
print(r.text)

r = requests.get('http://127.0.0.1:5000/data')
print(r.status_code)
print(r.text)

URL = 'http://127.0.0.1:5000/'
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