
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Cliente, Agendamento

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/clientes", methods=["GET", "POST"])
def clientes():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()

        if not nome or not telefone:
            flash("Nome e telefone são obrigatórios.", "danger")
            return redirect(url_for("main.clientes"))

        cliente = Cliente(
            nome=nome,
            telefone=telefone,
            email=email or None
        )

        try:
            db.session.add(cliente)
            db.session.commit()
            flash("Cliente cadastrado com sucesso!", "success")
        except Exception:
            db.session.rollback()
            flash("Não foi possível cadastrar o cliente.", "danger")

        return redirect(url_for("main.clientes"))

    lista_clientes = Cliente.query.order_by(Cliente.nome).all()

    return render_template(
        "clientes.html",
        clientes=lista_clientes
    )


@main.route("/clientes/<int:id_cliente>/editar", methods=["GET", "POST"])
def editar_cliente(id_cliente):
    cliente = db.get_or_404(Cliente, id_cliente)

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()

        if not nome or not telefone:
            flash("Nome e telefone são obrigatórios.", "danger")
        else:
            cliente.nome = nome
            cliente.telefone = telefone
            cliente.email = email or None

            try:
                db.session.commit()
                flash("Cliente atualizado com sucesso!", "success")
                return redirect(url_for("main.clientes"))
            except Exception:
                db.session.rollback()
                flash("Não foi possível atualizar o cliente.", "danger")

    return render_template("editar_cliente.html", cliente=cliente)


@main.route("/clientes/<int:id_cliente>/excluir", methods=["POST"])
def excluir_cliente(id_cliente):
    cliente = db.get_or_404(Cliente, id_cliente)

    if Agendamento.query.filter_by(id_cliente=id_cliente).first():
        flash(
            "Este cliente possui agendamentos e não pode ser excluído.",
            "warning"
        )
        return redirect(url_for("main.clientes"))

    try:
        db.session.delete(cliente)
        db.session.commit()
        flash("Cliente excluído com sucesso!", "success")
    except Exception:
        db.session.rollback()
        flash("Não foi possível excluir o cliente.", "danger")

    return redirect(url_for("main.clientes"))


@main.route("/profissionais")
def profissionais():
    return render_template(
        "modulo.html",
        titulo="Profissionais",
        descricao="Consulte e organize as informações das profissionais do salão."
    )


@main.route("/agendamentos")
def agendamentos():
    return render_template(
        "modulo.html",
        titulo="Agendamentos",
        descricao="Organize os horários, serviços, clientes e profissionais do salão."
    )
