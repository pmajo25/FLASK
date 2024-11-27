"""
CRUD FLASK PYTHON + MYSQL
Desarrollado por: Valentina Zuñiga, Daily Rodriguez y María Paternina
"""

#Realizamos la importación de las librería flask requeridas
from flask import Flask, render_template, request, redirect, flash
#importamos el controlador
import controlador_juegos

#Iniciamos creando una aplicación flask
app = Flask(__name__)

#Ruta: /ruta principal /juego lista de juegos
@app.route("/")
@app.route("/juegos")
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

#Ruta: agregar_juego
@app.route("/agregar_juego")
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
def guardar_juego():
    #Recibe los datos del formulario
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precioCompra = request.form["PrecioCompra"]
    #Guarda datos en la base de datos ingresando a la función inserta_juego
    controlador_juegos.insertar_juego(nombre, descripcion, precioCompra)
    #De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/juegos")

@app.route("/juegos/<int:id>")
def detalles_juego(id):
    # Obtener los detalles del juego por ID
    juego = controlador_juegos.obtener_juego_por_id(id)
    return {
        "id": juego[0],
        "nombre": juego[1],
        "descripcion": juego[2],
        "PrecioCompra": juego[3]
    }

# Ruta: eliminar_juego
@app.route("/eliminar_juego", methods=["POST"])
def eliminar_juego():
    controlador_juegos.eliminar_juego(request.form["id"])
    return redirect("/juegos")

# Ruta: formulario_editar_juego
@app.route("/juegos/<int:id>")
def editar_juego(id):
    # Obtener el juego por ID
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("juegos.html", juego=juego)

# Ruta: actualizar_juego
@app.route("/actualizar_juego", methods=["POST"])
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    PrecioCompra = request.form["PrecioCompra"]
    controlador_juegos.actualizar_juego(nombre, descripcion, PrecioCompra, id)
    return redirect("/juegos")

# Iniciar el servidor para ejecutar la aplicación flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)