
import re
from decimal import Decimal, InvalidOperation
from functools import wraps

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, abort
)
from mysql.connector import IntegrityError

from app.models.materia_prima_model import MateriaPrimaModel


materia_prima_bp = Blueprint(
    "materias_primas",
    __name__,
    url_prefix="/materias-primas"
)


def login_requerido(funcion):
    @wraps(funcion)
    def decorador(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        return funcion(*args, **kwargs)
    return decorador


def obtener_datos():
    return {
        "codigo": request.form.get("codigo", "").strip().upper(),
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "id_unidad": request.form.get("id_unidad", "").strip(),
        "stock_minimo": request.form.get("stock_minimo", "").strip()
    }


def validar_datos(datos, excluir_id=None):
    errores = []

    if not re.fullmatch(r"[A-Z0-9-]{2,40}", datos["codigo"]):
        errores.append(
            "El código debe tener entre 2 y 40 caracteres: "
            "letras, números o guiones."
        )
    elif MateriaPrimaModel.existe_codigo(
        datos["codigo"], excluir_id
    ):
        errores.append("El código ya está registrado.")

    if not 3 <= len(datos["nombre"]) <= 130:
        errores.append(
            "El nombre debe tener entre 3 y 130 caracteres."
        )

    if len(datos["descripcion"]) > 65535:
        errores.append("La descripción es demasiado larga.")

    unidades = MateriaPrimaModel.listar_unidades()
    ids_validos = {str(u["id_unidad"]) for u in unidades}

    if datos["id_unidad"] not in ids_validos:
        errores.append("Seleccione una unidad de medida válida.")

    try:
        stock = Decimal(datos["stock_minimo"])

        if not stock.is_finite() or stock < 0:
            errores.append(
                "El stock mínimo debe ser mayor o igual a cero."
            )
        elif stock > Decimal("999999999999999.999"):
            errores.append("El stock mínimo es demasiado grande.")
        elif stock.as_tuple().exponent < -3:
            errores.append(
                "El stock mínimo admite hasta 3 decimales."
            )

    except (InvalidOperation, ValueError):
        errores.append("Ingrese un stock mínimo válido.")

    return errores


@materia_prima_bp.route("/")
@login_requerido
def listar():
    busqueda = request.args.get("buscar", "").strip()

    materias = MateriaPrimaModel.listar(busqueda)

    return render_template(
        "materias_primas/listar.html",
        materias=materias,
        busqueda=busqueda
    )


@materia_prima_bp.route("/nuevo", methods=["GET", "POST"])
@login_requerido
def nuevo():
    datos = None

    if request.method == "POST":
        datos = obtener_datos()
        errores = validar_datos(datos)

        if not errores:
            try:
                MateriaPrimaModel.crear(datos)
                flash(
                    "Materia prima registrada correctamente.",
                    "success"
                )
                return redirect(url_for("materias_primas.listar"))

            except IntegrityError:
                errores.append(
                    "El código ya existe o la unidad no es válida."
                )

        for error in errores:
            flash(error, "danger")

    return render_template(
        "materias_primas/formulario.html",
        materia=datos,
        unidades=MateriaPrimaModel.listar_unidades(),
        editando=False
    )


@materia_prima_bp.route(
    "/editar/<int:id_materia>",
    methods=["GET", "POST"]
)
@login_requerido
def editar(id_materia):
    materia = MateriaPrimaModel.obtener(id_materia)

    if materia is None:
        abort(404)

    if request.method == "POST":
        datos = obtener_datos()
        errores = validar_datos(datos, id_materia)

        if not errores:
            try:
                MateriaPrimaModel.actualizar(id_materia, datos)
                flash(
                    "Materia prima actualizada correctamente.",
                    "success"
                )
                return redirect(url_for("materias_primas.listar"))

            except IntegrityError:
                errores.append(
                    "El código ya existe o la unidad no es válida."
                )

        for error in errores:
            flash(error, "danger")

        materia = datos

    return render_template(
        "materias_primas/formulario.html",
        materia=materia,
        unidades=MateriaPrimaModel.listar_unidades(),
        editando=True
    )



@materia_prima_bp.route(
    "/estado/<int:id_materia>",
    methods=["POST"]
)
@login_requerido
def cambiar_estado(id_materia):

    try:
        nuevo_estado = MateriaPrimaModel.alternar_estado(
            id_materia
        )

        if nuevo_estado == 0:
            flash(
                "Materia prima desactivada correctamente. "
                "Se conserva su inventario e historial, "
                "pero se bloquean las nuevas operaciones.",
                "warning"
            )
        else:
            flash(
                "Materia prima reactivada correctamente.",
                "success"
            )

    except ValueError as error:
        flash(str(error), "danger")

    return redirect(
        url_for("materias_primas.listar")
    )
