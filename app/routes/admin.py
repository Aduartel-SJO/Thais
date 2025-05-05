from flask import Blueprint, render_template, redirect, request, url_for, session
from ..models.Usuario import Usuario
from ..models.Mesas import Mesa
from ..models.Notas import Nota
from ..models.Comidas import Comida, db
from ..models.Ingredientes import Ingrediente
from werkzeug.utils import secure_filename
import os
admin_bp = Blueprint('admin', __name__, template_folder='../templates/')

# Carpeta donde se guardarán las imágenes
CARPETA_IMG = 'static/img'
# Extensiones permitidas
EXTENSIONES = {'png', 'jpg', 'jpeg', 'gif'}

def Comprobar_Archivo(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in EXTENSIONES

@admin_bp.route("/lista_comida")
def lista_comida():
    comidas = Comida.query.all()
    return render_template("listaComida.html", comidas=comidas)

@admin_bp.route("/lista_comida/crear_comida", methods=['POST'])
def crear_comida():
    if request.method == 'POST':
        nombreComida = request.form["comidaNombre"]
        Alias = request.form["Alias"]
        precio = request.form["precio"]
        archivo = request.files['imagen']
        nombreArchivo = ""
        if archivo and Comprobar_Archivo(archivo.filename):
            nombreArchivo = secure_filename(archivo.filename)
            archivo.save(CARPETA_IMG, nombreArchivo)


        
    return redirect(url_for("admin.lista_comida"))


@admin_bp.route("/resumen")
def resumen():
    notas = Nota.query.all()
    return render_template("resumen.html")