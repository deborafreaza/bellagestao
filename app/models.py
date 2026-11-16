
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cliente(db.Model):
    id_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))


class Profissional(db.Model):
    id_profissional = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    status = db.Column(db.String(10), nullable=False, default="ativo")


class Servico(db.Model):
    id_servico = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    duracao_minutos = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False, default="ativo")


class Agendamento(db.Model):
    id_agendamento = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(15), nullable=False, default="agendado")

    id_cliente = db.Column(
        db.Integer, db.ForeignKey("cliente.id_cliente"), nullable=False
    )
    id_profissional = db.Column(
        db.Integer, db.ForeignKey("profissional.id_profissional"), nullable=False
    )
    id_servico = db.Column(
        db.Integer, db.ForeignKey("servico.id_servico"), nullable=False
    )

    cliente = db.relationship("Cliente")
    profissional = db.relationship("Profissional")
    servico = db.relationship("Servico")
