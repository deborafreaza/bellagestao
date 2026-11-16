
import pytest
from sqlalchemy import inspect

from app import create_app
from app.models import db


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-key"
    })

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"BellaGest" in response.data


def test_database_tables_created(app):
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        assert "cliente" in tables
        assert "profissional" in tables
        assert "servico" in tables
        assert "agendamento" in tables
