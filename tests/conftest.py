import pytest

from app import create_app, db


@pytest.fixture()
def app_created():
    app_created = create_app(testing=True)
    with app_created.app_context():
        # Create the database and the database table
        db.create_all()

        yield app_created

        # Teardown: Drop all tables
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app_created):
    return app_created.test_client()
