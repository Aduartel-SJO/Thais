from flask import Blueprint, render_template, redirect, url_for, session
from ..models.Usuario import Usuario
auth_bp = Blueprint('auth', __name__, template_folder='../templates/')

@auth_bp.route('/')
def mesas():
    usuario = Usuario.query.first()
    return render_template('mesas.html', usuario=usuario)