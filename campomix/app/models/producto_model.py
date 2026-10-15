
from app.database.conexion import obtener_conexion


class ProductoModel:

    @staticmethod
    def listar(busqueda=""):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    p.*,
                    c.nombre AS categoria,
                    c.activo AS categoria_activa,
                    u.nombre AS unidad,
                    u.simbolo
                FROM productos p
                INNER JOIN categorias_producto c
                    ON p.id_categoria = c.id_categoria
                INNER JOIN unidades_medida u
                    ON p.id_unidad = u.id_unidad
                WHERE p.codigo LIKE %s
                   OR p.nombre LIKE %s
                ORDER BY p.nombre
            """, (
                f"%{busqueda}%",
                f"%{busqueda}%"
            ))

            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()


    @staticmethod
    def obtener(id_producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    p.*,
                    u.nombre AS unidad_nombre,
                    u.simbolo AS unidad
                FROM productos p
                INNER JOIN unidades_medida u
                    ON p.id_unidad = u.id_unidad
                WHERE p.id_producto = %s
            """, (id_producto,))

            return cursor.fetchone()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def existe_codigo(codigo, excluir_id=None):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            if excluir_id is None:
                cursor.execute("""
                    SELECT 1
                    FROM productos
                    WHERE codigo = %s
                    LIMIT 1
                """, (codigo,))
            else:
                cursor.execute("""
                    SELECT 1
                    FROM productos
                    WHERE codigo = %s
                      AND id_producto <> %s
                    LIMIT 1
                """, (codigo, excluir_id))

            return cursor.fetchone() is not None

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def listar_categorias():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT id_categoria, nombre
                FROM categorias_producto
                WHERE activo = 1
                ORDER BY nombre
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def listar_unidades():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT id_unidad, nombre, simbolo
                FROM unidades_medida
                ORDER BY nombre
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def crear(datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                INSERT INTO productos (
                    codigo,
                    id_categoria,
                    nombre,
                    descripcion,
                    id_unidad,
                    precio_referencia,
                    vida_util_dias,
                    activo
                )
                SELECT
                    %s, c.id_categoria, %s, %s,
                    %s, %s, %s, 1
                FROM categorias_producto c
                WHERE c.id_categoria = %s
                  AND c.activo = 1
            """, (
                datos["codigo"],
                datos["nombre"],
                datos["descripcion"],
                datos["id_unidad"],
                datos["precio_referencia"],
                datos["vida_util_dias"],
                datos["id_categoria"]
            ))

            if cursor.rowcount != 1:
                raise ValueError(
                    "La categoría seleccionada no está activa."
                )

            conexion.commit()
            return cursor.lastrowid

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(id_producto, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                UPDATE productos p
                INNER JOIN categorias_producto c
                    ON c.id_categoria = %s
                   AND c.activo = 1
                SET p.codigo = %s,
                    p.id_categoria = c.id_categoria,
                    p.nombre = %s,
                    p.descripcion = %s,
                    p.id_unidad = %s,
                    p.precio_referencia = %s,
                    p.vida_util_dias = %s
                WHERE p.id_producto = %s
            """, (
                datos["id_categoria"],
                datos["codigo"],
                datos["nombre"],
                datos["descripcion"],
                datos["id_unidad"],
                datos["precio_referencia"],
                datos["vida_util_dias"],
                id_producto
            ))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def cambiar_estado(id_producto, nuevo_estado):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            if nuevo_estado == 1:
                cursor.execute("""
                    UPDATE productos p
                    INNER JOIN categorias_producto c
                        ON p.id_categoria = c.id_categoria
                    SET p.activo = 1
                    WHERE p.id_producto = %s
                      AND c.activo = 1
                """, (id_producto,))

                if cursor.rowcount == 0:
                    raise ValueError(
                        "No se puede activar un producto "
                        "si su categoría está inactiva."
                    )
            else:
                cursor.execute("""
                    UPDATE productos
                    SET activo = 0
                    WHERE id_producto = %s
                """, (id_producto,))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()
