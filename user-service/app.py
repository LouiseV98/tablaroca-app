from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
import datetime
import bcrypt

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Configuración de la conexión a PostgreSQL
app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:huehue123@localhost:5432/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de usuario
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Almacenamos el hash de la contraseña
    role = db.Column(db.String(20), default="user")

    def __init__(self, username, password, role="user"):
        self.username = username
        # Asegúrate de que password sea un str antes de pasar a bytes
        if isinstance(password, str):  # Si el password es un string
            password = password.encode()  # Convertimos a bytes
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())  # Hash de la contraseña
        self.password = password.decode('utf-8')
        self.role = role

# Crea todas las tablas
with app.app_context():
    users = User.query.all()
    for user in users:
        # Verifica si el hash está mal formado (por ejemplo, no tiene un formato de bcrypt correcto)
        if len(user.password) != 60:  # Longitud del hash bcrypt es siempre 60 caracteres
            print(f"Actualizando contraseña para {user.username}")
            # Generamos un nuevo hash bcrypt para cada contraseña
            hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
            user.password = hashed_password.decode('utf-8')  # Almacenamos el nuevo hash
    db.session.commit()

def generate_token(user_id):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({"user_id": user_id, "exp": expiration}, app.config['SECRET_KEY'], algorithm="HS256")
    return token

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"].strip()
    password = data["password"].strip()

    # Generamos un hash bcrypt para la contraseña
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # Asegúrate de que esté codificado a bytes

    new_user = User(username=username, password=hashed_password, role=data.get("role", "user"))

    # Verifica si el usuario ya existe
    if User.query.filter_by(username=new_user.username).first():
        return jsonify({"message": "El usuario ya existe"}), 409

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id, "username": new_user.username, "role": new_user.role}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"].strip()
    password = data["password"].strip()

    print(f"Nombre de usuario recibido: {username}")  # Imprime el nombre de usuario recibido

    # Obtener el usuario de la base de datos
    user = User.query.filter_by(username=username).first()

    if user is None:
        # Si el usuario no existe, retornar un error apropiado
        print(f"No se encontró usuario con el nombre {username}")
        return jsonify({"message": "Credenciales incorrectas"}), 401

    print(f"Hash almacenado: {user.password}")
    print(f"Hash generado: {bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')}")

    # Verificamos si la contraseña coincide con el hash almacenado
    if user and bcrypt.checkpw(password.encode(), user.password.encode()):  # Convertimos el hash almacenado a bytes para comparación
        token = generate_token(user.id)  # Generamos el token solo si las credenciales son correctas
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
