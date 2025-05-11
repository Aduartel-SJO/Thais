from . import db


class ingredientes_plato(db.Model):
    __tablename__ = 'ingredientes_plato'
    id_ingrediente = db.Column(db.Integer,primary_key=True)
    id_comida = db.Column(db.Integer, primary_key=True)
