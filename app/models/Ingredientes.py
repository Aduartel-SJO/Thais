from . import db

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'

    id_ingrediente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)