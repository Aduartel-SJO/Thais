from flask import Blueprint, render_template, redirect, url_for, session
from ..models.Usuario import Usuario
dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates/')

@dashboard_bp.route('/')
def mesas():
    usuario = Usuario.query.first()
    return render_template('mesas.html', usuario=usuario)