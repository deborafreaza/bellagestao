
from flask import Blueprint

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return """
    <h1>BellaGestão</h1>
    <h2>Salão Distak</h2>
    <p>Sistema de gerenciamento de agendamentos.</p>
    <p>Bem-vindo ao BellaGestão!</p>
    """
