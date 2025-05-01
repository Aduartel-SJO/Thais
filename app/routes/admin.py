from flask import Blueprint, render_template, redirect, url_for, session
from ..models.Usuario import Usuario
from ..models.Mesas import Mesa
from ..models.Comidas import Comida
from werkzeug.utils import secure_filename
import os
admin_bp = Blueprint('admin', __name__, template_folder='../templates/')

@admin_bp.route("/lista_comida")
def crear_comida():
    comidas = Comida.query.all()
    return render_template("listaComida.html", comidas=comidas)