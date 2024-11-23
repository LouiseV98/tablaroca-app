import os
from flask import Flask, jsonify, request, send_from_directory
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from flask_cors import CORS
from functools import wraps
import jwt

# Cargar variables de entorno
load_dotenv()

SECRET_KEY = "tu_clave_secreta"

# Configuración de Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Directorio para almacenar imágenes
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Extensiones permitidas
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

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
        token = request.headers.get("Authorization")  # El token se espera en el encabezado Authorization

        if not token:
            return jsonify({"message": "Token no proporcionado"}), 401

        try:
            # Decodificar el token y obtener el user_id
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = decoded_token["user_id"]  # Almacenar user_id en la solicitud
            print("ID de usuario decodificado:", request.user_id)

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "El token ha expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token inválido"}), 401

        return f(*args, **kwargs)
    return decorated

@app.route("/images/upload", methods=["POST"])
@token_required
def upload_image():
    """
    Subir una imagen asociada a un usuario autenticado.
    """
    if "image" not in request.files:
        return jsonify({"message": "No se proporcionó el archivo de imagen"}), 400

    image = request.files["image"]
    user_id = request.user_id  # Obtener user_id del token

    if image.filename == "":
        return jsonify({"message": "No se seleccionó ningún archivo"}), 400

    if not allowed_file(image.filename):
        return jsonify({"message": "Extensión de archivo no permitida"}), 400

    try:
        # Guardar la imagen en el servidor
        filename = f"{user_id}_{image.filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(filepath)

        # Guardar la ruta de la imagen en la base de datos
        cur.execute(
            "INSERT INTO images (user_id, filename) VALUES (%s, %s) RETURNING id",
            (user_id, filename)
        )
        conn.commit()
        image_id = cur.fetchone()[0]

        return jsonify({"id": image_id, "filename": filename, "message": "Imagen cargada con éxito"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error al guardar la imagen: {str(e)}"}), 500

@app.route('/uploads/<filename>', methods=["GET"])
@token_required
def uploaded_file(filename):
    """
    Descarga una imagen solo si pertenece al usuario autenticado.
    """
    user_id = request.user_id  # Obtener user_id del token

    try:
        # Verifica que la imagen pertenece al usuario
        cur.execute("SELECT id FROM images WHERE filename = %s AND user_id = %s", (filename, user_id))
        image = cur.fetchone()

        if not image:
            return jsonify({"message": "Acceso denegado"}), 403

        # Enviar la imagen si pasa la validación
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    except Exception as e:
        return jsonify({"message": f"Error al acceder a la imagen: {str(e)}"}), 500


@app.route("/images", methods=["GET"])
@token_required
def get_images():
    """
    Obtén las imágenes del usuario autenticado.
    """
    user_id = request.user_id  # Obtener user_id del token

    try:
        cur.execute("SELECT id, filename FROM images WHERE user_id = %s", (user_id,))
        images = cur.fetchall()

        return jsonify([{"id": row[0], "filename": row[1]} for row in images]), 200
    except Exception as e:
        return jsonify({"message": f"Error al obtener las imágenes: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
