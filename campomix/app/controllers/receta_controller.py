
from decimal import Decimal, InvalidOperation
from functools import wraps

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, abort
)
from mysql.connector import Error as MySQLError

from app.models.receta_model import RecetaModel
from app.models.producto_model import ProductoModel


receta_bp = Blueprint(
    "recetas",
    __name__,
    url_prefix="/productos"
)


def login_requerido(funcion):
    @wraps(funcion)
    def decorador(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        return funcion(*args, **kwargs)
    return decorador


def convertir_cantidad(valor, nombre):
    try:
        cantidad = Decimal(str(valor).strip())

        if not cantidad.is_finite():
            raise ValueError()

        if cantidad <= 0:
            raise ValueError()

        if cantidad > Decimal("999999999999999.999"):
            raise ValueError()

        if cantidad.as_tuple().exponent < -3:
            raise ValueError()

        return cantidad

    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(
            f"{nombre} debe ser mayor que cero "
            "y tener máximo 3 decimales."
        )


def obtener_datos_formulario():
    cantidad_base = convertir_cantidad(
        request.form.get("cantidad_base", ""),
        "El rendimiento base"
    )

    observacion = request.form.get(
        "observacion", ""
    ).strip()

    ids_materias = request.form.getlist("id_materia[]")
    cantidades = request.form.getlist("cantidad[]")

    if not ids_materias:
        raise ValueError(
            "Debe agregar al menos una materia prima."
        )

    if len(ids_materias) != len(cantidades):
        raise ValueError(
            "Los ingredientes enviados no son válidos."
        )

    detalles = []
    materias_utilizadas = set()

    for posicion, (id_texto, valor) in enumerate(
        zip(ids_materias, cantidades), start=1
    ):
        try:
            id_materia = int(id_texto)
        except (TypeError, ValueError):
            raise ValueError(
                f"Seleccione una materia prima válida "
                f"en la fila {posicion}."
            )

        if id_materia <= 0:
            raise ValueError(
                f"Seleccione una materia prima "
                f"en la fila {posicion}."
            )

        if id_materia in materias_utilizadas:
            raise ValueError(
                "No puede repetir la misma materia prima."
            )

        materias_utilizadas.add(id_materia)

        cantidad = convertir_cantidad(
            valor,
            f"La cantidad de la fila {posicion}"
        )

        detalles.append({
            "id_materia": id_materia,
            "cantidad": cantidad
        })

    return cantidad_base, observacion, detalles


@receta_bp.route(
    "/<int:id_producto>/receta",
    methods=["GET", "POST"]
)
@login_requerido
def gestionar(id_producto):
    producto = ProductoModel.obtener(id_producto)

    if producto is None:
        abort(404)

    receta = RecetaModel.obtener_por_producto(id_producto)

    if request.method == "POST":
        try:
            cantidad_base, observacion, detalles = (
                obtener_datos_formulario()
            )

            RecetaModel.guardar(
                id_producto,
                cantidad_base,
                observacion,
                detalles
            )

            flash(
                "Receta guardada correctamente.",
                "success"
            )

            return redirect(
                url_for(
                    "recetas.gestionar",
                    id_producto=id_producto
                )
            )

        except (ValueError, MySQLError) as error:
            if isinstance(error, MySQLError):
                flash(
                    "No se pudo guardar la receta. "
                    "Verifique los datos e inténtelo nuevamente.",
                    "danger"
                )
            else:
                flash(str(error), "danger")

    receta = RecetaModel.obtener_por_producto(id_producto)

    detalles = []

    if receta:
        detalles = RecetaModel.obtener_detalles(
            receta["id_receta"]
        )

    materias = RecetaModel.listar_materias_primas()

    return render_template(
        "recetas/formulario.html",
        producto=producto,
        receta=receta,
        detalles=detalles,
        materias=materias
    )


@receta_bp.route(
    "/<int:id_producto>/receta/estado",
    methods=["POST"]
)
@login_requerido
def cambiar_estado(id_producto):
    producto = ProductoModel.obtener(id_producto)

    if producto is None:
        abort(404)

    receta = RecetaModel.obtener_por_producto(id_producto)

    if receta is None:
        flash(
            "Primero debe registrar una receta.",
            "warning"
        )

        return redirect(
            url_for(
                "recetas.gestionar",
                id_producto=id_producto
            )
        )

    estado = request.form.get("estado", "").strip()

    transiciones = {
        "BORRADOR": {"VIGENTE", "INACTIVA"},
        "VIGENTE": {"INACTIVA"},
        "INACTIVA": {"BORRADOR"}
    }

    if estado not in transiciones.get(receta["estado"], set()):
        flash(
            "El cambio de estado solicitado no está permitido.",
            "danger"
        )

        return redirect(
            url_for(
                "recetas.gestionar",
                id_producto=id_producto
            )
        )

    try:
        RecetaModel.cambiar_estado(
            receta["id_receta"],
            estado
        )

        flash(
            f"La receta ahora está en estado {estado}.",
            "success"
        )

    except (ValueError, MySQLError) as error:
        if isinstance(error, MySQLError):
            flash(
                "No se pudo cambiar el estado de la receta.",
                "danger"
            )
        else:
            flash(str(error), "danger")

    return redirect(
        url_for(
            "recetas.gestionar",
            id_producto=id_producto
        )
    )
