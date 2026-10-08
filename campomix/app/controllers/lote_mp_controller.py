
from flask import (
    Blueprint, render_template,
    request, redirect, url_for, flash, session, abort
)

from app.models.lote_mp_model import LoteMPModel
from app.controllers.proveedor_controller import login_requerido


lote_mp_bp = Blueprint(
    "lotes_mp",
    __name__,
    url_prefix="/lotes-mp"
)


@lote_mp_bp.route("/")
@login_requerido
def listar():
    lotes = LoteMPModel.listar()

    return render_template(
        "lotes_mp/listar.html",
        lotes=lotes
    )


@lote_mp_bp.route(
    "/calidad/<int:id_lote>",
    methods=["POST"]
)
@login_requerido
def cambiar_calidad(id_lote):

    estado = request.form.get("estado", "")

    try:
        LoteMPModel.cambiar_calidad(id_lote, estado)
        flash(
            "Estado de calidad actualizado correctamente.",
            "success"
        )

    except ValueError as error:
        flash(str(error), "danger")

    return redirect(url_for("lotes_mp.listar"))
