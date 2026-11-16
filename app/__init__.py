
from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "chave-temporaria-desenvolvimento"

    @app.route("/")
    def home():
        return "BellaGestão - Sistema de gerenciamento do Salão Distak"

    return app
