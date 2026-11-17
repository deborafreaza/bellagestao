
from datetime import date, time

import pytest

from app import create_app
from app.models import db, Cliente, Profissional, Servico, Agendamento


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


def test_criar_cliente(app):
    with app.app_context():
        cliente = Cliente(
            nome="Maria Silva",
            telefone="13999999999",
            email="maria@example.com"
        )

        db.session.add(cliente)
        db.session.commit()

        resultado = Cliente.query.first()

        assert resultado.nome == "Maria Silva"
        assert resultado.telefone == "13999999999"


def test_status_padrao_profissional(app):
    with app.app_context():
        profissional = Profissional(
            nome="Ana Souza"
        )

        db.session.add(profissional)
        db.session.commit()

        assert profissional.status == "ativo"


def test_status_padrao_servico(app):
    with app.app_context():
        servico = Servico(
            nome="Manicure",
            duracao_minutos=60
        )

        db.session.add(servico)
        db.session.commit()

        assert servico.status == "ativo"


def test_criar_agendamento_com_relacionamentos(app):
    with app.app_context():
        cliente = Cliente(
            nome="Maria Silva",
            telefone="13999999999"
        )

        profissional = Profissional(
            nome="Ana Souza"
        )

        servico = Servico(
            nome="Manicure",
            duracao_minutos=60
        )

        db.session.add_all([cliente, profissional, servico])
        db.session.commit()

        agendamento = Agendamento(
            data=date(2026, 11, 20),
            hora_inicio=time(10, 0),
            hora_fim=time(11, 0),
            id_cliente=cliente.id_cliente,
            id_profissional=profissional.id_profissional,
            id_servico=servico.id_servico
        )

        db.session.add(agendamento)
        db.session.commit()

        resultado = Agendamento.query.first()

        assert resultado.status == "agendado"
        assert resultado.cliente.nome == "Maria Silva"
        assert resultado.profissional.nome == "Ana Souza"
        assert resultado.servico.nome == "Manicure"
