import os
from flask import Flask, jsonify, request, send_from_directory
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from flask_cors import CORS

# Cargar variables de entorno
load_dotenv()

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

@app.route("/images/upload", methods=["POST"])
def upload_image():
    """
    Subir una imagen y asociarla a un diseño.
    La imagen se guarda en la carpeta `uploads` y se registra en la base de datos.
    """
    if "image" not in request.files:
        return jsonify({"message": "No se proporcionó el archivo de imagen"}), 400

    image = request.files["image"]
    design_id = request.form.get("design_id")

    if not design_id:
        return jsonify({"message": "Falta el ID del diseño"}), 400

    if image.filename == "":
        return jsonify({"message": "No se seleccionó ningún archivo"}), 400

    if not allowed_file(image.filename):
        return jsonify({"message": "Extensión de archivo no permitida"}), 400

    try:
        # Guardar la imagen en el servidor
        filename = f"{design_id}_{image.filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(filepath)

        # Guardar la ruta de la imagen en la base de datos
        image_url = f"/uploads/{filename}"
        cur.execute(
            "INSERT INTO images (design_id, url) VALUES (%s, %s) RETURNING id",
            (design_id, image_url)
        )
        conn.commit()
        image_id = cur.fetchone()[0]

        return jsonify({"id": image_id, "url": image_url, "message": "Imagen cargada con éxito"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error al guardar la imagen: {str(e)}"}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/images', methods=['GET'])
def get_images():
    try:
        # Lista los archivos en la carpeta 'uploads'
        images = os.listdir(app.config['UPLOAD_FOLDER'])
        
        # Filtra solo los archivos de imagen
        image_files = [img for img in images if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        
        return jsonify(image_files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
