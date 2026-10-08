
import re

from functools import wraps
from mysql.connector import IntegrityError

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, abort
)

from app.models.proveedor_model import ProveedorModel


proveedor_bp = Blueprint(
    "proveedores",
    __name__,
    url_prefix="/proveedores"
)


def login_requerido(funcion):
    @wraps(funcion)
    def decorador(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        return funcion(*args, **kwargs)
    return decorador


@proveedor_bp.route("/")
@login_requerido
def listar():

    busqueda = request.args.get(
        "buscar", ""
    ).strip()

    proveedores = ProveedorModel.listar(busqueda)

    return render_template(
        "proveedores/listar.html",
        proveedores=proveedores,
        busqueda=busqueda
    )



def obtener_datos():
    return {
        "razon_social": request.form.get(
            "razon_social", ""
        ).strip(),

        "nit": request.form.get(
            "nit", ""
        ).strip(),

        "contacto": request.form.get(
            "contacto", ""
        ).strip(),

        "telefono": request.form.get(
            "telefono", ""
        ).strip(),

        "correo": request.form.get(
            "correo", ""
        ).strip().lower(),

        "direccion": request.form.get(
            "direccion", ""
        ).strip()
    }


def validar_proveedor(datos, excluir_id=None):
    errores = []

    limites = {
        "razon_social": 160,
        "nit": 30,
        "contacto": 120,
        "telefono": 30,
        "correo": 150,
        "direccion": 255
    }

    etiquetas = {
        "razon_social": "Razón social",
        "nit": "NIT",
        "contacto": "Contacto",
        "telefono": "Teléfono",
        "correo": "Correo",
        "direccion": "Dirección"
    }

    # Campos obligatorios
    for campo, etiqueta in etiquetas.items():
        if not datos[campo]:
            errores.append(
                f"El campo {etiqueta} es obligatorio."
            )
        elif len(datos[campo]) > limites[campo]:
            errores.append(
                f"El campo {etiqueta} es demasiado largo."
            )

    # Validación del NIT
    nit = datos["nit"]

    if nit:
        if not re.fullmatch(r"[0-9]{5,15}", nit):
            errores.append(
                "El NIT debe tener entre 5 y 15 dígitos."
            )
        elif ProveedorModel.existe_nit(
            nit, excluir_id
        ):
            errores.append(
                "El NIT ya está registrado."
            )

    # Validación del correo
    correo = datos["correo"]

    if correo:
        patron = r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(patron, correo):
            errores.append(
                "Ingrese un correo electrónico válido."
            )
        elif ProveedorModel.existe_correo(
            correo, excluir_id
        ):
            errores.append(
                "El correo electrónico ya está registrado."
            )

    # Validación del teléfono
    telefono = datos["telefono"]

    if telefono and not re.fullmatch(
        r"[0-9]{7,15}", telefono
    ):
        errores.append(
            "El teléfono debe tener entre 7 y 15 dígitos."
        )

    return errores




@proveedor_bp.route("/nuevo", methods=["GET", "POST"])
@login_requerido
def nuevo():

    if request.method == "POST":

        datos = obtener_datos()
        errores = validar_proveedor(datos)

        if errores:
            for error in errores:
                flash(error, "danger")

            return render_template(
                "proveedores/formulario.html",
                proveedor=datos
            )

        try:
            ProveedorModel.crear(datos)

            flash(
                "Proveedor registrado correctamente.",
                "success"
            )

            return redirect(
                url_for("proveedores.listar")
            )

        except IntegrityError:
            flash(
                "El NIT o correo ya está registrado.",
                "danger"
            )

            return render_template(
                "proveedores/formulario.html",
                proveedor=datos
            )

    return render_template(
        "proveedores/formulario.html",
        proveedor=None
    )




@proveedor_bp.route(
    "/editar/<int:id_proveedor>",
    methods=["GET", "POST"]
)
@login_requerido
def editar(id_proveedor):

    proveedor = ProveedorModel.obtener(id_proveedor)

    if not proveedor:
        abort(404)

    if request.method == "POST":

        datos = obtener_datos()

        errores = validar_proveedor(
            datos,
            excluir_id=id_proveedor
        )

        if errores:
            for error in errores:
                flash(error, "danger")

            return render_template(
                "proveedores/formulario.html",
                proveedor=datos
            )

        try:
            ProveedorModel.actualizar(
                id_proveedor, datos
            )

            flash(
                "Proveedor actualizado correctamente.",
                "success"
            )

            return redirect(
                url_for("proveedores.listar")
            )

        except IntegrityError:
            flash(
                "El NIT o correo ya está registrado.",
                "danger"
            )

            return render_template(
                "proveedores/formulario.html",
                proveedor=datos
            )

    return render_template(
        "proveedores/formulario.html",
        proveedor=proveedor
    )


@proveedor_bp.route(
    "/estado/<int:id_proveedor>",
    methods=["POST"]
)
@login_requerido
def cambiar_estado(id_proveedor):

    proveedor = ProveedorModel.obtener(id_proveedor)

    if not proveedor:
        abort(404)

    nuevo_estado = 0 if proveedor["activo"] else 1

    ProveedorModel.cambiar_estado(
        id_proveedor,
        nuevo_estado
    )

    if nuevo_estado == 1:
        flash(
            "Proveedor activado correctamente.",
            "success"
        )
    else:
        flash(
            "Proveedor desactivado correctamente.",
            "warning"
        )

    return redirect(
        url_for("proveedores.listar")
    )
