from . import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    contrasena = db.Column(db.String(100), nullable=False)
    is_Admin = db.Column(db.Boolean, nullable=False)