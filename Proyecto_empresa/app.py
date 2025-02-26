from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Creamos una instancia de la aplicación Flask.
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/prueba_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

# Definimos la ruta principal de la aplicación que se ejecuta al acceder a la URL raíz ('/').
@app.route("/")
@app.route("/base")
def base():
    # Renderizamos el template HTML y pasamos la lista weather_data como contexto.
    return render_template("base.html")

# Modelo User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_json(self):
        return {"id": self.id, "name": self.name, "email": self.email}

# Crear base de datos
with app.app_context():
    db.create_all()

# Rutas CRUD
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_json() for user in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_json()), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.name = data['name']
    user.email = data['email']
    db.session.commit()
    return jsonify(user.to_json())

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"})

@app.route('/index')
def index():
    return render_template('index.html')

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


@app.route("/categoria")
def categoria():
    return render_template("categoria.html")

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

# Modelo de Categoría
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    imagen = db.Column(db.String(255), nullable=True)

# Crear la base de datos
with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

