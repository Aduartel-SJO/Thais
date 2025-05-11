from flask import Blueprint, render_template, redirect, url_for, session, request
from ..models.Usuario import Usuario
auth_bp = Blueprint('auth', __name__, template_folder='../templates/')
import bcrypt

@auth_bp.route('/', methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for('dashboard.Dashboard_mesas'))

    if request.method == "POST":
        #cojemos los valores del form 
        email = request.form["email"]
        contrasena = request.form["contrasena"]
        # buscamos al usuario
        usuario_encontrado = Usuario.query.filter_by(email=email).first()
        # si el usuario existe y las contraseñas coinciden se crean las variables de sesion y se pasa a la pagina de mesas
        if usuario_encontrado and bcrypt.checkpw(contrasena.encode("utf-8"), usuario_encontrado.contrasena.encode("utf-8")):
            session["user"] = usuario_encontrado.id_usuario
            session["is_admin"] = usuario_encontrado.is_Admin
            user_id = session["user"]

            return redirect(url_for("dashboard.Dashboard_mesas"))
        # si te equivocas se vuelve a abrir el login pero con un error
        return render_template("login.html", error="Credenciales incorrectas")
    
    return render_template("login.html")