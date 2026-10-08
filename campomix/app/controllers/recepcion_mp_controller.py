
from flask import Blueprint, render_template
from app.models.recepcion_mp_model import RecepcionMPModel
from app.controllers.proveedor_controller import login_requerido

from flask import request, redirect, url_for, flash, session
from decimal import Decimal, InvalidOperation
from datetime import date
from mysql.connector import IntegrityError



recepcion_mp_bp = Blueprint(
    "recepciones_mp",
    __name__,
    url_prefix="/recepciones-mp"
)


@recepcion_mp_bp.route("/")
@login_requerido
def listar():

    recepciones = RecepcionMPModel.listar()

    return render_template(
        "recepciones_mp/listar.html",
        recepciones=recepciones
    )


@recepcion_mp_bp.route("/nueva", methods=["GET", "POST"])
@login_requerido
def nueva():

    datos = {}

    if request.method == "POST":

        datos = {
            "id_proveedor": request.form.get(
                "id_proveedor", ""
            ),
            "id_almacen": request.form.get(
                "id_almacen", ""
            ),
            "id_materia": request.form.get(
                "id_materia", ""
            ),
            "codigo_lote": request.form.get(
                "codigo_lote", ""
            ).strip(),
            "fecha_vencimiento": request.form.get(
                "fecha_vencimiento", ""
            ),
            "cantidad": request.form.get(
                "cantidad", ""
            ),
            "costo_unitario": request.form.get(
                "costo_unitario", ""
            )
        }

        errores = []

        for campo in (
            "id_proveedor", "id_almacen", "id_materia"
        ):
            if not datos[campo].isdigit():
                errores.append(
                    "Seleccione proveedor, almacén y materia prima."
                )
                break

        if not datos["codigo_lote"]:
            errores.append("El código de lote es obligatorio.")
        elif len(datos["codigo_lote"]) > 70:
            errores.append("El código de lote es demasiado largo.")

        try:
            vencimiento = date.fromisoformat(
                datos["fecha_vencimiento"]
            )
            if vencimiento < date.today():
                errores.append(
                    "La fecha de vencimiento no puede ser anterior a hoy."
                )
        except ValueError:
            errores.append("Ingrese una fecha de vencimiento válida.")

        try:
            cantidad = Decimal(datos["cantidad"])
            if (
                not cantidad.is_finite()
                or cantidad <= 0
                or cantidad > Decimal("999999999999999.999")
                or cantidad.as_tuple().exponent < -3
            ):
                errores.append(
                    "La cantidad debe ser positiva y admitir "
                    "como máximo 3 decimales."
                )
        except InvalidOperation:
            errores.append("Ingrese una cantidad válida.")

        try:
            costo = Decimal(datos["costo_unitario"])
            if (
                not costo.is_finite()
                or costo < 0
                or costo > Decimal("99999999999999.9999")
                or costo.as_tuple().exponent < -4
            ):
                errores.append(
                    "El costo debe ser válido, no negativo "
                    "y admitir hasta 4 decimales."
                )
        except InvalidOperation:
            errores.append("Ingrese un costo válido.")

        if not errores:
            try:
                numero = RecepcionMPModel.crear_borrador(
                    datos,
                    session["usuario_id"]
                )

                flash(
                    f"Recepción {numero} guardada como borrador.",
                    "success"
                )
                return redirect(
                    url_for("recepciones_mp.listar")
                )

            except (ValueError, IntegrityError) as error:
                errores.append(str(error))

        for error in errores:
            flash(error, "danger")

    return render_template(
        "recepciones_mp/formulario.html",
        proveedores=RecepcionMPModel.listar_proveedores(),
        almacenes=RecepcionMPModel.listar_almacenes(),
        materias=RecepcionMPModel.listar_materias(),
        datos=datos
    )



@recepcion_mp_bp.route(
    "/confirmar/<int:id_recepcion>",
    methods=["POST"]
)
@login_requerido
def confirmar(id_recepcion):

    try:
        RecepcionMPModel.confirmar(
            id_recepcion,
            session["usuario_id"]
        )

        flash(
            "Recepción confirmada. "
            "Las materias primas ingresaron al "
            "inventario físico y permanecen "
            "en cuarentena.",
            "success"
        )

    except ValueError as error:
        flash(str(error), "danger")

    return redirect(
        url_for("recepciones_mp.listar")
    )




@recepcion_mp_bp.route(
    "/anular/<int:id_recepcion>",
    methods=["POST"]
)
@login_requerido
def anular(id_recepcion):

    try:
        RecepcionMPModel.anular(
            id_recepcion,
            session["usuario_id"]
        )

        flash(
            "Recepción anulada correctamente. "
            "El inventario fue actualizado cuando correspondía.",
            "success"
        )

    except ValueError as error:
        flash(str(error), "danger")

    return redirect(
        url_for("recepciones_mp.listar")
    )

