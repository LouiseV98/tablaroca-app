import os
from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Flask y PostgreSQL
app = Flask(__name__)

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname=os.getenv("users"),
    user=os.getenv("postgres"),
    password=os.getenv("huehue123"),
    host=os.getenv("localhost"),
    port=os.getenv("5432")
)
cur = conn.cursor()

# Ruta para subir la URL de la imagen
@app.route("/images", methods=["POST"])
def upload_image():
    data = request.json
    design_id = data.get("design_id")
    image_url = data.get("url")  # Asumimos que el frontend enviará la URL de la imagen

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
        images_data = [{"id": img[0], "url": img[1]} for img in images]

        return jsonify(images_data)
    except Exception as e:
        return jsonify({"message": f"Error al obtener las imágenes: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
