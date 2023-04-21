"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False


# Establecemos la conexion con la base de datos
db_url = os.getenv("DATABASE_URL") # Sacamos la direccion de la BBDD del archivo .env
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Migraciones -> Actualizaciones de la BBDD
MIGRATE = Migrate(app, db)
db.init_app(app) # -> Si no hay una instancia de la BBDD la crea


# CORS
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# -> Empiezan endpoints
@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200



# Todos los personajes
# Una ruta que te traiga la lista
# Una ruta que te traiga un elemento
# Una ruta que te cree un elemento
# Delete
# Upd

@app.route('/characters', methods=['GET'])
def get_all_characters():
    character_list = Character.query.all()
    serialized_characters = [character.serialize() for character in character_list]
    return jsonify({"characters": serialized_characters})

@app.route('/character', methods=['POST'])
def create_character():
    body = request.json
    body_name = body.get('name', None)
    body_eye_color = body.get('eye_color', None)
    body_homeworld = body.get('homeworld', None)
    body_gender = body.get('gender', None)

    if body_name is None or body_eye_color is None or body_homeworld is None or body_gender is None:
        return {"error": "Todos los campos requeridos"}, 400

    # verificamos si ya existe un personaje con el nombre que recibes del body
    character_exists = Character.query.filter_by(name=body_name).first()
    if character_exists:
        return {"error": f"Ya existe un personaje con el nombre: {body_name}"}, 400

    new_character = Character(name=body_name, eye_color=body_eye_color, homeworld=body_homeworld, gender=body_gender)
    db.session.add(new_character)

    try:
        db.session.commit() # commit ->
        return jsonify({"msg": "personaje creado con exito!"}), 201

    except Exception as error:
        db.session.rollback()
        return {"error": error}, 500

@app.route('/character/<int:id>', methods=['GET'])
def get_character_by_id(id):
    character = Character.query.filter_by(id=id).first()

    if not character:
        return {"error": "No existe un personaje con ese id"}, 404

    return jsonify({"personaje": character.serialize()})

# CRUD - C-reate R-ead U-pdate D-elete
# Put -> actualizar
# delete -> borrar
# Todos los planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    # Model.query.all() -> trae todos los elementos
    planets = Planet.query.all()
    # nueva_lista = [item.serialize() for item in list]
    serialized_planets = [planet.serialize() for planet in planets]
    
    return jsonify({ "data": serialized_planets })

# Trae UN planeta
@app.route('/planet', methods=['GET'])
def get_planet():
    # 1
    test_id = 1
    # Model.query.filter_by(campo=valor) ->
    planet = Planet.query.filter_by(id=test_id).one_or_none()
    print("serializado")
    print(planet.serialize())
    print("Sin serializar")
    print(planet)
    return jsonify({"data": planet.serialize()})

# Agregue un planeta

@app.route('/planet', methods=['POST'])
def add_planet():
    # que campos necesito para crear un planeta
    # -> Body = {name}
    body = request.json # Busco el json del body
    
    # Validaciones
    body_name = body.get('name', None) # Extraigo el name, si no existe la variable vale None
    if body_name is None:
        return {"error": "Todos los campos requeridos"}, 400

    # Valido si ya existe un planeta con ese nombre
    planet_exists = Planet.query.filter_by(name=body_name).first()
    if planet_exists:
        return {"Error": f"Ya existe un planeta con el nombre: {body_name}"}

    # Creando una nueva instancia del modelo
    new_planet = Planet(name=body_name) 

    # añado el cambio
    db.session.add(new_planet) # git add .

    # Guardo el cambio
    db.session.commit() # git commit
    
    # Status 201 -> Creado
    return jsonify({"data": f"Planeta {body_name} creado con exito"}), 201

# -> termina Endpoints


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
