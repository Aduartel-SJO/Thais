import bcrypt
from flask import Blueprint, render_template, redirect, request, url_for, session
from ..models.Usuario import Usuario
from ..models.Mesas import Mesa
from ..models.Notas import Nota
from ..models.Comidas import Comida, db
from ..models.ingredientes_plato import ingredientes_plato
from ..models.Ingredientes import Ingrediente
from ..models.Usuario import Usuario
from ..models.Comida_nota import ComidaNota
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
admin_bp = Blueprint('admin', __name__, template_folder='../templates/')

# Carpeta donde se guardarán las imágenes
CARPETA_IMG = 'app/static/img'
# Extensiones permitidas
EXTENSIONES = {'png', 'jpg', 'jpeg', 'gif'}

def Comprobar_Archivo(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in EXTENSIONES

# zona Comida
@admin_bp.route("/lista_comida")
def lista_comida():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    comidas = Comida.query.all()
    ingredientes = Ingrediente.query.all()
    
    for comida in comidas:
        #obtener los ingredientes por comidas
        comida.ingredientes = ingredientes_plato.query.filter(ingredientes_plato.id_comida == comida.id_comida).all()
        comida.ingredientes_ids = [i.id_ingrediente for i in comida.ingredientes]

    return render_template("listaComida.html", comidas=comidas, ingredientes=ingredientes)

# metodo para crear comida
@admin_bp.route("/lista_comida/crear_comida", methods=['POST'])
def crear_comida():
    if request.method == 'POST':
        nombreComida = request.form.get("comidaNombre")
        Alias = request.form.get("Alias")
        precio = request.form.get("precio", 0)
        tipo = request.form.get("TipoComida")
        archivo = request.files.get('imagen')
        nombreArchivo = ""
        ruta_completa = ""
        #crea el archivo si no existe 
        if archivo and Comprobar_Archivo(archivo.filename):
            nombreArchivo = secure_filename(archivo.filename)
            ruta_completa = os.path.join(CARPETA_IMG, nombreArchivo)
            if not os.path.exists(ruta_completa):
                archivo.save(ruta_completa)
        nuevaComida = Comida(
            nombre = nombreComida,
            alias = Alias,
            tipo = tipo,
            precio = precio,
            imagen = f"img/{nombreArchivo}"
        )
        db.session.add(nuevaComida)
        db.session.commit()
        
    return redirect(url_for("admin.lista_comida"))

#metodo para elimar la comida
@admin_bp.route("/lista_comida/eliminar_comida/<int:id_comida>" , methods=['POST'])
def eliminar_comida(id_comida):
    if request.method == 'POST':
        #cojemos la comida en cuestion
        comida = Comida.query.filter(Comida.id_comida == id_comida).first()
        # cojemos los ingredientes asignados y tambien los eliminamos
        comida_ing = ingredientes_plato.query.filter(ingredientes_plato.id_comida == id_comida).all()
        for ig in comida_ing:
            db.session.delete(ig)
        db.session.delete(comida)
        db.session.commit()
    return redirect(url_for("admin.lista_comida"))

#metodo para editar los valores de la comida
@admin_bp.route("/lista_comida/editar_comida/<int:id_comida>", methods=['POST'])
def editar_comida(id_comida):
    if request.method == 'POST':
        # coge la comida en cuestion
        comida = Comida.query.filter(Comida.id_comida == id_comida).first()
        if comida:
            nombreComida = request.form.get("comidaNombre")
            Alias = request.form.get("Alias")
            precio = request.form.get("precio", 0)
            tipo = request.form.get("TipoComida")
            archivo = request.files.get('imagen')
            nombreArchivo = ""
            ruta_completa = ""
            #crea el archivo si no existe 
            if archivo and Comprobar_Archivo(archivo.filename):
                nombreArchivo = secure_filename(archivo.filename)
                ruta_completa = os.path.join(CARPETA_IMG, nombreArchivo)
                if not os.path.exists(ruta_completa):
                    archivo.save(ruta_completa)

            comida.nombre = nombreComida
            comida.alias = Alias
            comida.tipo = tipo
            comida.precio =precio
            if comida.imagen != ruta_completa and ruta_completa != "":
                comida.imagen = f"img/{nombreArchivo}"
            db.session.commit()
        
    return redirect(url_for("admin.lista_comida"))

@admin_bp.route("/lista_comida/AnadirIngredientes/<int:id_comida>", methods=['POST'])
#metodo para añafir ingredientes al plato
def anadir_ingredientes_plato(id_comida):
    if request.method == 'POST':
        ingredientes = request.form.getlist('ingredientes[]')
        print(ingredientes)
        print(id_comida)
        #cogemos los que ya tenia y los eliminamos para volver a crearlos
        ip = ingredientes_plato.query.filter(ingredientes_plato.id_comida == id_comida).all()
        for i in ip:
            db.session.delete(i)
            db.session.commit()
        for ingrediente in  ingredientes:
            print(ip)
            nuevoIngredientePlato = ingredientes_plato (
                id_comida = id_comida,
                id_ingrediente = ingrediente
            )
            db.session.add(nuevoIngredientePlato)
            db.session.commit()
    return redirect(url_for("admin.lista_comida"))

#zona resumen
@admin_bp.route("/resumen", methods=['POST','GET'])
def resumen():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    desde_str = request.form.get("desde")
    hasta_str = request.form.get("hasta")

    # Procesar fechas con valores por defecto si no se envían
    if desde_str:
        desde = datetime.strptime(desde_str, "%Y-%m-%d")
    else:
        desde = datetime.now()

    if hasta_str:
        hasta = datetime.strptime(hasta_str, "%Y-%m-%d")
    else:
        hasta = desde + timedelta(days=30)
    #cogemos las nostas entre las dos fechas
    notas = Nota.query.filter(Nota.fecha >= desde, Nota.fecha <= hasta).all()
    #total de notas
    total_notas = len(notas)
    dinero_total = 0
    for nota in notas:
        #cogemos todas los "platos" por nota
        comidas_nota = ComidaNota.query.filter(ComidaNota.id_nota == nota.id_nota).all()
        for cn in comidas_nota:
            dinero_total=dinero_total + cn.precio
    
    promedio_mesa = round(dinero_total / int(total_notas), 2) if total_notas > 0 else 0
    return render_template("resumen.html", promedio_mesa=promedio_mesa, total_notas=total_notas, dinero_total=dinero_total, desde=desde_str, hasta=hasta_str )




# Zona MESAS
@admin_bp.route("/lista_mesas")
#metodo que abre la pestaña de mesas
def lista_mesas():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    mesas = Mesa.query.order_by(Mesa.nombre).all() #coge las mesas y las ordena segun el nombre
    return render_template("listaMesas.html", mesas=mesas)

@admin_bp.route("/lista_mesas/editar/<int:id_mesa>", methods=['POST'])
#metodo para editar mesas
def editar_mesa(id_mesa):
    if request.method == "POST":
        #coje la mesa en cuestion
        mesa = Mesa.query.filter(Mesa.id_mesa==id_mesa).first()
        if mesa:
            #cogemos los valores
            nombreMesa = request.form.get("nombreMesa")
            #buscamos la mesa
            #cambiamos el nombre
            mesa.nombre = nombreMesa

            db.session.commit() #guardamos los cambios

    return redirect(url_for("admin.lista_mesas"))

@admin_bp.route("/lista_mesas/añadir", methods=['POST'])
#metodo para crear mesas
def Añadir_mesa():
    if request.method == "POST":
        nombreMesa = request.form.get("nombreMesa")
        #nueva mesa
        nuevaMesa = Mesa(nombre=nombreMesa) #creamos la nueva mesa

        db.session.add(nuevaMesa) 
        db.session.commit() #guardamos los cambios
    return redirect(url_for("admin.lista_mesas"))

#metodo para eliminar mesas
@admin_bp.route("/lista_mesas/eliminar/<int:id_mesa>", methods=['POST'])
def delete_mesas(id_mesa):
    if request.method == "POST":
        #coje la mesa en cuestion
        mesa = Mesa.query.filter(Mesa.id_mesa==id_mesa).first()
        if mesa:
            db.session.delete(mesa)
            db.session.commit()
    return redirect(url_for("admin.lista_mesas"))


#Zona de ingredientes
@admin_bp.route("/lista_ingredientes")
#metodo que abre la pestaña de mesas
def lista_ingredientes():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    ingredientes = Ingrediente.query.all() #coge todos los ingredientes
    return render_template("listaIngredientes.html", ingredientes=ingredientes)

@admin_bp.route("/lista_ingredientes/editar/<int:id_ingrediente>", methods=['POST'])
#metodo para editar mesas
def editar_ingredientes(id_ingrediente):
    if request.method == "POST":
        ingrediente = Ingrediente.query.filter(Ingrediente.id_ingrediente==id_ingrediente).first()
        if ingrediente:
            #cogemos los valores
            nombreIngrediente = request.form.get("nombreIngrediente")
            #cambiamos el nombre
            ingrediente.nombre = nombreIngrediente

            db.session.commit() #guardamos los cambios

    return redirect(url_for("admin.lista_ingredientes"))
#meto para añadir ingredientes
@admin_bp.route("/lista_ingredientes/añadir", methods=['POST'])
def Añadir_ingrediente():
    if request.method == "POST":
        nombreIngrediente = request.form.get("nombreIngrediente")
        #nuevo ingrediente
        nuevoIngrediente = Ingrediente(nombre=nombreIngrediente) #creamos el ingrediente

        db.session.add(nuevoIngrediente) 
        db.session.commit() #guardamos los cambios
    return redirect(url_for("admin.lista_ingredientes"))
# metodo para eliminar ingredientes
@admin_bp.route("/lista_ingredientes/eliminar/<int:id_ingrediente>", methods=['POST'])
def delete_ingrediente(id_ingrediente):
    if request.method == "POST":
        #cojo el ingrediente para eliminarlo
        ingrediente = Ingrediente.query.filter(Ingrediente.id_ingrediente==id_ingrediente).first()
        if ingrediente:
            #cojo todos los registros que estuvieran con los platos y lugo los elimino
            ip = ingredientes_plato.query.filter(ingredientes_plato.id_ingrediente == ingrediente.id_ingrediente).all()  
            for i in ip:
                db.session.delete(i)        
            db.session.delete(ingrediente)
            db.session.commit()
    return redirect(url_for("admin.lista_ingredientes"))


#Zona Usuarios
@admin_bp.route("/usuarios")
def lista_Usuarios():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    # cogemos todos los usuarios
    usuarios = Usuario.query.all()
    return render_template("listaUsuarios.html", usuarios=usuarios)
#metodo para añadir usuarios
@admin_bp.route("/usuarios/anadir",  methods=['POST'] )
def anadir_usuario():
    if request.method == "POST":
        nombre = request.form.get("nombreUsuario")
        email = request.form.get("email")
        contrasena = request.form.get("contrasena")
        is_admin = int(request.form.get("is_admin"))
        contrasena_encriptada = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())
        nuevoUsuario = Usuario(
            nombre = nombre,
            email=email,
            is_Admin= is_admin,
            contrasena=contrasena_encriptada
        )
        db.session.add(nuevoUsuario)
        db.session.commit()
    return redirect(url_for("admin.lista_Usuarios"))

# metodo para editar usuarios
@admin_bp.route("/usuarios/editar/<int:id_usuario>",  methods=['POST'])
def editar_usuario(id_usuario):
    if request.method == "POST":
        #cojemos el usuario
        usuario = Usuario.query.filter(Usuario.id_usuario == id_usuario).first()
        if usuario:
            nombre = request.form.get("nombreUsuario")
            email = request.form.get("email")
            contrasena = request.form.get("contrasena")
            is_admin = int(request.form.get("is_admin"))
            if contrasena != "":
                usuario.contrasena  = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())
            usuario.nombre = nombre
            usuario.email = email
            usuario.is_Admin = is_admin

            db.session.commit()

    return redirect(url_for("admin.lista_Usuarios"))

#metodo para eliminar usuarios
@admin_bp.route("/usuarios/eliminar/<int:id_usuario>",  methods=['POST'])
def eliminar_usuario(id_usuario):
    if request.method == "POST":
        #cojemos al usuario y lo eliminamos
        usuario = Usuario.query.filter(Usuario.id_usuario == id_usuario).first()
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
    return redirect(url_for("admin.lista_Usuarios"))