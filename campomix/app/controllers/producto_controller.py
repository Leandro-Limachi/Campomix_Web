
from decimal import Decimal, InvalidOperation
from functools import wraps

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, abort
)
from mysql.connector import IntegrityError

from app.models.producto_model import ProductoModel


producto_bp = Blueprint(
    "productos",
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


def obtener_datos():
    return {
        "codigo": request.form.get(
            "codigo", ""
        ).strip().upper(),

        "nombre": request.form.get(
            "nombre", ""
        ).strip(),

        "descripcion": request.form.get(
            "descripcion", ""
        ).strip(),

        "id_categoria": request.form.get(
            "id_categoria", type=int
        ),

        "id_unidad": request.form.get(
            "id_unidad", type=int
        ),

        "precio_referencia": request.form.get(
            "precio_referencia", ""
        ).strip(),

        "vida_util_dias": request.form.get(
            "vida_util_dias", ""
        ).strip()
    }


def validar_datos(datos, excluir_id=None):
    errores = []

    if not datos["codigo"]:
        errores.append("El código es obligatorio.")

    elif len(datos["codigo"]) > 40:
        errores.append(
            "El código no puede superar 40 caracteres."
        )

    elif ProductoModel.existe_codigo(
        datos["codigo"], excluir_id
    ):
        errores.append(
            "Ya existe un producto con ese código."
        )

    if not datos["nombre"]:
        errores.append("El nombre es obligatorio.")

    elif len(datos["nombre"]) > 150:
        errores.append(
            "El nombre no puede superar 150 caracteres."
        )

    categorias = ProductoModel.listar_categorias()
    ids_categorias = {
        c["id_categoria"] for c in categorias
    }

    if datos["id_categoria"] not in ids_categorias:
        errores.append(
            "Seleccione una categoría activa válida."
        )

    unidades = ProductoModel.listar_unidades()
    ids_unidades = {
        u["id_unidad"] for u in unidades
    }

    if datos["id_unidad"] not in ids_unidades:
        errores.append(
            "Seleccione una unidad de medida válida."
        )

    try:
        precio = Decimal(datos["precio_referencia"])

        if not precio.is_finite():
            raise ValueError()

        if precio < 0 or precio > Decimal("9999999999999999.99"):
            raise ValueError()

        if precio.as_tuple().exponent < -2:
            raise ValueError()

        datos["precio_referencia"] = precio

    except (InvalidOperation, ValueError):
        errores.append(
            "Ingrese un precio válido con máximo 2 decimales."
        )

    if datos["vida_util_dias"]:
        try:
            vida = int(datos["vida_util_dias"])

            if vida < 0 or vida > 4294967295:
                raise ValueError()

            datos["vida_util_dias"] = vida

        except ValueError:
            errores.append(
                "La vida útil debe ser un número entero válido."
            )
    else:
        datos["vida_util_dias"] = None

    return errores


@producto_bp.route("/")
@login_requerido
def listar():
    busqueda = request.args.get("buscar", "").strip()

    productos = ProductoModel.listar(busqueda)

    total = len(productos)

    activos = sum(
        1 for p in productos
        if p["activo"] and p["categoria_activa"]
    )

    inactivos = total - activos

    return render_template(
        "productos/listar.html",
        productos=productos,
        busqueda=busqueda,
        total=total,
        activos=activos,
        inactivos=inactivos
    )


@producto_bp.route("/nuevo", methods=["GET", "POST"])
@login_requerido
def nuevo():
    datos = None

    if request.method == "POST":
        datos = obtener_datos()
        errores = validar_datos(datos)

        if not errores:
            try:
                ProductoModel.crear(datos)

                flash(
                    "Producto registrado correctamente.",
                    "success"
                )

                return redirect(
                    url_for("productos.listar")
                )

            except IntegrityError:
                errores.append(
                    "No se pudo registrar. Verifique el código "
                    "y los datos relacionados."
                )

            except ValueError as error:
                errores.append(str(error))

        for error in errores:
            flash(error, "danger")

    return render_template(
        "productos/formulario.html",
        producto=datos,
        editando=False,
        categorias=ProductoModel.listar_categorias(),
        unidades=ProductoModel.listar_unidades()
    )


@producto_bp.route(
    "/editar/<int:id_producto>",
    methods=["GET", "POST"]
)
@login_requerido
def editar(id_producto):
    producto = ProductoModel.obtener(id_producto)

    if producto is None:
        abort(404)

    if request.method == "POST":
        datos = obtener_datos()
        errores = validar_datos(datos, id_producto)

        if not errores:
            try:
                ProductoModel.actualizar(
                    id_producto, datos
                )

                flash(
                    "Producto actualizado correctamente.",
                    "success"
                )

                return redirect(
                    url_for("productos.listar")
                )

            except IntegrityError:
                errores.append(
                    "No se pudo actualizar. Verifique los datos."
                )

        for error in errores:
            flash(error, "danger")

        producto = datos

    return render_template(
        "productos/formulario.html",
        producto=producto,
        editando=True,
        categorias=ProductoModel.listar_categorias(),
        unidades=ProductoModel.listar_unidades()
    )


@producto_bp.route(
    "/estado/<int:id_producto>",
    methods=["POST"]
)
@login_requerido
def cambiar_estado(id_producto):
    producto = ProductoModel.obtener(id_producto)

    if producto is None:
        abort(404)

    nuevo_estado = 0 if producto["activo"] else 1

    try:
        ProductoModel.cambiar_estado(
            id_producto, nuevo_estado
        )

        flash(
            "Estado del producto actualizado.",
            "success"
        )

    except ValueError as error:
        flash(str(error), "danger")

    return redirect(
        url_for("productos.listar")
    )
