from flask import Flask, render_template

# Creamos una instancia de la aplicación Flask.
app = Flask(__name__)

# Definimos la ruta principal de la aplicación que se ejecuta al acceder a la URL raíz ('/').
@app.route("/")
@app.route("/base")
def base():
    # Renderizamos el template HTML y pasamos la lista weather_data como contexto.
    return render_template("base.html")



@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/recuperacion")
def recuperacion():
    return render_template("recuperacion.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)