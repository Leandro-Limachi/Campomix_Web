
from functools import wraps

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, abort
)
from mysql.connector import IntegrityError

from app.models.categoria_producto_model import CategoriaProductoModel


categoria_producto_bp = Blueprint(
    "categorias",
    __name__,
    url_prefix="/categorias"
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
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip()
    }


def validar_datos(datos, excluir_id=None):
    errores = []

    nombre = datos["nombre"]
    descripcion = datos["descripcion"]

    if not nombre:
        errores.append("El nombre de la categoría es obligatorio.")

    elif len(nombre) < 3 or len(nombre) > 100:
        errores.append(
            "El nombre debe tener entre 3 y 100 caracteres."
        )

    elif CategoriaProductoModel.existe_nombre(
        nombre, excluir_id
    ):
        errores.append("Ya existe una categoría con ese nombre.")

    if len(descripcion) > 255:
        errores.append(
            "La descripción no puede superar los 255 caracteres."
        )

    return errores


@categoria_producto_bp.route("/")
@login_requerido
def listar():
    busqueda = request.args.get("buscar", "").strip()

    categorias = CategoriaProductoModel.listar(busqueda)

    return render_template(
        "categorias_producto/listar.html",
        categorias=categorias,
        busqueda=busqueda
    )


@categoria_producto_bp.route(
    "/nueva",
    methods=["GET", "POST"]
)
@login_requerido
def nueva():
    datos = None

    if request.method == "POST":
        datos = obtener_datos()
        errores = validar_datos(datos)

        if not errores:
            try:
                CategoriaProductoModel.crear(datos)

                flash(
                    "Categoría registrada correctamente.",
                    "success"
                )

                return redirect(
                    url_for("categorias.listar")
                )

            except IntegrityError:
                errores.append(
                    "Ya existe una categoría con ese nombre."
                )

        for error in errores:
            flash(error, "danger")

    return render_template(
        "categorias_producto/formulario.html",
        categoria=datos,
        editando=False
    )


@categoria_producto_bp.route(
    "/editar/<int:id_categoria>",
    methods=["GET", "POST"]
)
@login_requerido
def editar(id_categoria):
    categoria = CategoriaProductoModel.obtener(id_categoria)

    if categoria is None:
        abort(404)

    if request.method == "POST":
        datos = obtener_datos()

        errores = validar_datos(
            datos,
            excluir_id=id_categoria
        )

        if not errores:
            try:
                CategoriaProductoModel.actualizar(
                    id_categoria,
                    datos
                )

                flash(
                    "Categoría actualizada correctamente.",
                    "success"
                )

                return redirect(
                    url_for("categorias.listar")
                )

            except IntegrityError:
                errores.append(
                    "Ya existe una categoría con ese nombre."
                )

        for error in errores:
            flash(error, "danger")

        categoria = datos

    return render_template(
        "categorias_producto/formulario.html",
        categoria=categoria,
        editando=True
    )


@categoria_producto_bp.route(
    "/estado/<int:id_categoria>",
    methods=["POST"]
)
@login_requerido
def cambiar_estado(id_categoria):
    categoria = CategoriaProductoModel.obtener(id_categoria)

    if categoria is None:
        abort(404)

    nuevo_estado = 0 if categoria["activo"] else 1

    CategoriaProductoModel.cambiar_estado(
        id_categoria,
        nuevo_estado
    )

    if nuevo_estado == 1:
        flash(
            "Categoría activada correctamente.",
            "success"
        )
    else:
        flash(
            "Categoría desactivada. Los productos asociados "
            "deberán quedar bloqueados para nuevas operaciones.",
            "warning"
        )

    return redirect(
        url_for("categorias.listar")
    )
