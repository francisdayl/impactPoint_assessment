import requests
from schemas.pokemon import pokemon_schema

pokemon_request = requests.get("https://pokeapi.co/api/v2/pokemon/1")
pokemon_request_json = pokemon_request.json()
pokemon_request_data = {
    "name": pokemon_request_json["name"],
    "height": pokemon_request_json["height"],
    "weight": pokemon_request_json["weight"],
    "base_experience": pokemon_request_json["base_experience"],
    "location_area_encounters": pokemon_request_json["location_area_encounters"],
    "is_active": True,
}
pokemon_data = pokemon_schema.load(pokemon_request_data)
