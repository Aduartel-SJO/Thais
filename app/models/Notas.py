from . import db

class Nota(db.Model):
    __tablename__ = 'notas'

    id_nota = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_mesa = db.Column(db.Integer, db.ForeignKey('mesas.id_mesa', ondelete='CASCADE'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    is_Active = db.Column(db.Boolean, nullable=False)

    comidas_nota = db.relationship('ComidaNota', backref='nota', cascade='all, delete')