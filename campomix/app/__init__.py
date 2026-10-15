
from datetime import timedelta

from flask import (
    Flask, redirect, url_for,
    session, render_template
)

from config import Config

from app.controllers.auth_controller import auth_bp
from app.controllers.proveedor_controller import proveedor_bp

from app.controllers.materia_prima_controller import materia_prima_bp
from app.controllers.recepcion_mp_controller import recepcion_mp_bp
from app.controllers.lote_mp_controller import lote_mp_bp
from app.controllers.inventario_mp_controller import inventario_mp_bp
from app.controllers.categoria_producto_controller import categoria_producto_bp
from app.controllers.producto_controller import producto_bp
from app.controllers.receta_controller import receta_bp








def create_app():

    app = Flask(__name__)

    # Configuración general
    app.config.from_object(Config)
    

    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
        minutes=30
    )

    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # Registrar controladores
    app.register_blueprint(auth_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(materia_prima_bp)
    app.register_blueprint(recepcion_mp_bp)
    app.register_blueprint(lote_mp_bp)
    app.register_blueprint(inventario_mp_bp)
    app.register_blueprint(categoria_producto_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(receta_bp)

    # Página principal
    @app.route("/")
    def inicio():

        if "usuario_id" in session:
            return redirect(url_for("dashboard"))

        return redirect(url_for("auth.login"))

    # Dashboard
    @app.route("/dashboard")
    def dashboard():

        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))

        return render_template("dashboard.html")

    return app
