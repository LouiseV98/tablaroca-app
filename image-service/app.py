import os
from flask import Flask, jsonify, request, send_from_directory
import psycopg2
from dotenv import load_dotenv
from flask_cors import CORS
from functools import wraps
import jwt
import logging

# Cargar variables de entorno
load_dotenv()

SECRET_KEY = "tu_clave_secreta"

# Configuración de Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers="Authorization")

# Directorio para almacenar imágenes
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Extensiones permitidas
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# Conexión a PostgreSQL
try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")
    exit(1)

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            app.logger.debug("Token no encontrado en la cabecera")
            return jsonify({"message": "Token no encontrado"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            app.logger.debug(f"Token decodificado correctamente: {data}")
            request.user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            app.logger.debug("El token ha expirado")
            return jsonify({"message": "El token ha expirado"}), 401
        except jwt.InvalidTokenError as e:
            app.logger.debug(f"Error de validación de token: {str(e)}")
            return jsonify({"message": "Token inválido"}), 401

        return f(*args, **kwargs)
    return decorated

@app.route("/images/upload", methods=["POST"])
@token_required
def upload_image():
    if "image" not in request.files:
        return jsonify({"message": "Archivo de imagen requerido"}), 400

    file = request.files["image"]
    user_id = request.user_id  # Obtenemos el user_id desde el token

    if not allowed_file(file.filename):
        return jsonify({"message": "Extensión no permitida"}), 400

    # Guardar archivo en el servidor
    filename = f"{user_id}_{file.filename}"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        # Guardar información en la base de datos
        cur.execute(
            "INSERT INTO images (user_id, filename) VALUES (%s, %s)",
            (user_id, filename),
        )
        conn.commit()
        return jsonify({"message": "Imagen subida correctamente"}), 201
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Error al guardar en la base de datos: {e}")
        return jsonify({"message": f"Error al guardar en la base de datos: {e}"}), 500

@app.route("/images", methods=["GET"])
@token_required
def list_images():
    user_id = request.user_id  # Obtener user_id desde el token
    try:
        cur.execute("SELECT filename FROM images WHERE user_id = %s", (user_id,))
        rows = cur.fetchall()
        files = [row[0] for row in rows]
        return jsonify(files), 200
    except Exception as e:
        app.logger.error(f"Error al listar imágenes: {e}")
        return jsonify({"message": f"Error al listar imágenes: {e}"}), 500

@app.route('/uploads/<path:filename>', methods=["GET"])
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
