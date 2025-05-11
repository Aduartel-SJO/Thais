from flask import Blueprint, render_template, redirect, request, url_for, session

from ..models.ingredientes_plato import ingredientes_plato
from ..models.Usuario import Usuario
from ..models.Mesas import Mesa
from ..models.Notas import Nota, db
from ..models.Comida_nota import ComidaNota
from ..models.Comidas import Comida
from ..models.Ingredientes import Ingrediente
from datetime import datetime
dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates/')
#metodo que abre la pestaña de mesas
@dashboard_bp.route('/mesas')
def Dashboard_mesas():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    usuario = Usuario.query.first()
    mesas = Mesa.query.order_by(Mesa.nombre).all() #coge las mesas y las ordena segun el nombre
    return render_template('mesas.html', Mesas=mesas ,usuario=usuario)

#Abre la ventana para añadir "platos" a la nota
@dashboard_bp.route('/comida_bebida/<int:id_nota>')
def comida_bebida(id_nota):
    if "user" not in session:
        return redirect(url_for("auth.login"))
    #obtenemos la comida y ingredientes
    comidas = Comida.query.all()
    ingredientes = Ingrediente.query.all()
    for comida in comidas:
         #cogemos los ingredientes de la comida y lo guardamos como un atributo
         comida.ingredientes = ingredientes_plato.query.filter(ingredientes_plato.id_comida == comida.id_comida).all()
         comida.ingredientes_ids = [i.id_ingrediente for i in comida.ingredientes]
            
    return render_template("comidaBebida.html", id_nota=id_nota, comidas=comidas, ingredientes=ingredientes)    

#metodo que añade la nueva comida seleccionada a la nota
@dashboard_bp.route('/comida_bebida/anadire/<int:id_nota>/<int:id_comida>', methods=['POST'])
def anadir_comida_nota(id_nota, id_comida):
    if request.method == 'POST':
        cantidad = request.form.get("cantidad")
        ingredientes = request.form.getlist("ingredientes[]")
        #buscamos la comida
        comida = Comida.query.filter(Comida.id_comida == id_comida).first()
        ingrediente_comida = Ingrediente.query.filter(Ingrediente.id_ingrediente == comida.id_comida).all()
        nombre=comida.nombre
        print(nombre)
        if ingredientes:
                for ing in ingredientes:
                    nombre = nombre + " " +  ing
        nueva_nota_comida = ComidaNota(
            id_nota = id_nota,
            id_comida = id_comida,
            nombre = nombre,
            cantidad = cantidad,
            checked = False,
            precio = comida.precio
        )
        db.session.add(nueva_nota_comida)
        db.session.commit()


    return redirect(url_for("dashboard.abrir_nota", id_nota=id_nota))

#metodo para elimanar una comida de la comanda
@dashboard_bp.route("/delete/comida_nota/<int:id_comida_nota>/<int:id_nota>" , methods=['POST'])
def delete_comida_nota(id_comida_nota,id_nota):
    if request.method == 'POST':
         #obtenemos la nota/comida para cambiar el estado
        comida_nota =  ComidaNota.query.filter(ComidaNota.id_comida_nota == id_comida_nota).first()
        db.session.delete(comida_nota)
        db.session.commit()
    return redirect(url_for("dashboard.abrir_nota", id_nota=id_nota))

#metodo que nos permite marcar como terminado o falta, las comidas de la nota
@dashboard_bp.route('/check/<int:id_comida_nota>/<int:id_nota>' , methods=['POST'])
def check_comida(id_comida_nota, id_nota):
    if request.method == 'POST':
        #obtenemos la nota/comida para cambiar el estado
        comida_nota =  ComidaNota.query.filter(ComidaNota.id_comida_nota == id_comida_nota).first()
        print(comida_nota)
        if comida_nota.checked == 1:
            comida_nota.checked = 0
        else:
            comida_nota.checked = 1
        db.session.commit()
    return redirect(url_for("dashboard.abrir_nota", id_nota=id_nota))

# metod que habre la ventana de la nota especifica
@dashboard_bp.route('/nota_especifica/<int:id_nota>')
def abrir_nota(id_nota):
    if "user" not in session:
        return redirect(url_for("auth.login"))
    # buscamos la nota activa de la mesa
    nota = Nota.query.filter(Nota.id_nota == id_nota, Nota.is_Active == 1).first()
    #obtenemos la mesa 
    mesa = Mesa.query.filter(Mesa.id_mesa == nota.id_mesa).first()
    #obtener todos los registros de comida de la nota
    nota_comida = ComidaNota.query.filter(ComidaNota.id_nota == nota.id_nota).all()


    return render_template("nota_especifica.html", mesa=mesa, nota=nota, nota_comida=nota_comida)

#metodo que crea la nota y nos redirije a la ventana de dicha nota
@dashboard_bp.route('/crear_nota/<int:id_mesa>', )
def crearNota(id_mesa):
        if "user" not in session:
            return redirect(url_for("auth.login"))
    # buscamos la nota activa de la mesa
        nota = Nota.query.filter(Nota.id_mesa == id_mesa, Nota.is_Active == 1).first()
        #
        if not nota or nota.id_nota == 99 :
            nueva_nota = Nota(
                id_mesa=id_mesa,
                fecha= datetime.now(),
                is_Active = 1
            )
            db.session.add(nueva_nota)
            db.session.commit()
            id_generado = nueva_nota.id_nota
            return redirect(url_for("dashboard.abrir_nota", id_nota=id_generado))
        else:
            return redirect(url_for("dashboard.abrir_nota", id_nota=nota.id_nota))