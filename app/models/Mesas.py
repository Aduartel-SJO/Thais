from . import db

class Mesa(db.Model):
    __tablename__ = 'mesas'
    id_mesa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)