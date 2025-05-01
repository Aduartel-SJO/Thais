from flask import Blueprint, render_template, redirect, url_for, session
from ..models.Usuario import Usuario
from ..models.Mesas import Mesa
dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates/')

@dashboard_bp.route('/')
def Dashboard_mesas():
    usuario = Usuario.query.first()
    Mesas = Mesa.query.all()
    return render_template('mesas.html', Mesas=Mesas ,usuario=usuario)

@dashboard_bp.route('/crear_nota/<int:id_mesa>/<string:nombre>')
def crearNota(id_mesa, nombre):
    return render_template('crear_nota.html', id_mesa=id_mesa, nombreMesa=nombre)