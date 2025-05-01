from . import db

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'

    id_ingrediente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_comida = db.Column(db.Integer, db.ForeignKey('comidas.id_comida', ondelete='CASCADE'), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)