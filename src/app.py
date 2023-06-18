import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, UserFavoriteCharacters, UserFavoritePlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
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


@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    # Create a list
    results = []
    for character in characters:
        results.append(character.serialize())
    response_body = {
        "msg": "ok",
        "total_records": len(results),
        "results": results
    }
    return jsonify(response_body), 200


@app.route('/characters/<int:character_id>', methods=['GET'])
def get_characters_by_id(character_id):
    characters = db.get_or_404(Character, character_id) # Este es un metodo para conseguir un id especifico de una lista
    results = characters.serialize()
    response_body = {
        "msg": " todo fino señores ",
        "total_records": len(results),
        "results": results
    }
    return jsonify(response_body), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    results = [planet.serialize() for planet in planets]
    response_body = {
        "msg": "todo fino, lucia te hateamos",
        "total_records": len(results),
        "results": results
    }
    return jsonify(response_body), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first() # Este es otro metodo para conseguir un id especifico de una lista
    if planet:
        results = planet.serialize()
        response_body = {
            "msg": "alles gut",
            "total_records": 1,
            "results": results
        }
        return response_body, 200
    else:
        response_body = {"msg": "404, not found :("}
        return response_body, 200


@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    # Create a list
    results = [user.serialize() for user in users]
    response_body = {
        "msg": " todo fino señores ",
        "total_records": len(results),
        "results": results
    }
    return jsonify(response_body), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id) # Este es otro metodo para conseguir un id especifico de una lista
    return jsonify(user.serialize())


@app.route('/user', methods=['POST'])
def post_user():
    request_body: request.get_json()
    users = User(
        email = request.body('email'),
        password = request.body('password'),
        is_active = request_body('is_active')
    )
    db.session.add(User) # Se prepara todo para el commit 
    db.session.commit # Commit de ese añadido a la base de datos, si está todo bien
    return jsonify(request_body)


@app.route('/user/favorites-planets/<int:user_id>', methods=['GET'])
def get_favorite_planet(user_id):
    favs = UserFavoritePlanets.query.filter(UserFavoritePlanets.user_id == user_id).all()
    results = [fav.serialize() for fav in favs]
    response_body = {
        "msg": "Alles super",
        "total records": len(results),
        "results": results
    }

    return jsonify(response_body), 200


@app.route('/favorite/planets', methods=['POST'])
def post_favorite_planet():

    request_body = request.get_json()
    fav = UserFavoritePlanets(user_id = request_body['user_id'], fav_planet_id = request_body['fav_planet_id'])
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize()), 200


@app.route('/user/favorites-planets/<int:fav_id>', methods=['DELETE'])
def delete_fav_planet(fav_id):
    fav = UserFavoritePlanets.query.get(fav_id)
    if fav is None:
        raise APIException('Fav is not found', status_code=404)
    db.session.delete(fav)
    db.session.commit()
    return jsonify("Su base de datos ha sido actualizada :)"), 200


# @app.route('/user/favorites-planets/<int:fav_id>', methods=['PUT'])
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def put_fav_planet(planet_id):
    request_body = request.get_json()
    fav = Planet.query.get(planet_id)
    if fav is None:
        raise APIException('Planet not found', status_code=404)
    if "name" in request_body:
        fav.name == request_body["name"]
    db.session.commit()
    return jsonify(request_body), 200


@app.route('/user/favorites-characters/<int:user_id>', methods=['GET'])
def get_favorite_character(user_id):
    favs = UserFavoriteCharacters.query.filter(UserFavoriteCharacters.user_id == user_id).all()
    results = [fav.serialize() for fav in favs]
    response_body = {
        "msg": "coolio",
        "total records": len(results),
        "results": results
    }

    return jsonify(response_body), 200


@app.route('/favorite/characters', methods=['POST'])
def post_favorite_character():
    request_body = request.get_json()
    favorite = UserFavoriteCharacters(user_id = request_body['user_id'], fav_character_id = request_body['fav_character_id'])
    db.session.add(favorite)
    db.session.commit()
    return jsonify(request_body), 200


@app.route('/user/favorites-characters/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_character(favorite_id):
    fav = UserFavoriteCharacters.query.get(favorite_id)
    if fav is None:
        raise APIException('Fav was not found', status_code=404)
    db.session.delete(fav)
    db.session.commit()
    return jsonify("Todo crema"), 200


@app.route('/characters/<int:character_id>', methods=['PUT'])
def put_fav_character(character_id):
    request_body = request.get_json()
    fav = Character.query.get(character_id)
    if fav is None:
        raise APIException('Character not found', status_code=404)
    if "name" in request_body:
        fav.name == request_body["name"]
    db.session.commit()
    return jsonify(request_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)