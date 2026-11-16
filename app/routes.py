
from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/clientes")
def clientes():
    return render_template("clientes.html")

@main.route("/profissionais")
def profissionais():
    return render_template("profissionais.html")

@main.route("/agendamentos")
def agendamentos():
    return render_template("agendamentos.html")
