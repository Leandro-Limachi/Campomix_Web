
from app.database.conexion import obtener_conexion


class ProveedorModel:

    @staticmethod
    def listar(busqueda=""):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            sql = """
                SELECT *
                FROM proveedores
                WHERE razon_social LIKE %s
                   OR COALESCE(nit, '') LIKE %s
                ORDER BY id_proveedor DESC
            """

            patron = f"%{busqueda}%"
            cursor.execute(sql, (patron, patron))
            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener(id_proveedor):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT *
                FROM proveedores
                WHERE id_proveedor = %s
            """, (id_proveedor,))

            return cursor.fetchone()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def crear(datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                INSERT INTO proveedores (
                    razon_social, nit, contacto,
                    telefono, correo, direccion, activo
                )
                VALUES (%s, %s, %s, %s, %s, %s, 1)
            """, (
                datos["razon_social"],
                datos["nit"],
                datos["contacto"],
                datos["telefono"],
                datos["correo"],
                datos["direccion"]
            ))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(id_proveedor, datos):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                UPDATE proveedores
                SET razon_social = %s,
                    nit = %s,
                    contacto = %s,
                    telefono = %s,
                    correo = %s,
                    direccion = %s
                WHERE id_proveedor = %s
            """, (
                datos["razon_social"],
                datos["nit"],
                datos["contacto"],
                datos["telefono"],
                datos["correo"],
                datos["direccion"],
                id_proveedor
            ))

            conexion.commit()
            return cursor.rowcount > 0

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def cambiar_estado(id_proveedor, activo):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                UPDATE proveedores
                SET activo = %s
                WHERE id_proveedor = %s
            """, (activo, id_proveedor))

            conexion.commit()
            return cursor.rowcount > 0

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()


    @staticmethod
    def existe_nit(nit, excluir_id=None):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            sql = """
                SELECT COUNT(*)
                FROM proveedores
                WHERE nit = %s
            """
            parametros = [nit]

            if excluir_id is not None:
                sql += " AND id_proveedor != %s"
                parametros.append(excluir_id)

            cursor.execute(sql, tuple(parametros))
            return cursor.fetchone()[0] > 0

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def existe_correo(correo, excluir_id=None):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            sql = """
                SELECT COUNT(*)
                FROM proveedores
                WHERE LOWER(correo) = %s
            """
            parametros = [correo.lower()]

            if excluir_id is not None:
                sql += " AND id_proveedor != %s"
                parametros.append(excluir_id)

            cursor.execute(sql, tuple(parametros))
            return cursor.fetchone()[0] > 0

        finally:
            cursor.close()
            conexion.close()
