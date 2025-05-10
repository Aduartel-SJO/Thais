from . import db

class ComidaNota(db.Model):
    __tablename__ = 'comida_nota'

    id_comida_nota = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_nota = db.Column(db.Integer, db.ForeignKey('notas.id_nota', ondelete='CASCADE'), nullable=False)
    id_comida = db.Column(db.Integer, db.ForeignKey('comidas.id_comida', ondelete='CASCADE'), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    checked = db.Column(db.Boolean, nullable=False)
    precio = precio = db.Column(db.Numeric(5, 2), nullable=False)