from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import flash



# Creamos una instancia de la aplicación Flask.
app = Flask(__name__)
app.secret_key = "mi_clave_secreta_super_segura"  # Debe ser una clave única y secreta

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/prueba_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

# Definimos la ruta principal de la aplicación que se ejecuta al acceder a la URL raíz ('/').
@app.route("/")
@app.route("/index")
def index():
    # Renderizamos el template HTML y pasamos la lista weather_data como contexto.
    return render_template("index.html")

# Modelo User
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250))
    role = db.Column(db.String(20))
    def to_json(self):
        return {"id": self.id, "name": self.name, "email": self.email, "password": self.password, "role": self.role}

# Crear base de datos
with app.app_context():
    db.create_all()

# Rutas CRUD
@app.route('/users', methods=['GET'])
def get_users():
    users = Admin.query.all()
    return jsonify([user.to_json() for user in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = Admin(name=data['name'], email=data['email'], password=data['password'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_json()), 201



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Admin.query.filter_by(email=email).first()
        contrasena = Admin.query.filter_by(password=password).first()

        if user and contrasena:  # Aquí debes validar con una contraseña segura
            session['user_id'] = user.id
            session['role'] = user.role  # Guardamos el rol en la sesión

            if user.role == 'admin':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('base'))

        flash("Credenciales incorrectas", "danger")
    
    return render_template("login.html")



@app.route("/categoria")
def categoria():
    if "user_id" not in session:  # Si no hay usuario en sesión, redirige a login
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))
    return render_template("categoria.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:  # Si no hay usuario en sesión, redirige a login
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))

    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()  # Elimina todos los datos de la sesión
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for("login"))  # Redirige al login

@app.route("/recuperacion")
def recuperacion():
    return render_template("recuperacion.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/empleados")
def empleados():
    return render_template("empleados.html")

@app.route("/clientes")
def clientes():
    return render_template("clientes.html")

@app.route('/sucursales')
def sucursales():
    return render_template('sucursales.html')

# Crear la base de datos
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True) 

    