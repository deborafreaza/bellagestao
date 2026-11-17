
import logging
from datetime import datetime, timedelta

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)

from .models import db, Cliente, Profissional, Servico, Agendamento

main = Blueprint("main", __name__)

logger = logging.getLogger(__name__)


@main.route("/")
def home():
    return render_template("index.html")


# ==========================
# MÓDULO DE CLIENTES
# ==========================

@main.route("/clientes", methods=["GET", "POST"])
def clientes():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()

        if not nome or not telefone:
            flash("Nome e telefone são obrigatórios.", "danger")

        elif len(nome) > 100 or len(telefone) > 20 or len(email) > 120:
            flash("Um ou mais campos excedem o tamanho permitido.", "danger")

        else:
            cliente = Cliente(
                nome=nome,
                telefone=telefone,
                email=email or None
            )

            try:
                db.session.add(cliente)
                db.session.commit()
                flash("Cliente cadastrado com sucesso!", "success")
                return redirect(url_for("main.clientes"))

            except Exception:
                db.session.rollback()
                logger.exception("Erro ao cadastrar cliente.")
                flash("Não foi possível cadastrar o cliente.", "danger")

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

        elif len(nome) > 100 or len(telefone) > 20 or len(email) > 120:
            flash("Um ou mais campos excedem o tamanho permitido.", "danger")

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
                logger.exception("Erro ao atualizar cliente.")
                flash("Não foi possível atualizar o cliente.", "danger")

    return render_template(
        "editar_cliente.html",
        cliente=cliente
    )


@main.route("/clientes/<int:id_cliente>/excluir", methods=["POST"])
def excluir_cliente(id_cliente):
    cliente = db.get_or_404(Cliente, id_cliente)

    possui_agendamentos = Agendamento.query.filter_by(
        id_cliente=id_cliente
    ).first()

    if possui_agendamentos:
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
        logger.exception("Erro ao excluir cliente.")
        flash("Não foi possível excluir o cliente.", "danger")

    return redirect(url_for("main.clientes"))


# ==========================
# MÓDULO DE PROFISSIONAIS
# ==========================

@main.route("/profissionais", methods=["GET", "POST"])
def profissionais():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()

        if not nome:
            flash("O nome da profissional é obrigatório.", "danger")

        elif len(nome) > 100 or len(telefone) > 20:
            flash("Um ou mais campos excedem o tamanho permitido.", "danger")

        else:
            profissional = Profissional(
                nome=nome,
                telefone=telefone or None
            )

            try:
                db.session.add(profissional)
                db.session.commit()
                flash("Profissional cadastrada com sucesso!", "success")
                return redirect(url_for("main.profissionais"))

            except Exception:
                db.session.rollback()
                logger.exception("Erro ao cadastrar profissional.")
                flash("Não foi possível cadastrar a profissional.", "danger")

    lista_profissionais = Profissional.query.order_by(
        Profissional.nome
    ).all()

    return render_template(
        "profissionais.html",
        profissionais=lista_profissionais
    )


@main.route(
    "/profissionais/<int:id_profissional>/editar",
    methods=["GET", "POST"]
)
def editar_profissional(id_profissional):
    profissional = db.get_or_404(Profissional, id_profissional)

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()

        if not nome:
            flash("O nome da profissional é obrigatório.", "danger")

        elif len(nome) > 100 or len(telefone) > 20:
            flash("Um ou mais campos excedem o tamanho permitido.", "danger")

        else:
            profissional.nome = nome
            profissional.telefone = telefone or None

            try:
                db.session.commit()
                flash("Profissional atualizada com sucesso!", "success")
                return redirect(url_for("main.profissionais"))

            except Exception:
                db.session.rollback()
                logger.exception("Erro ao atualizar profissional.")
                flash("Não foi possível atualizar a profissional.", "danger")

    return render_template(
        "editar_profissional.html",
        profissional=profissional
    )


@main.route(
    "/profissionais/<int:id_profissional>/status",
    methods=["POST"]
)
def alterar_status_profissional(id_profissional):
    profissional = db.get_or_404(Profissional, id_profissional)

    if profissional.status == "ativo":
        profissional.status = "inativo"
        flash("Profissional inativada com sucesso!", "success")
    else:
        profissional.status = "ativo"
        flash("Profissional ativada com sucesso!", "success")

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()
        logger.exception("Erro ao alterar status da profissional.")
        flash("Não foi possível alterar o status.", "danger")

    return redirect(url_for("main.profissionais"))


# ==========================
# MÓDULO DE AGENDAMENTOS
# ==========================

# ==========================
# MÓDULO DE SERVIÇOS
# ==========================

@main.route("/servicos", methods=["GET", "POST"])
def servicos():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        duracao = request.form.get("duracao_minutos", "").strip()

        if not nome or not duracao:
            flash("Nome e duração são obrigatórios.", "danger")

        elif len(nome) > 100:
            flash("O nome do serviço é muito longo.", "danger")

        else:
            try:
                duracao = int(duracao)

                if duracao <= 0:
                    raise ValueError

                servico = Servico(
                    nome=nome,
                    duracao_minutos=duracao
                )

                db.session.add(servico)
                db.session.commit()

                flash("Serviço cadastrado com sucesso!", "success")
                return redirect(url_for("main.servicos"))

            except ValueError:
                flash("Informe uma duração válida em minutos.", "danger")

            except Exception:
                db.session.rollback()
                logger.exception("Erro ao cadastrar serviço.")
                flash("Não foi possível cadastrar o serviço.", "danger")

    lista_servicos = Servico.query.order_by(Servico.nome).all()

    return render_template(
        "servicos.html",
        servicos=lista_servicos
    )


@main.route(
    "/servicos/<int:id_servico>/editar",
    methods=["GET", "POST"]
)
def editar_servico(id_servico):
    servico = db.get_or_404(Servico, id_servico)

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        duracao = request.form.get("duracao_minutos", "").strip()

        if not nome:
            flash("O nome do serviço é obrigatório.", "danger")

        elif len(nome) > 100:
            flash("O nome do serviço é muito longo.", "danger")

        else:
            try:
                duracao = int(duracao)

                if duracao <= 0:
                    raise ValueError

                servico.nome = nome
                servico.duracao_minutos = duracao

                db.session.commit()

                flash("Serviço atualizado com sucesso!", "success")
                return redirect(url_for("main.servicos"))

            except ValueError:
                flash("Informe uma duração válida em minutos.", "danger")

            except Exception:
                db.session.rollback()
                logger.exception("Erro ao atualizar serviço.")
                flash("Não foi possível atualizar o serviço.", "danger")

    return render_template(
        "editar_servico.html",
        servico=servico
    )


@main.route(
    "/servicos/<int:id_servico>/status",
    methods=["POST"]
)
def alterar_status_servico(id_servico):
    servico = db.get_or_404(Servico, id_servico)

    if servico.status == "ativo":
        servico.status = "inativo"
        mensagem = "Serviço inativado com sucesso!"
    else:
        servico.status = "ativo"
        mensagem = "Serviço ativado com sucesso!"

    try:
        db.session.commit()
        flash(mensagem, "success")

    except Exception:
        db.session.rollback()
        logger.exception("Erro ao alterar status do serviço.")
        flash("Não foi possível alterar o status.", "danger")

    return redirect(url_for("main.servicos"))


# ==========================
# MÓDULO DE AGENDAMENTOS
# ==========================

@main.route("/agendamentos", methods=["GET", "POST"])
def agendamentos():

    if request.method == "POST":
        id_cliente = request.form.get("id_cliente", "").strip()
        id_profissional = request.form.get("id_profissional", "").strip()
        id_servico = request.form.get("id_servico", "").strip()
        data_form = request.form.get("data", "").strip()
        hora_form = request.form.get("hora_inicio", "").strip()

        try:
            if not all([
                id_cliente,
                id_profissional,
                id_servico,
                data_form,
                hora_form
            ]):
                raise ValueError("Preencha todos os campos obrigatórios.")

            id_cliente = int(id_cliente)
            id_profissional = int(id_profissional)
            id_servico = int(id_servico)

            data_agendamento = datetime.strptime(
                data_form, "%Y-%m-%d"
            ).date()

            hora_inicio = datetime.strptime(
                hora_form, "%H:%M"
            ).time()

            cliente = db.get_or_404(Cliente, id_cliente)
            profissional = db.get_or_404(Profissional, id_profissional)
            servico = db.get_or_404(Servico, id_servico)

            if profissional.status != "ativo":
                raise ValueError("A profissional selecionada está inativa.")

            if servico.status != "ativo":
                raise ValueError("O serviço selecionado está inativo.")

            inicio_datetime = datetime.combine(
                data_agendamento, hora_inicio
            )

            fim_datetime = inicio_datetime + timedelta(
                minutes=servico.duracao_minutos
            )

            if fim_datetime.date() != data_agendamento:
                raise ValueError(
                    "O agendamento não pode ultrapassar a meia-noite."
                )

            hora_fim = fim_datetime.time()

            conflito = Agendamento.query.filter(
                Agendamento.data == data_agendamento,
                Agendamento.id_profissional == id_profissional,
                Agendamento.status != "cancelado",
                Agendamento.hora_inicio < hora_fim,
                Agendamento.hora_fim > hora_inicio
            ).first()

            if conflito:
                raise ValueError(
                    "A profissional já possui um agendamento nesse horário."
                )

            novo_agendamento = Agendamento(
                data=data_agendamento,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                id_cliente=cliente.id_cliente,
                id_profissional=profissional.id_profissional,
                id_servico=servico.id_servico
            )

            db.session.add(novo_agendamento)
            db.session.commit()

            flash("Agendamento cadastrado com sucesso!", "success")
            return redirect(url_for("main.agendamentos"))

        except ValueError as erro:
            db.session.rollback()
            flash(str(erro), "danger")

        except Exception:
            db.session.rollback()
            logger.exception("Erro ao cadastrar agendamento.")
            flash("Não foi possível cadastrar o agendamento.", "danger")

    lista_agendamentos = Agendamento.query.order_by(
        Agendamento.data,
        Agendamento.hora_inicio
    ).all()

    lista_clientes = Cliente.query.order_by(Cliente.nome).all()

    lista_profissionais = Profissional.query.filter_by(
        status="ativo"
    ).order_by(Profissional.nome).all()

    lista_servicos = Servico.query.filter_by(
        status="ativo"
    ).order_by(Servico.nome).all()

    return render_template(
        "agendamentos.html",
        agendamentos=lista_agendamentos,
        clientes=lista_clientes,
        profissionais=lista_profissionais,
        servicos=lista_servicos
    )


@main.route(
    "/agendamentos/<int:id_agendamento>/cancelar",
    methods=["POST"]
)
def cancelar_agendamento(id_agendamento):

    agendamento = db.get_or_404(Agendamento, id_agendamento)

    if agendamento.status == "cancelado":
        flash("Este agendamento já está cancelado.", "warning")
        return redirect(url_for("main.agendamentos"))

    try:
        agendamento.status = "cancelado"
        db.session.commit()
        flash("Agendamento cancelado com sucesso!", "success")

    except Exception:
        db.session.rollback()
        logger.exception("Erro ao cancelar agendamento.")
        flash("Não foi possível cancelar o agendamento.", "danger")

    return redirect(url_for("main.agendamentos"))
