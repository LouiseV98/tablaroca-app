from flask import Flask, jsonify, request
from flask_cors import CORS  # Importa la extensión CORS
import jwt
import datetime

app = Flask(__name__)
CORS(app, resources={r"/login": {"origins": "http://localhost:3000"}})  # Permite solicitudes solo desde el frontend en localhost:3000
# También puedes permitir todos los orígenes con CORS(app) si prefieres

app.config['SECRET_KEY'] = 'tu_clave_secreta'

# Datos simulados para usuarios registrados
users = [{"id": 1, "username": "admin", "password": "admin123", "role": "admin"}]

def generate_token(user_id):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({"user_id": user_id, "exp": expiration}, app.config['SECRET_KEY'], algorithm="HS256")
    return token

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    new_user = {"id": len(users) + 1, "username": data["username"], "password": data["password"], "role": data.get("role", "user")}
    users.append(new_user)
    return jsonify(new_user), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = next((u for u in users if u["username"] == data["username"] and u["password"] == data["password"]), None)
    if user:
        token = generate_token(user["id"])
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # O usa el puerto configurado en Kubernetes si es necesario



