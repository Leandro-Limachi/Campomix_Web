
from app.database.conexion import obtener_conexion


class UsuarioModel:

    @staticmethod
    def buscar_por_usuario(usuario):
        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT
                    u.id_usuario,
                    u.nombre_completo,
                    u.usuario,
                    u.password_hash,
                    u.activo,
                    r.id_rol,
                    r.nombre AS rol,
                    r.activo AS rol_activo
                FROM usuarios u
                INNER JOIN roles r
                    ON u.id_rol = r.id_rol
                WHERE u.usuario = %s
                LIMIT 1
            """

            cursor.execute(consulta, (usuario,))
            return cursor.fetchone()

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()
