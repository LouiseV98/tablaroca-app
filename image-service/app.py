import os
from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from flask_cors import CORS

# Cargar variables de entorno
load_dotenv()

# Configuración de Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Conexión a la base de datos PostgreSQL usando variables de entorno
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

# Ruta para subir la URL de la imagen
@app.route("/images", methods=["POST"])
def upload_image():
    data = request.json
    print(f"Recibido en backend: {data}")  # Imprime el cuerpo de la solicitud

    design_id = data.get("design_id")
    image_url = data.get("url")

    if not design_id or not image_url:
        return jsonify({'message': 'Missing design_id or url'}), 400

    try:
        cur.execute(
            "INSERT INTO images (design_id, url) VALUES (%s, %s) RETURNING id",
            (design_id, image_url)
        )
        conn.commit()
        image_id = cur.fetchone()[0]

        return jsonify({"id": image_id, "url": image_url, "message": "Imagen cargada con éxito"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error al guardar la URL de la imagen: {str(e)}"}), 500

# Ruta para obtener las imágenes de un diseño
@app.route("/images/<int:design_id>", methods=["GET"])
def get_images(design_id):
    try:
        cur.execute("SELECT id, url FROM images WHERE design_id = %s", (design_id,))
        images = cur.fetchall()

        # Devuelve una lista de imágenes con sus URLs
        images_data = [{"id": img[0], "url": img[1], "design_id": design_id} for img in images]

        return jsonify(images_data)
    except Exception as e:
        return jsonify({"message": f"Error al obtener las imágenes: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
