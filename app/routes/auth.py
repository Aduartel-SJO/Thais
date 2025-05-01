from flask import Blueprint, render_template, redirect, url_for, session, request
from ..models.Usuario import Usuario
auth_bp = Blueprint('auth', __name__, template_folder='../templates/')
import bcrypt

@auth_bp.route('/', methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form["email"]
        contrasena = request.form["contrasena"]

        usuario_encontrado = Usuario.query.filter_by(email=email).first()

        if usuario_encontrado and bcrypt.checkpw(contrasena.encode("utf-8"), usuario_encontrado.contrasena.encode("utf-8")):
            session["user"] = usuario_encontrado.id_usuario
            session["is_admin"] = usuario_encontrado.is_admin
            user_id = session["user"]

            return redirect(url_for("dashboard.Dashboard_mesas"))

        return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")