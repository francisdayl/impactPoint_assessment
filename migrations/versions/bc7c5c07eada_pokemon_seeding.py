"""Pokemon Seeding

Revision ID: bc7c5c07eada
Revises: 8aaeb165d8f3
Create Date: 2025-04-21 11:21:54.171052

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
import requests
from models.pokemon import Pokemon
from schemas.pokemon import pokemon_schema


# revision identifiers, used by Alembic.
revision = "bc7c5c07eada"
down_revision = "8aaeb165d8f3"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    try:

        # Create pokemons
        base_pokemons = [
            "pikachu",
            "dhelmise",
            "charizard",
            "parasect",
            "terodactyl",
            "kingler",
        ]
        pokemons_to_add = []
        for base_pokemon in base_pokemons:
            pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{base_pokemon}"
            print(f"Fetching data for {base_pokemon} from {pokemon_url}")
            response = requests.get(pokemon_url)
            if not response.ok:
                print(
                    f"Failed to fetch data for {base_pokemon}: {response.status_code}"
                )
                continue
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
            pokemons_to_add.append(Pokemon(**pokemon_data))
        session.add_all(pokemons_to_add)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    pass


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    try:
        session.query(Pokemon).all().delete(synchronize_session=False)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
