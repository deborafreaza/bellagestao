
import os
from flask import Flask
from .models import db


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "chave-temporaria-desenvolvimento"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bellagestao.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return "BellaGestão - Sistema de gerenciamento do Salão Distak"

    return app
