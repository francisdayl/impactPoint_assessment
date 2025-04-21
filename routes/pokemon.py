from flask import Blueprint, jsonify, request, Response
import requests
from models.pokemon import Pokemon
from sqlalchemy.exc import SQLAlchemyError
from schemas.pokemon import pokemon_schema, pokemons_schema, string_list_schema
from marshmallow import ValidationError
from app import db
import polars as pl

pokemon_pb = Blueprint("pokemon", __name__)


@pokemon_pb.route("/create-by-name", methods=["POST"])
def create_pokemons_by_names():
    pokemon_name = request.json.get("name")
    if not pokemon_name:
        return jsonify({"message": "Pokemon name is required"}), 400
    existing_pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
    if existing_pokemon:
        return jsonify({"message": "Pokemon already exists"}), 400
    try:
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = requests.get(pokemon_url)
        if not response.ok:
            return (
                jsonify(
                    {
                        "message": f"Failed to fetch data for {pokemon_name}: {response.status_code}"
                    }
                ),
                400,
            )
        pokemon_request_json = response.json()
        pokemon_request_data = {
            "name": pokemon_request_json["name"],
            "height": pokemon_request_json["height"],
            "weight": pokemon_request_json["weight"],
            "base_experience": pokemon_request_json["base_experience"],
            "location_area_encounters": pokemon_request_json[
                "location_area_encounters"
            ],
            "is_active": True,
        }
        pokemon_data = pokemon_schema.load(pokemon_request_data)
        pokemon = Pokemon(**pokemon_data)
        db.session.add(pokemon)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Pokemon created successfully",
                    "task": pokemon_schema.dump(pokemon),
                }
            ),
            201,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500


@pokemon_pb.route("/create", methods=["POST"])
def create_pokemon():
    try:
        pokemon_data = pokemon_schema.load(request.json)
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
                    "message": "Pokemon created successfully",
                    "task": pokemon_schema.dump(pokemon_data),
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
    return jsonify(pokemon_schema.dump(pokemon)), 200


@pokemon_pb.route("/<string:pokemon_name>", methods=["GET"])
def get_pokemon_by_name(pokemon_name):
    pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
    if not pokemon:
        return jsonify({"message": "Pokemon not found"}), 404
    return jsonify(pokemon_schema.dump(pokemon)), 200


@pokemon_pb.route("/report", methods=["GET"])
def pokemon_report():
    pokemons = pokemons_schema.dump(Pokemon.query.all())
    df = pl.DataFrame(pokemons)
    csv_data = df.write_csv()
    response = Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=pokemons_data.csv"},
    )
    return response
