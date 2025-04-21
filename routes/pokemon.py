from flask import Blueprint, jsonify, request
from models.pokemon import Pokemon
from sqlalchemy.exc import SQLAlchemyError
from schemas.pokemon import PokemonSchema
from marshmallow import ValidationError
from app import db

pokemon_pb = Blueprint("pokemon", __name__)


@pokemon_pb.route("/create-by-names", methods=["POST"])
def create_pokemons_by_names():
    # Check if the Pokemon already exists

    # existing_pokemon = Pokemon.query.filter_by(name=name).first()
    # if existing_pokemon:
    #     return existing_pokemon

    # Create a new Pokemon instance
    new_pokemon = Pokemon()

    # Add the new Pokemon to the session and commit
    db.session.add(new_pokemon)
    db.session.commit()

    return new_pokemon


@pokemon_pb.route("/create", methods=["POST"])
def create_pokemon():
    try:
        pokemon_data = PokemonSchema.load(request.json)
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

    pokemon = Pokemon(**pokemon_data)

    existing_pokemon = Pokemon.query.filter_by(name=pokemon.name).first()
    if existing_pokemon:
        return jsonify({"message": "Pokemon already exists"}), 400

    try:
        db.session.add(pokemon)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Task created successfully",
                    "task": PokemonSchema.dump(pokemon_data),
                }
            ),
            201,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500


@pokemon_pb.route("/<int:pokemon_id>", methods=["GET"])
def get_pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    return jsonify(pokemon.to_dict()), 200


@pokemon_pb.route("/report", methods=["GET"])
def pokemon_report():
    pokemons = [pokemon.to_dict() for pokemon in Pokemon.query.all()]
    # Return a csv of all pokemons
    return jsonify([pokemons]), 200
