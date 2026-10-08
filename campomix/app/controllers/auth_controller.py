
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash
)
from werkzeug.security import check_password_hash

from app.models.usuario_model import UsuarioModel

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if "usuario_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")

        if not usuario or not password:
            flash("Complete todos los campos.", "warning")
            return render_template("auth/login.html")

        datos = UsuarioModel.buscar_por_usuario(usuario)

        if datos and check_password_hash(
            datos["password_hash"], password
        ):

            if not datos["activo"] or not datos["rol_activo"]:
                flash("Su cuenta no está activa.", "danger")
                return render_template("auth/login.html")

            session.clear()

            session["usuario_id"] = datos["id_usuario"]
            session["nombre"] = datos["nombre_completo"]
            session["rol"] = datos["rol"]

            return redirect(url_for("dashboard"))

        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))
