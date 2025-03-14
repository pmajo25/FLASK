from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configuración de la aplicación
app = Flask(__name__)
app.secret_key = "mi_clave_secreta_super_segura"

# Configuración de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/empresa_fanta'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =======================
# MODELOS DE BASE DE DATOS
# =======================

# Modelo Usuario
class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }

# Modelo Usuario

class Clientes(db.Model):
    __tablename__ = "clientes"
    idCliente = db.Column(db.Integer, primary_key=True)
    idEncargado = db.Column(db.Integer, db.ForeignKey('empleados.idEmpleado'), nullable=False)  # Aquí está la corrección
    identificacion = db.Column(db.String(80), nullable=False)
    nombres = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(80), nullable=False)
    tipoCliente = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), nullable=False)

    encargado = db.relationship('Empleados', backref='clientes')  # Relación con empleados


    def to_json(self):
        return {
            "idCliente": self.idCliente,
            "idEncargado": self.idEncargado,
            "identificacion": self.identificacion,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "tipoCliente": self.tipoCliente,
            "email": self.email,
            "telefono": self.telefono,
            "estado": self.estado
        }
  
class Sucursales(db.Model):
    __tablename__ = "sucursales"
    
    idSucursal = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    ciudad = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(80), nullable=False)

    def to_json(self):
        return {
            "idSucursal": self.idSucursal,
            "nombre": self.nombre,
            "ciudad": self.ciudad,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "estado": self.estado
        }
  
class Empleados(db.Model):
    __tablename__ = "empleados"
    
    idEmpleado = db.Column(db.Integer, primary_key=True)
    identificacion = db.Column(db.String(80), nullable=False)
    nombres = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(80), nullable=False)
    cargo = db.Column(db.String(80), nullable=False)
    salario = db.Column(db.String(80), nullable=False)
    estado = db.Column(db.String(80), nullable=False)
    idSucursal = db.Column(db.Integer, db.ForeignKey('sucursales.idSucursal'), nullable=False)  # Relación con Sucursales
    sucursal = db.relationship('Sucursales', backref='empleados')  # Relación para acceder a la sucursal

    def to_json(self):
        return {
            "idEmpleado": self.idEmpleado,
            "identificacion": self.identificacion,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "cargo": self.cargo,
            "salario": self.salario,
            "estado": self.estado,
            "idSucursal": self.idSucursal
        }
    
# Modelo Categoría
class Categoria(db.Model):
    __tablename__ = "categorias"

    idCategoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    descripcion = db.Column(db.String(120), unique=True, nullable=False)
    estado = db.Column(db.String(10), nullable=False, default='Activo')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_json(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion,
            "fecha_actualizacion": self.fecha_actualizacion
        }

# Modelo Productos
class Productos(db.Model):
    __tablename__ = "productos"
    
    idProducto = db.Column(db.Integer, primary_key=True)
    idCategoria = db.Column(db.Integer, db.ForeignKey('categorias.idCategoria'), nullable=False)
    producto = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    referencia = db.Column(db.String(50))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(10), nullable=False, default='Activo')

    def to_json(self):
        return {
            "idProducto": self.idProducto,
            "idCategoria": self.idCategoria,
            "producto": self.producto,
            "descripcion": self.descripcion,
            "referencia": self.referencia,
            "precio": self.precio,
            "stock": self.stock,
            "estado": self.estado
        }



# Crear base de datos si no existe
with app.app_context():
    db.create_all()

# =======================
# RUTAS CRUD
# =======================


@app.route('/createUsers', methods=['POST'])
def createUsers():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    if password != confirm_password:
        flash("Las contraseñas no coinciden", "danger")
        return redirect(url_for('login'))

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("El correo ya está registrado", "warning")
        return redirect(url_for('login'))

    hashed_password = generate_password_hash(password)

    new_user = User(
        name=name, 
        email=email, 
        password=hashed_password,  # Guardamos la contraseña hasheada
        role='Administrador'
    )

    db.session.add(new_user)
    db.session.commit()

    flash("Usuario registrado con éxito", "success")
    return redirect(url_for('login'))


# =======================
# AUTENTICACIÓN
# =======================


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()  # Buscamos por email

        if user and check_password_hash(user.password, password):  # Verificamos hash
            session['user_id'] = user.id
            session['role'] = user.role  

            if user.role == 'Administrador':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'))

        flash("Credenciales incorrectas", "danger")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for("login"))

# =======================
# RUTAS DE CATEGORÍAS
# =======================

@app.route("/categoria", methods=["GET"])
def categoria():
    if "user_id" not in session:
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))
    
    obtener_categorias = Categoria.query.all()
    
    return render_template("categoria.html", obtener_categorias=obtener_categorias)
    
@app.route("/agregar_categoria", methods=["POST", "GET"])
def agregar_categoria():
    if "user_id" not in session:
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        estado = request.form["estado"]

        nueva_categoria = Categoria(nombre=nombre, descripcion=descripcion, estado=estado)
        db.session.add(nueva_categoria)
        db.session.commit()

        flash("Categoría añadida correctamente", "success")  # Mensaje de éxito
        return redirect(url_for("categoria"))

    categorias = Categoria.query.all()
    return render_template("categoria.html", categorias=categorias)


@app.route("/editar_categoria/<int:id>", methods=["GET", "POST"])
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == "POST":
        categoria.nombre = request.form["nombre"]
        categoria.descripcion = request.form["descripcion"]
        categoria.estado = request.form["estado"]
        db.session.commit()
        flash("Categoría editada correctamente", "info")  # Mensaje de éxito
        return redirect(url_for("categoria"))
    return render_template("categoria.html", categoria=categoria)


@app.route("/eliminar_categoria/<int:id>", methods=["POST"])
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash("Categoría eliminada correctamente", "danger")  # Mensaje de eliminación
    return redirect(url_for("categoria"))


# =======================
# RUTAS DE EMPLEADOS
# =======================
@app.route("/empleados", methods=["GET"])
def empleados():
    if "user_id" not in session:
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))
    
    obtener_empleados = Empleados.query.all()
    sucursales = Sucursales.query.filter_by(estado='Activo').all()

    return render_template("empleado.html", obtener_empleados=obtener_empleados, sucursales=sucursales)
    
@app.route("/agregar_empleado", methods=["POST", "GET"])
def agregar_empleado():
    if "user_id" not in session:
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        identificacion = request.form["identificacion"]
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        cargo = request.form["cargo"]
        salario = request.form["salario"]
        estado = request.form["estado"]
        idSucursal = request.form["idSucursal"]  # Nuevo campo para la sucursal

        nuevo_empleado = Empleados(
            identificacion=identificacion,
            nombres=nombres,
            apellidos=apellidos,
            cargo=cargo,
            salario=salario,
            estado=estado,
            idSucursal=idSucursal  # Asignar la sucursal
        )
        db.session.add(nuevo_empleado)
        db.session.commit()

        flash("Empleado añadido correctamente", "success")
        return redirect(url_for("empleados"))

    sucursales = Sucursales.query.filter_by(estado='Activo').all()  # Obtener sucursales activas
    return render_template("empleado.html", sucursales=sucursales)


@app.route("/editar_empleado/<int:idEmpleado>", methods=["GET", "POST"])
def editar_empleado(idEmpleado):
    empleado = Empleados.query.get_or_404(idEmpleado)
    sucursales = Sucursales.query.filter_by(estado='Activo').all()  # Obtener sucursales activas

    if request.method == "POST":
        empleado.identificacion = request.form["identificacion"]
        empleado.nombres = request.form["nombres"]
        empleado.apellidos = request.form["apellidos"]
        empleado.cargo = request.form["cargo"]
        empleado.salario = request.form["salario"]
        empleado.estado = request.form["estado"]
        empleado.idSucursal = request.form["idSucursal"]  # Actualizar la sucursal
        db.session.commit()
        flash("Empleado editado correctamente", "info")
        return redirect(url_for("empleados"))

    return render_template("empleado.html", empleado=empleado, sucursales=sucursales)


@app.route("/eliminar_empleado/<int:idEmpleado>", methods=["POST"])
def eliminar_empleado(idEmpleado):
    empleado = Empleados.query.get_or_404(idEmpleado)
    db.session.delete(empleado)
    db.session.commit()
    flash("empleado eliminado correctamente", "danger")  # Mensaje de eliminación
    return redirect(url_for("empleados"))

# =======================
# RUTAS DE CLIENTES
# =======================
@app.route("/clientes", methods=["GET"])
def clientes():
    if "user_id" not in session:
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))
    
    obtener_clientes = Clientes.query.all()
    empleados = Empleados.query.all()  # Obtener la lista de empleados
    
    return render_template("cliente.html", obtener_clientes=obtener_clientes, empleados=empleados)
    
@app.route("/agregar_cliente", methods=["POST", "GET"])
def agregar_cliente():
    if "user_id" not in session:
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))


    if request.method == "POST":
        idEncargado = request.form["idEncargado"]
        identificacion = request.form["identificacion"]
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        tipoCliente = request.form["tipoCliente"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        estado = request.form["estado"]

        nuevo_cliente = Clientes(idEncargado=idEncargado, identificacion=identificacion, nombres=nombres, apellidos=apellidos, tipoCliente=tipoCliente , email=email,  telefono=telefono, estado=estado)
        db.session.add(nuevo_cliente)
        db.session.commit()

        flash("Cliente añadido correctamente", "success")
        return redirect(url_for("clientes"))

    return render_template("cliente.html")


@app.route("/editar_cliente/<int:idCliente>", methods=["GET", "POST"])
def editar_cliente(idCliente):
    cliente = Clientes.query.get_or_404(idCliente)
    empleados = Empleados.query.all()  # Obtener empleados

    if request.method == "POST":
        cliente.idEncargado = request.form["idEncargado"]
        cliente.identificacion = request.form["identificacion"]
        cliente.nombres = request.form["nombres"]
        cliente.apellidos = request.form["apellidos"]
        cliente.tipoCliente = request.form["tipoCliente"]
        cliente.email = request.form["email"]
        cliente.telefono = request.form["telefono"]
        cliente.estado = request.form["estado"]

        db.session.commit()
        flash("Cliente editado correctamente", "info")
        return redirect(url_for("clientes"))

    return render_template("cliente.html", cliente=cliente, empleados=empleados)


@app.route("/eliminar_cliente/<int:idCliente>", methods=["POST"])
def eliminar_cliente(idCliente):
    cliente = Clientes.query.get_or_404(idCliente)
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente eliminada correctamente", "danger")  # Mensaje de eliminación
    return redirect(url_for("cliente.html"))


# =======================
# RUTAS DE PRODUCTOS
# =======================

@app.route("/productos", methods=["GET"])
def productos():
    if "user_id" not in session:
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))
    
    obtener_productos = db.session.query(Productos, Categoria.nombre).join(Categoria, Productos.idCategoria == Categoria.idCategoria).all()
    categorias = Categoria.query.filter_by(estado='Activo').all()
    
    return render_template("producto.html", obtener_productos=obtener_productos, categorias=categorias)

    
@app.route("/agregar_producto", methods=["POST", "GET"])
def agregar_producto():
    if "user_id" not in session:
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))

    categorias = Categoria.query.filter_by(estado='Activo').all()

    if request.method == "POST":
        idCategoria = request.form["idCategoria"]
        producto = request.form["producto"]
        descripcion = request.form["descripcion"]
        referencia = request.form["referencia"]
        precio = request.form["precio"]
        stock = request.form["stock"]
        estado = request.form["estado"]

        nuevo_producto = Productos(
            idCategoria=idCategoria,
            producto=producto,
            descripcion=descripcion,
            referencia=referencia,
            precio=precio,
            stock=stock,
            estado=estado
        )
        db.session.add(nuevo_producto)
        db.session.commit()

        flash("Producto añadido correctamente", "success")
        return redirect(url_for("productos"))

    return render_template("producto.html", categorias=categorias)

@app.route("/editar_producto/<int:idProducto>", methods=["GET", "POST"])
def editar_producto(idProducto):
    producto = Productos.query.get_or_404(idProducto)
    categorias = Categoria.query.filter_by(estado='activo').all()  # Obtener categorías activas

    if request.method == "POST":
        producto.idCategoria = request.form["idCategoria"]
        producto.producto = request.form["producto"]
        producto.descripcion = request.form["descripcion"]
        producto.referencia = request.form["referencia"]
        producto.precio = request.form["precio"]
        producto.stock = request.form["stock"]
        producto.estado = request.form["estado"]
        db.session.commit()
        flash("Producto editado correctamente", "info")
        return redirect(url_for("productos"))

    return render_template("producto.html", producto=producto, categorias=categorias)

@app.route("/eliminar_producto/<int:idProducto>", methods=["POST"])
def eliminar_producto(idProducto):
    producto = Productos.query.get_or_404(idProducto)
    db.session.delete(producto)
    db.session.commit()
    flash("producto eliminado correctamente", "danger")  # Mensaje de eliminación
    return redirect(url_for("producto.html"))


# =======================
# RUTAS DE SUCURSALES
# =======================
@app.route("/sucursales", methods=["GET"])
def sucursales():
    if "user_id" not in session:
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))
    
    obtener_sucursales = Sucursales.query.all()
    
    return render_template("sucursales.html", obtener_sucursales=obtener_sucursales)

    
@app.route("/agregar_sucursal", methods=["POST", "GET"])
def agregar_sucursal():
    if "user_id" not in session:
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        ciudad = request.form["ciudad"]
        estado = request.form["estado"]

        nueva_sucursal = Sucursales(nombre=nombre, ciudad=ciudad, direccion=direccion, telefono=telefono, estado=estado)
        db.session.add(nueva_sucursal)
        db.session.commit()

        flash("Sucursal añadida correctamente", "success")  # Mensaje de éxito
        return redirect(url_for("sucursales"))

    sucursales = Sucursales.query.all()
    return render_template("sucursales.html", sucursales=sucursales)


@app.route("/editar_sucursal/<int:idSucursal>", methods=["GET", "POST"])
def editar_sucursal(idSucursal):
    sucursal = Sucursales.query.get_or_404(idSucursal)
    if request.method == "POST":
        sucursal.nombre = request.form["nombre"]
        sucursal.direccion = request.form["direccion"]
        sucursal.telefono = request.form["telefono"]
        sucursal.ciudad = request.form["ciudad"]
        sucursal.estado = request.form["estado"]
        db.session.commit()
        flash("Sucursal editada correctamente", "info")  # Mensaje de éxito
        return redirect(url_for("sucursales"))
    return render_template("sucursales.html", sucursal=sucursal)


@app.route("/eliminar_sucursal/<int:idSucursal>", methods=["POST"])
def eliminar_sucursal(idSucursal):
    sucursal = Sucursales.query.get_or_404(idSucursal)
    db.session.delete(sucursal)
    db.session.commit()
    flash("Sucursal eliminada correctamente", "danger")  # Mensaje de eliminación
    return redirect(url_for("sucursales"))



# =======================
# OTRAS RUTAS
# =======================

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/recuperacion")
def recuperacion():
    return render_template("recuperacion.html")


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/promociones")
def promociones():
    return render_template("promociones.html")

@app.route("/productomenu")
def productomenu():
    return render_template("productomenu.html")

# =======================
# EJECUCIÓN DE LA APP
# =======================

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
