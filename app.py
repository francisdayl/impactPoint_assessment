from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

API_DEFINITION = "/static/openapi_definition.yml"
SWAGGER_URL = "/api/docs"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_DEFINITION,
    config={"app_name": "Poke Impact API"},
)


def create_app(testing=False):
    app = Flask(__name__)
    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./poke_DB.db"

    db.init_app(app)
    ma.init_app(app)

    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    # Register blueprints
    from routes.pokemon import pokemon_bp
    from routes.api import api_pb

    app.register_blueprint(pokemon_bp, url_prefix="/pokemon")
    app.register_blueprint(api_pb, url_prefix="/api")
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    return app
