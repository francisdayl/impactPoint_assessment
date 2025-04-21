from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./poke_DB.db"

    db.init_app(app)
    ma.init_app(app)

    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    # Register blueprints
    from routes.pokemon import pokemon_pb

    app.register_blueprint(pokemon_pb, url_prefix="/pokemon")

    return app
