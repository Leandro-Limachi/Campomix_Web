
from app.database.conexion import obtener_conexion


class RecetaModel:

    @staticmethod
    def obtener_por_producto(id_producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    r.*,
                    p.codigo,
                    p.nombre AS producto,
                    u.simbolo AS unidad
                FROM recetas r
                INNER JOIN productos p
                    ON r.id_producto = p.id_producto
                INNER JOIN unidades_medida u
                    ON p.id_unidad = u.id_unidad
                WHERE r.id_producto = %s
            """, (id_producto,))

            return cursor.fetchone()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener_detalles(id_receta):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    d.id_detalle,
                    d.id_materia,
                    d.cantidad,
                    m.codigo,
                    m.nombre AS materia_prima,
                    u.nombre AS unidad,
                    u.simbolo
                FROM receta_detalles d
                INNER JOIN materias_primas m
                    ON d.id_materia = m.id_materia
                INNER JOIN unidades_medida u
                    ON m.id_unidad = u.id_unidad
                WHERE d.id_receta = %s
                ORDER BY m.nombre
            """, (id_receta,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def listar_materias_primas():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    m.id_materia,
                    m.codigo,
                    m.nombre,
                    u.simbolo
                FROM materias_primas m
                INNER JOIN unidades_medida u
                    ON m.id_unidad = u.id_unidad
                WHERE m.activo = 1
                ORDER BY m.nombre
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def guardar(
        id_producto,
        cantidad_base,
        observacion,
        detalles
    ):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            conexion.start_transaction()

            # Bloquear el producto durante la operación
            cursor.execute("""
                SELECT id_producto, activo
                FROM productos
                WHERE id_producto = %s
                FOR UPDATE
            """, (id_producto,))

            producto = cursor.fetchone()

            if not producto:
                raise ValueError(
                    "El producto no existe."
                )

            if not producto["activo"]:
                raise ValueError(
                    "No se puede gestionar la receta "
                    "de un producto inactivo."
                )

            # Verificar receta existente
            cursor.execute("""
                SELECT id_receta, estado
                FROM recetas
                WHERE id_producto = %s
                FOR UPDATE
            """, (id_producto,))

            receta = cursor.fetchone()

            if receta:
                id_receta = receta["id_receta"]

                if receta["estado"] == "VIGENTE":
                    raise ValueError(
                        "La receta vigente no se puede "
                        "modificar directamente. "
                        "Primero debe pasar a borrador."
                    )

                cursor.execute("""
                    UPDATE recetas
                    SET cantidad_base = %s,
                        observacion = %s
                    WHERE id_receta = %s
                """, (
                    cantidad_base,
                    observacion,
                    id_receta
                ))

                cursor.execute("""
                    DELETE FROM receta_detalles
                    WHERE id_receta = %s
                """, (id_receta,))

            else:
                cursor.execute("""
                    INSERT INTO recetas (
                        id_producto,
                        version,
                        cantidad_base,
                        estado,
                        observacion
                    )
                    VALUES (%s, 1, %s, 'BORRADOR', %s)
                """, (
                    id_producto,
                    cantidad_base,
                    observacion
                ))

                id_receta = cursor.lastrowid

            # Validar ingredientes contra el catálogo
            ids = [d["id_materia"] for d in detalles]

            if not ids or len(ids) != len(set(ids)):
                raise ValueError(
                    "Debe seleccionar materias primas "
                    "sin repetir ingredientes."
                )

            for detalle in detalles:
                cursor.execute("""
                    SELECT id_materia
                    FROM materias_primas
                    WHERE id_materia = %s
                      AND activo = 1
                """, (detalle["id_materia"],))

                if cursor.fetchone() is None:
                    raise ValueError(
                        "Una materia prima no existe "
                        "o está inactiva."
                    )

                cursor.execute("""
                    INSERT INTO receta_detalles (
                        id_receta,
                        id_materia,
                        cantidad
                    )
                    VALUES (%s, %s, %s)
                """, (
                    id_receta,
                    detalle["id_materia"],
                    detalle["cantidad"]
                ))

            conexion.commit()
            return id_receta

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def cambiar_estado(id_receta, estado):
        estados_permitidos = {
            "BORRADOR",
            "VIGENTE",
            "INACTIVA"
        }

        if estado not in estados_permitidos:
            raise ValueError(
                "Estado de receta no válido."
            )

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            conexion.start_transaction()

            cursor.execute("""
                SELECT
                    r.estado,
                    p.activo AS producto_activo,
                    c.activo AS categoria_activa
                FROM recetas r
                INNER JOIN productos p
                    ON r.id_producto = p.id_producto
                INNER JOIN categorias_producto c
                    ON p.id_categoria = c.id_categoria
                WHERE r.id_receta = %s
                FOR UPDATE
            """, (id_receta,))

            receta = cursor.fetchone()

            if not receta:
                raise ValueError(
                    "La receta no existe."
                )

            if estado == "VIGENTE":
                if (
                    not receta["producto_activo"]
                    or not receta["categoria_activa"]
                ):
                    raise ValueError(
                        "El producto y su categoría "
                        "deben estar activos."
                    )

                cursor.execute("""
                    SELECT COUNT(*) AS total
                    FROM receta_detalles
                    WHERE id_receta = %s
                """, (id_receta,))

                resultado = cursor.fetchone()

                if resultado["total"] == 0:
                    raise ValueError(
                        "La receta debe tener al menos "
                        "una materia prima."
                    )

            cursor.execute("""
                UPDATE recetas
                SET estado = %s
                WHERE id_receta = %s
            """, (estado, id_receta))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()
