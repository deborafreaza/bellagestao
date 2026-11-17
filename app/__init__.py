
import os
from flask import Flask
from .models import db
from .routes import main


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get(
            "SECRET_KEY", "chave-temporaria-desenvolvimento"
        ),
        SQLALCHEMY_DATABASE_URI="sqlite:///bellagestao.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
