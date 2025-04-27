from . import db

class Comida(db.Model):
    __tablename__ = 'comidas'

    id_comida = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50))
    tipo = db.Column(db.Enum('Comida', 'Bebida', name='tipo_comida_enum'))
    precio = db.Column(db.Numeric(5, 2), nullable=False)
    imagen = db.Column(db.TEXT)

    ingredientes = db.relationship('Ingrediente', backref='comida', cascade='all, delete')
    comida_nota = db.relationship('ComidaNota', backref='comida', cascade='all, delete')
