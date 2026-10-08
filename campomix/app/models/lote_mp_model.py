
from app.database.conexion import obtener_conexion


class LoteMPModel:

    @staticmethod
    def listar():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    l.id_lote_mp,
                    l.codigo_lote,
                    l.fecha_recepcion,
                    l.fecha_vencimiento,
                    l.estado_calidad,
                    m.nombre AS materia_prima,
                    m.codigo AS codigo_materia,
                    u.simbolo,
                    p.razon_social AS proveedor,
                    COALESCE(
                        SUM(mov.cantidad_firmada), 0
                    ) AS stock_fisico
                FROM lotes_mp l
                INNER JOIN materias_primas m
                    ON l.id_materia = m.id_materia
                INNER JOIN unidades_medida u
                    ON m.id_unidad = u.id_unidad
                LEFT JOIN proveedores p
                    ON l.id_proveedor = p.id_proveedor
                LEFT JOIN movimientos_mp mov
                    ON l.id_lote_mp = mov.id_lote_mp
                GROUP BY
                    l.id_lote_mp,
                    l.codigo_lote,
                    l.fecha_recepcion,
                    l.fecha_vencimiento,
                    l.estado_calidad,
                    m.nombre,
                    m.codigo,
                    u.simbolo,
                    p.razon_social
                ORDER BY l.id_lote_mp DESC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def cambiar_calidad(id_lote, estado):
        if estado not in ("APROBADO", "RECHAZADO"):
            raise ValueError("Estado de calidad no válido.")

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            conexion.start_transaction()

            cursor.execute("""
                SELECT
                    l.id_lote_mp,
                    l.estado_calidad,
                    l.fecha_vencimiento
                FROM lotes_mp l
                WHERE l.id_lote_mp = %s
                FOR UPDATE
            """, (id_lote,))

            lote = cursor.fetchone()

            if lote is None:
                raise ValueError("El lote no existe.")

            if lote["estado_calidad"] != "CUARENTENA":
                raise ValueError(
                    "Solo se pueden evaluar lotes en cuarentena."
                )

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM recepcion_mp_detalles d
                INNER JOIN recepciones_mp r
                    ON d.id_recepcion = r.id_recepcion
                WHERE d.id_lote_mp = %s
                  AND r.estado = 'CONFIRMADA'
            """, (id_lote,))

            if cursor.fetchone()["total"] == 0:
                raise ValueError(
                    "El lote todavía no pertenece a una "
                    "recepción confirmada."
                )

            if estado == "APROBADO":
                from datetime import date

                if (
                    lote["fecha_vencimiento"] is not None
                    and lote["fecha_vencimiento"] < date.today()
                ):
                    raise ValueError(
                        "No se puede aprobar un lote vencido."
                    )

            cursor.execute("""
                UPDATE lotes_mp
                SET estado_calidad = %s
                WHERE id_lote_mp = %s
            """, (estado, id_lote))

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            cursor.close()
            conexion.close()
