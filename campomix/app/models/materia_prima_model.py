
from app.database.conexion import obtener_conexion


class MateriaPrimaModel:

    @staticmethod
    def listar(busqueda=""):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            patron = f"%{busqueda}%"

            cursor.execute("""
                SELECT
                    m.id_materia,
                    m.codigo,
                    m.nombre,
                    m.descripcion,
                    m.stock_minimo,
                    m.activo,
                    u.nombre AS unidad,
                    u.simbolo
                FROM materias_primas m
                INNER JOIN unidades_medida u
                    ON m.id_unidad = u.id_unidad
                WHERE m.codigo LIKE %s
                   OR m.nombre LIKE %s
                ORDER BY m.id_materia DESC
            """, (patron, patron))

            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener(id_materia):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT *
                FROM materias_primas
                WHERE id_materia = %s
            """, (id_materia,))

            return cursor.fetchone()

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
    def existe_codigo(codigo, excluir_id=None):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            sql = """
                SELECT COUNT(*)
                FROM materias_primas
                WHERE codigo = %s
            """
            parametros = [codigo]

            if excluir_id is not None:
                sql += " AND id_materia != %s"
                parametros.append(excluir_id)

            cursor.execute(sql, tuple(parametros))
            return cursor.fetchone()[0] > 0

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def crear(datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                INSERT INTO materias_primas (
                    codigo, nombre, descripcion,
                    id_unidad, stock_minimo, activo
                )
                VALUES (%s, %s, %s, %s, %s, 1)
            """, (
                datos["codigo"],
                datos["nombre"],
                datos["descripcion"],
                datos["id_unidad"],
                datos["stock_minimo"]
            ))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(id_materia, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                UPDATE materias_primas
                SET codigo = %s,
                    nombre = %s,
                    descripcion = %s,
                    id_unidad = %s,
                    stock_minimo = %s
                WHERE id_materia = %s
            """, (
                datos["codigo"],
                datos["nombre"],
                datos["descripcion"],
                datos["id_unidad"],
                datos["stock_minimo"],
                id_materia
            ))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def cambiar_estado(id_materia, activo):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                UPDATE materias_primas
                SET activo = %s
                WHERE id_materia = %s
            """, (activo, id_materia))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()


    @staticmethod
    def alternar_estado(id_materia):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            conexion.start_transaction()

            cursor.execute("""
                SELECT id_materia, nombre, activo
                FROM materias_primas
                WHERE id_materia = %s
                FOR UPDATE
            """, (id_materia,))

            materia = cursor.fetchone()

            if materia is None:
                raise ValueError(
                    "La materia prima no existe."
                )

            nuevo_estado = 0 if materia["activo"] else 1

            cursor.execute("""
                UPDATE materias_primas
                SET activo = %s
                WHERE id_materia = %s
            """, (
                nuevo_estado,
                id_materia
            ))

            conexion.commit()

            return nuevo_estado

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()
