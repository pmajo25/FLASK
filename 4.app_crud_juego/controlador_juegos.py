"""
CRUD FLASK PYTHON + MYSQL
Desarrollado por: Valentina Zuñiga, Daily Rodriguez y María Paternina
"""

#Realizamos la importación de nuestra función de conexion
from bd import obtener_conexion

#Controlador: insertar_juego
def insertar_juego(nombre, descripcion, precioCompra):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO juegos(nombre, descripcion, precioCompra) VALUES (%s, %s, %s)",
                       (nombre, descripcion, precioCompra))      
    conexion.commit()
    conexion.close()

#Controlador: obtener_juego
def obtener_juegos():
    conexion = obtener_conexion()
    juegos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, precioCompra FROM juegos")
        juegos = cursor.fetchall()
    conexion.close()
    return juegos    

# Controlador: obtener_juego_id
def obtener_juego_por_id(id):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, precioCompra FROM juegos WHERE id = %s", (id,)
        )
        juego = cursor.fetchone()
    conexion.close()
    return juego

# Controlador: actualizar_juego
def actualizar_juego(nombre, descripcion, precioCompra, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE juegos SET nombre = %s, descripcion = %s, precioCompra = %s WHERE id = %s",
            (nombre, descripcion, precioCompra, id),
        )
    conexion.commit()
    conexion.close()

# Controlador: eliminar_juego
def eliminar_juego(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM juegos WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()
        