
from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/clientes")
def clientes():
    return render_template(
        "modulo.html",
        titulo="Clientes",
        descricao="Consulte e organize as informações das clientes do Salão Distak."
    )


@main.route("/profissionais")
def profissionais():
    return render_template(
        "modulo.html",
        titulo="Profissionais",
        descricao="Visualize e organize as profissionais do salão."
    )


@main.route("/agendamentos")
def agendamentos():
    return render_template(
        "modulo.html",
        titulo="Agendamentos",
        descricao="Organize os horários e atendimentos do Salão Distak."
    )
