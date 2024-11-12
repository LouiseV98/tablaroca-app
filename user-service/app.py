from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
import datetime
import hashlib

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
        self.password = hashlib.sha256(password.encode()).hexdigest()  # Guardamos el hash de la contraseña
        self.role = role

# Crea todas las tablas
with app.app_context():
    db.create_all()

def generate_token(user_id):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({"user_id": user_id, "exp": expiration}, app.config['SECRET_KEY'], algorithm="HS256")
    return token

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    hashed_password = hashlib.sha256(data["password"].encode()).hexdigest()  # Generar el hash
    new_user = User(username=data["username"], password=hashed_password, role=data.get("role", "user"))

    # Verifica si el usuario ya existe
    if User.query.filter_by(username=new_user.username).first():
        return jsonify({"message": "El usuario ya existe"}), 409

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id, "username": new_user.username, "role": new_user.role}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    hashed_password = hashlib.sha256(data["password"].encode()).hexdigest()  # Generamos el hash de la contraseña proporcionada
    user = User.query.filter_by(username=data["username"], password=hashed_password).first()

    if user:
        token = generate_token(user.id)  # Generamos el token solo si las credenciales son correctas
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
