
from getpass import getpass

from werkzeug.security import generate_password_hash
from app import create_app
from app.database.conexion import obtener_conexion

app = create_app()


def crear_administrador():
    conexion = None
    cursor = None

    try:
        nombre = input("Nombre completo: ").strip()
        usuario = input("Usuario administrador: ").strip()
        password = getpass("Contraseña: ")

        if not nombre or not usuario:
            print("El nombre y usuario son obligatorios.")
            return

        if len(password) < 6:
            print("La contraseña debe tener al menos 6 caracteres.")
            return

        with app.app_context():
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            # Buscar rol administrador activo
            cursor.execute("""
                SELECT id_rol
                FROM roles
                WHERE nombre = %s AND activo = 1
            """, ("Administrador",))

            rol = cursor.fetchone()

            if not rol:
                print("No existe un rol Administrador activo.")
                return

            # Comprobar si el usuario ya existe
            cursor.execute("""
                SELECT id_usuario
                FROM usuarios
                WHERE usuario = %s
            """, (usuario,))

            if cursor.fetchone():
                print("Este usuario ya está registrado.")
                return

            # Proteger contraseña
            password_hash = generate_password_hash(password)

            # Registrar administrador
            cursor.execute("""
                INSERT INTO usuarios (
                    id_rol,
                    nombre_completo,
                    usuario,
                    password_hash,
                    activo
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                rol[0],
                nombre,
                usuario,
                password_hash,
                1
            ))

            conexion.commit()

            print("Administrador registrado correctamente.")

    except Exception as error:
        if conexion is not None:
            conexion.rollback()
        print(f"Error al registrar administrador: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()


if __name__ == "__main__":
    crear_administrador()
