from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///designs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de SQLAlchemy
db = SQLAlchemy(app)

# Modelo de la base de datos para los diseños
class Design(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Inicialización de la base de datos (creación de tablas)
def initialize_db():
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen

# Llamar a la función de inicialización antes de recibir cualquier solicitud
initialize_db()

@app.route("/designs", methods=["GET"])
def list_designs():
    designs = Design.query.all()  # Obtener todos los diseños de la base de datos
    return jsonify([{
        "id": design.id,
        "name": design.name,
        "description": design.description,
        "price": design.price
    } for design in designs])

@app.route("/register", methods=["POST"])
def add_design():
    data = request.json
    new_design = Design(
        name=data.get("name"),
        description=data.get("description"),
        price=data.get("price")
    )
    db.session.add(new_design)
    db.session.commit()
    return jsonify({
        "id": new_design.id,
        "name": new_design.name,
        "description": new_design.description,
        "price": new_design.price
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
