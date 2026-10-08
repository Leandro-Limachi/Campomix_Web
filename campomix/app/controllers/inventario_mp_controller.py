
from flask import Blueprint, render_template

from app.models.inventario_mp_model import InventarioMPModel
from app.controllers.proveedor_controller import login_requerido


inventario_mp_bp = Blueprint(
    "inventario_mp",
    __name__,
    url_prefix="/inventario-mp"
)


@inventario_mp_bp.route("/")
@login_requerido
def listar():

    inventario = InventarioMPModel.listar()

    return render_template(
        "inventario_mp/listar.html",
        inventario=inventario
    )
