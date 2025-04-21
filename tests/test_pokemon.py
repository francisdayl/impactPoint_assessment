def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_get_all_pokemon_404(client):
    """Test the health check endpoint."""
    response = client.get("/pokemon/all")
    assert response.status_code == 404


def test_get_unexistent_pokemon_by_id(client):
    """Test the get unexistent pokemon by id endpoint."""
    response = client.get("/pokemon/999999")
    assert response.status_code == 404


def test_get_unexistent_pokemon_by_name(client):
    """Test the get unexistent pokemon by name endpoint."""
    response = client.get("/pokemon/Terodactyl")
    assert response.status_code == 404


def test_get_pokemon_by_id(client):
    """Test the get pokemon by id endpoint."""
    client.post("/pokemon/create-by-name", json={"name": "bulbasaur"})
    response = client.get("/pokemon/1")
    assert response.status_code == 200
    assert response.json["name"] == "bulbasaur"


def test_get_pokemon_by_name(client):
    """Test the get pokemon by name endpoint."""
    client.post("/pokemon/create-by-name", json={"name": "bulbasaur"})
    response = client.get("/pokemon/bulbasaur")
    assert response.status_code == 200
    assert response.json["name"] == "bulbasaur"


def test_create_pokemon_by_name(client):
    """Test the create pokemon by name endpoint."""
    response = client.post("/pokemon/create-by-name", json={"name": "pikachu"})
    assert response.status_code == 201
    assert response.json["name"] == "pikachu"


def test_create_pokemon(client):
    """Test the create pokemon"""
    payload = {
        "name": "pikachu",
        "height": 4,
        "weight": 60,
        "base_experience": 112,
        "location_area_encounters": "https://pokeapi.co/api/v2/pokemon/25/encounters",
    }
    response = client.post("/pokemon/create", json=payload)
    assert response.status_code == 201
    assert response.json["name"] == "pikachu"
    assert response.json["height"] == 4
    assert response.json["weight"] == 60
    assert response.json["base_experience"] == 112
    assert (
        response.json["location_area_encounters"]
        == "https://pokeapi.co/api/v2/pokemon/25/encounters"
    )


def test_create_pokemon_validation_failure(client):
    """Test the create pokemon validation"""
    payload = {
        "name": "pikachu",
        "height": 4,
        "weight": 60,
    }
    response = client.post("/pokemon/create", json=payload)
    assert response.status_code == 400


def test_pokemon_report(client):
    """Test the pokemon report endpoint."""
    client.post("create-by-name", json={"name": "pikachu"})
    client.post("create-by-name", json={"name": "charizard"})
    response = client.get("/pokemon/report")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/csv; charset=utf-8"
    assert (
        response.headers["Content-Disposition"]
        == "attachment;filename=pokemons_data.csv"
    )
