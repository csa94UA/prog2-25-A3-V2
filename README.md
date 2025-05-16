# [Yorkshire Chess]
[//]: # (Incluid aquí la descripción de vuestra aplicación. Por cierto, así se ponen comentarios en Markdown)

## Autores

* (Coordinador) [Julio Alfonso De la Torre León](https://github.com/JulioAlfonsoUA)
* [Carlos Salas Alarcón](https://github.com/csa94UA)
* [Mohammed Alí Arshad Bhatti](https://github.com/MohammedAli-Biar)
* [Vicente Pérez Pourtau](https://github.com/vicenteprzz)
* [Sofía Pérez Vásquez](https://github.com/sofiaaperezz)

## Profesor
[//]: # (Dejad a quien corresponda)
[Miguel A. Teruel](https://github.com/materuel-ua) / [Cristina Cachero](https://github.com/ccacheroc)

## Requisitos
[//]: # (Indicad aquí los requisitos de vuestra aplicación, así como el alumno responsable de cada uno de ellos)
* Diseño y Programación del Juego [Sofía] 

  * Movimientos especiales como en pasant y enroque. 

  * Seleccionar Color 

* Compatibilidad con Base de Datos y Algoritmos [Julio] 

* Hosting y Base de Datos [Vicente] 

* Diseño de los Algoritmos [Mohammed Alí] 

* Entrenamiento y Optimización de Algoritmos [Carlos] 

* Sistema de Puntuación y de Clasificación (para Ranking y entrenamiento de IA) [Carlos] 

## Instrucciones de instalación y ejecución
[//]: # (Indicad aquí qué habría que hacer para ejecutar vuestra aplicación)

1. Clonar el repositorio en un directorio
```bash
git clone <repositorio>
cd <directorio>
```

2. Crear entorno virtual e instalar las librerías necesarias con el archivo requirements.txt
```bash
python3 -m venv <entonrno_virtual>
source venv/bin/activate
pip install -r requirements.txt
```
3. Ejecutar el servidor Flask
```bash
python main.py
```

4. Seguidamente ejecutamos el programa de pruebas
```
python examples.py
```

## Resumen de la API
[//]: # (Cuando tengáis la API, añadiréis aquí la descripción de las diferentes llamadas.)
[//]: # (Para la evaluación por pares, indicaréis aquí las diferentes opciones de vuestro menú textual, especificando para qué sirve cada una de ellas)
La API Flask ofrece funcionalidades para gestionar partidas de ajedrez, movimientos y autenticación de usuarios.

Rutas Principales

* POST /signup: Registro de usuarios.

* GET /login: Inicio de sesión y generación de tokens.

* GET /perfil: Muestra datos del perfil del usuario.

* PUT /perfil: Modificar perfil del usuario

* GET /data/: Obtener un dato por ID.

* PUT /data/: Actualizar un dato por ID.

* DELETE /data/: Eliminar un dato por ID.