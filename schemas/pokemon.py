from marshmallow import fields, validate, ValidationError
from app import ma
from models.pokemon import Pokemon


class PokemonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pokemon

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True, validate=validate.Length(min=1))
    height = ma.auto_field(required=True, validate=validate.Range(min=0))
    weight = ma.auto_field(required=True, validate=validate.Range(min=0))
    base_experience = ma.auto_field(required=True, validate=validate.Range(min=0))
    location_area_encounters = ma.auto_field(
        required=False,
        validate=validate.Length(max=500),
        error_messages={
            "max": "Location area encounters cannot exceed 500 characters."
        },
    )
    created_at = ma.auto_field(dump_only=True)
    is_active = ma.auto_field()


pokemon_schema = PokemonSchema()
pokemons_schema = PokemonSchema(many=True)
