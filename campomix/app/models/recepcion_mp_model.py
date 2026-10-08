
from app.database.conexion import obtener_conexion


class RecepcionMPModel:

    @staticmethod
    def listar():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    r.id_recepcion,
                    r.numero,
                    r.fecha,
                    r.estado,
                    p.razon_social AS proveedor,
                    a.nombre AS almacen,
                    COALESCE(
                        SUM(d.cantidad * d.costo_unitario),
                        0
                    ) AS total
                FROM recepciones_mp r
                INNER JOIN proveedores p
                    ON r.id_proveedor = p.id_proveedor
                INNER JOIN almacenes a
                    ON r.id_almacen = a.id_almacen
                LEFT JOIN recepcion_mp_detalles d
                    ON r.id_recepcion = d.id_recepcion
                GROUP BY
                    r.id_recepcion,
                    r.numero,
                    r.fecha,
                    r.estado,
                    p.razon_social,
                    a.nombre
                ORDER BY r.id_recepcion DESC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()

     
    @staticmethod
    def listar_proveedores():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT id_proveedor, razon_social
                FROM proveedores
                WHERE activo = 1
                ORDER BY razon_social
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def listar_almacenes():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT id_almacen, nombre
                FROM almacenes
                WHERE activo = 1
                  AND tipo IN ('MP', 'MIXTO')
                ORDER BY nombre
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def listar_materias():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    m.id_materia,
                    m.nombre,
                    m.codigo,
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
    def crear_borrador(datos, id_usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            conexion.start_transaction()

            # Verificar referencias activas
            cursor.execute("""
                SELECT id_proveedor
                FROM proveedores
                WHERE id_proveedor = %s AND activo = 1
            """, (datos["id_proveedor"],))
            if not cursor.fetchone():
                raise ValueError("Proveedor no válido.")

            cursor.execute("""
                SELECT id_almacen
                FROM almacenes
                WHERE id_almacen = %s
                  AND activo = 1
                  AND tipo IN ('MP', 'MIXTO')
            """, (datos["id_almacen"],))
            if not cursor.fetchone():
                raise ValueError("Almacén no válido.")

            cursor.execute("""
                SELECT id_materia
                FROM materias_primas
                WHERE id_materia = %s AND activo = 1
            """, (datos["id_materia"],))
            if not cursor.fetchone():
                raise ValueError("Materia prima no válida.")

            # Crear un número provisional único
            import uuid
            numero = "TMP-" + uuid.uuid4().hex[:12].upper()

            cursor.execute("""
                INSERT INTO recepciones_mp (
                    numero, id_proveedor,
                    id_almacen, estado, id_usuario
                )
                VALUES (%s, %s, %s, 'BORRADOR', %s)
            """, (
                numero,
                datos["id_proveedor"],
                datos["id_almacen"],
                id_usuario
            ))

            id_recepcion = cursor.lastrowid
            numero = f"REC-{id_recepcion:06d}"

            cursor.execute("""
                UPDATE recepciones_mp
                SET numero = %s
                WHERE id_recepcion = %s
            """, (numero, id_recepcion))          

            # Crear el lote en cuarentena
            cursor.execute("""
                INSERT INTO lotes_mp (
                    id_materia, id_proveedor,
                    codigo_lote, fecha_recepcion,
                    fecha_vencimiento, estado_calidad
                )
                VALUES (%s, %s, %s, CURDATE(), %s,
                        'CUARENTENA')
            """, (
                datos["id_materia"],
                datos["id_proveedor"],
                datos["codigo_lote"],
                datos["fecha_vencimiento"]
            ))

            id_lote = cursor.lastrowid

            # Asociar el lote con la recepción
            cursor.execute("""
                INSERT INTO recepcion_mp_detalles (
                    id_recepcion, id_lote_mp,
                    cantidad, costo_unitario
                )
                VALUES (%s, %s, %s, %s)
            """, (
                id_recepcion,
                id_lote,
                datos["cantidad"],
                datos["costo_unitario"]
            ))

            conexion.commit()
            return numero

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()



    @staticmethod
    def confirmar(id_recepcion, id_usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            conexion.start_transaction()

            # Bloquear la recepción para evitar
            # confirmaciones simultáneas.
            cursor.execute("""
                SELECT id_recepcion, estado, id_almacen
                FROM recepciones_mp
                WHERE id_recepcion = %s
                FOR UPDATE
            """, (id_recepcion,))

            recepcion = cursor.fetchone()

            if not recepcion:
                raise ValueError(
                    "La recepción no existe."
                )

            if recepcion["estado"] != "BORRADOR":
                raise ValueError(
                    "Solo se pueden confirmar "
                    "recepciones en borrador."
                )

            # Verificar que el almacén sea válido.
            cursor.execute("""
                SELECT id_almacen
                FROM almacenes
                WHERE id_almacen = %s
                  AND activo = 1
                  AND tipo IN ('MP', 'MIXTO')
            """, (recepcion["id_almacen"],))

            if not cursor.fetchone():
                raise ValueError(
                    "El almacén no está disponible."
                )

            # Obtener detalles de la recepción.
            
            cursor.execute("""
                SELECT
                    d.id_detalle,
                    d.id_lote_mp,
                    d.cantidad,
                    l.estado_calidad,
                    m.nombre AS materia_prima,
                    m.activo AS materia_activa
                FROM recepcion_mp_detalles d
                INNER JOIN lotes_mp l
                    ON d.id_lote_mp = l.id_lote_mp
                INNER JOIN materias_primas m
                    ON l.id_materia = m.id_materia
                WHERE d.id_recepcion = %s
                ORDER BY d.id_detalle
                FOR UPDATE
            """, (id_recepcion,))

            detalles = cursor.fetchall()


            if not detalles:
                raise ValueError(
                    "La recepción no tiene detalles."
                )

            for detalle in detalles:
                if detalle["cantidad"] <= 0:
                    raise ValueError(
                        "La recepción contiene "
                        "cantidades inválidas."
                    )

                if detalle["estado_calidad"] != "CUARENTENA":
                    raise ValueError(
                        "El lote debe estar en cuarentena "
                        "antes de confirmar la recepción."
                    )

                
                if detalle["materia_activa"] != 1:
                    raise ValueError(
                        f"No se puede confirmar la recepción. "
                        f"La materia prima "
                        f"'{detalle['materia_prima']}' "
                        f"se encuentra desactivada."
                    )


            # Registrar las entradas físicas.
            for detalle in detalles:
                cursor.execute("""
                    INSERT INTO movimientos_mp (
                        id_lote_mp,
                        id_almacen,
                        cantidad_firmada,
                        tipo,
                        referencia_tipo,
                        referencia_id,
                        id_usuario,
                        observacion
                    )
                    VALUES (
                        %s, %s, %s,
                        'RECEPCION',
                        'RECEPCION_MP',
                        %s, %s,
                        'Entrada por recepción confirmada'
                    )
                """, (
                    detalle["id_lote_mp"],
                    recepcion["id_almacen"],
                    detalle["cantidad"],
                    id_recepcion,
                    id_usuario
                ))

            # Marcar como confirmada.
            cursor.execute("""
                UPDATE recepciones_mp
                SET estado = 'CONFIRMADA'
                WHERE id_recepcion = %s
            """, (id_recepcion,))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()


    @staticmethod
    def anular_borrador(id_recepcion):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            conexion.start_transaction()

            cursor.execute("""
                SELECT estado
                FROM recepciones_mp
                WHERE id_recepcion = %s
                FOR UPDATE
            """, (id_recepcion,))

            recepcion = cursor.fetchone()

            if recepcion is None:
                raise ValueError(
                    "La recepción no existe."
                )

            if recepcion["estado"] != "BORRADOR":
                raise ValueError(
                    "Esta operación solo permite "
                    "anular recepciones en borrador."
                )

            cursor.execute("""
                UPDATE recepciones_mp
                SET estado = 'ANULADA'
                WHERE id_recepcion = %s
            """, (id_recepcion,))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()


    @staticmethod
    def anular_confirmada(id_recepcion, id_usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            conexion.start_transaction()

            # Bloquear la recepción
            cursor.execute("""
                SELECT id_recepcion, estado, id_almacen
                FROM recepciones_mp
                WHERE id_recepcion = %s
                FOR UPDATE
            """, (id_recepcion,))

            recepcion = cursor.fetchone()

            if recepcion is None:
                raise ValueError("La recepción no existe.")

            if recepcion["estado"] != "CONFIRMADA":
                raise ValueError(
                    "Solo se pueden anular recepciones confirmadas."
                )

            # Obtener entradas originales de la recepción
            cursor.execute("""
                SELECT
                    id_lote_mp,
                    id_almacen,
                    SUM(cantidad_firmada) AS cantidad
                FROM movimientos_mp
                WHERE referencia_tipo = 'RECEPCION_MP'
                  AND referencia_id = %s
                  AND tipo = 'RECEPCION'
                GROUP BY id_lote_mp, id_almacen
                ORDER BY id_lote_mp, id_almacen
            """, (id_recepcion,))

            entradas = cursor.fetchall()

            if not entradas:
                raise ValueError(
                    "La recepción no tiene movimientos de entrada."
                )

            # Bloquear los lotes involucrados
            for entrada in entradas:
                cursor.execute("""
                    SELECT id_lote_mp
                    FROM lotes_mp
                    WHERE id_lote_mp = %s
                    FOR UPDATE
                """, (entrada["id_lote_mp"],))

                if cursor.fetchone() is None:
                    raise ValueError("No se encontró un lote.")

            # Comprobar que las existencias permitan anular
            for entrada in entradas:
                cursor.execute("""
                    SELECT COALESCE(
                        SUM(cantidad_firmada), 0
                    ) AS saldo
                    FROM movimientos_mp
                    WHERE id_lote_mp = %s
                      AND id_almacen = %s
                """, (
                    entrada["id_lote_mp"],
                    entrada["id_almacen"]
                ))

                saldo = cursor.fetchone()["saldo"]

                if saldo < entrada["cantidad"]:
                    raise ValueError(
                        "No se puede anular la recepción: "
                        "uno de sus lotes ya tiene movimientos "
                        "que redujeron las existencias."
                    )

            # Registrar movimientos inversos
            for entrada in entradas:
                cursor.execute("""
                    INSERT INTO movimientos_mp (
                        id_lote_mp,
                        id_almacen,
                        cantidad_firmada,
                        tipo,
                        referencia_tipo,
                        referencia_id,
                        id_usuario,
                        observacion
                    )
                    VALUES (
                        %s, %s, %s,
                        'DEVOLUCION',
                        'RECEPCION_MP',
                        %s, %s,
                        'Reversión por anulación de recepción'
                    )
                """, (
                    entrada["id_lote_mp"],
                    entrada["id_almacen"],
                    -entrada["cantidad"],
                    id_recepcion,
                    id_usuario
                ))

            cursor.execute("""
                UPDATE recepciones_mp
                SET estado = 'ANULADA'
                WHERE id_recepcion = %s
            """, (id_recepcion,))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()


    @staticmethod
    def anular_confirmada(id_recepcion, id_usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            conexion.start_transaction()

            cursor.execute("""
                SELECT id_recepcion, estado
                FROM recepciones_mp
                WHERE id_recepcion = %s
                FOR UPDATE
            """, (id_recepcion,))

            recepcion = cursor.fetchone()

            if not recepcion:
                raise ValueError("La recepción no existe.")

            if recepcion["estado"] != "CONFIRMADA":
                raise ValueError(
                    "Solo se pueden anular recepciones confirmadas."
                )

            cursor.execute("""
                SELECT
                    id_lote_mp,
                    id_almacen,
                    SUM(cantidad_firmada) AS cantidad,
                    MAX(id_movimiento) AS ultimo_movimiento
                FROM movimientos_mp
                WHERE referencia_tipo = 'RECEPCION_MP'
                  AND referencia_id = %s
                  AND tipo = 'RECEPCION'
                GROUP BY id_lote_mp, id_almacen
                ORDER BY id_lote_mp, id_almacen
            """, (id_recepcion,))

            entradas = cursor.fetchall()

            if not entradas:
                raise ValueError(
                    "No se encontraron entradas para esta recepción."
                )

            for entrada in entradas:
                cursor.execute("""
                    SELECT id_lote_mp
                    FROM lotes_mp
                    WHERE id_lote_mp = %s
                    FOR UPDATE
                """, (entrada["id_lote_mp"],))

                if not cursor.fetchone():
                    raise ValueError("El lote no existe.")

                cursor.execute("""
                    SELECT COUNT(*) AS total
                    FROM movimientos_mp
                    WHERE id_lote_mp = %s
                      AND id_movimiento > %s
                """, (
                    entrada["id_lote_mp"],
                    entrada["ultimo_movimiento"]
                ))

                if cursor.fetchone()["total"] > 0:
                    raise ValueError(
                        "No se puede anular: el lote tiene "
                        "movimientos posteriores."
                    )

                cursor.execute("""
                    SELECT COALESCE(
                        SUM(cantidad_firmada), 0
                    ) AS saldo
                    FROM movimientos_mp
                    WHERE id_lote_mp = %s
                      AND id_almacen = %s
                """, (
                    entrada["id_lote_mp"],
                    entrada["id_almacen"]
                ))

                saldo = cursor.fetchone()["saldo"]

                if saldo < entrada["cantidad"]:
                    raise ValueError(
                        "No existe stock suficiente para "
                        "revertir esta recepción."
                    )

            for entrada in entradas:
                cursor.execute("""
                    INSERT INTO movimientos_mp (
                        id_lote_mp,
                        id_almacen,
                        cantidad_firmada,
                        tipo,
                        referencia_tipo,
                        referencia_id,
                        id_usuario,
                        observacion
                    )
                    VALUES (
                        %s, %s, %s,
                        'DEVOLUCION',
                        'ANULACION_RECEPCION_MP',
                        %s, %s,
                        'Reversión por anulación de recepción'
                    )
                """, (
                    entrada["id_lote_mp"],
                    entrada["id_almacen"],
                    -entrada["cantidad"],
                    id_recepcion,
                    id_usuario
                ))

            cursor.execute("""
                UPDATE recepciones_mp
                SET estado = 'ANULADA'
                WHERE id_recepcion = %s
            """, (id_recepcion,))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()


    @staticmethod
    def anular(id_recepcion, id_usuario):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT estado
                FROM recepciones_mp
                WHERE id_recepcion = %s
            """, (id_recepcion,))

            recepcion = cursor.fetchone()

        finally:
            cursor.close()
            conexion.close()

        if recepcion is None:
            raise ValueError("La recepción no existe.")

        if recepcion["estado"] == "BORRADOR":
            return RecepcionMPModel.anular_borrador(
                id_recepcion
            )

        if recepcion["estado"] == "CONFIRMADA":
            return RecepcionMPModel.anular_confirmada(
                id_recepcion,
                id_usuario
            )

        raise ValueError(
            "Esta recepción ya está anulada."
        )
