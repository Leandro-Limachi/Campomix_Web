
from app.database.conexion import obtener_conexion


class CategoriaProductoModel:

    @staticmethod
    def listar(busqueda=""):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    c.id_categoria,
                    c.nombre,
                    c.descripcion,
                    c.activo,
                    COUNT(p.id_producto) AS total_productos
                FROM categorias_producto c
                LEFT JOIN productos p
                    ON p.id_categoria = c.id_categoria
                WHERE c.nombre LIKE %s
                GROUP BY
                    c.id_categoria,
                    c.nombre,
                    c.descripcion,
                    c.activo
                ORDER BY c.nombre ASC
            """

            cursor.execute(sql, (f"%{busqueda}%",))
            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener(id_categoria):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT *
                FROM categorias_producto
                WHERE id_categoria = %s
            """, (id_categoria,))

            return cursor.fetchone()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def existe_nombre(nombre, excluir_id=None):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            if excluir_id is None:
                cursor.execute("""
                    SELECT 1
                    FROM categorias_producto
                    WHERE nombre = %s
                    LIMIT 1
                """, (nombre,))
            else:
                cursor.execute("""
                    SELECT 1
                    FROM categorias_producto
                    WHERE nombre = %s
                      AND id_categoria <> %s
                    LIMIT 1
                """, (nombre, excluir_id))

            return cursor.fetchone() is not None

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def crear(datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                INSERT INTO categorias_producto
                    (nombre, descripcion, activo)
                VALUES (%s, %s, 1)
            """, (
                datos["nombre"],
                datos["descripcion"]
            ))

            conexion.commit()
            return cursor.lastrowid

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(id_categoria, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                UPDATE categorias_producto
                SET nombre = %s,
                    descripcion = %s
                WHERE id_categoria = %s
            """, (
                datos["nombre"],
                datos["descripcion"],
                id_categoria
            ))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def cambiar_estado(id_categoria, nuevo_estado):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                UPDATE categorias_producto
                SET activo = %s
                WHERE id_categoria = %s
            """, (
                nuevo_estado,
                id_categoria
            ))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()
