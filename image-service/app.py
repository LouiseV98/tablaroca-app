# image-service/app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos simulados de almacenamiento de imágenes
images = []

@app.route("/images", methods=["POST"])
def upload_image():
    data = request.json
    new_image = {"id": len(images) + 1, "design_id": data["design_id"], "url": data["url"]}
    images.append(new_image)
    return jsonify(new_image), 201

@app.route("/images/<int:design_id>", methods=["GET"])
def get_images(design_id):
    design_images = [img for img in images if img["design_id"] == design_id]
    return jsonify(design_images)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
