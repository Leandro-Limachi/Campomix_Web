
from app.database.conexion import obtener_conexion


class InventarioMPModel:

    @staticmethod
    def listar():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    m.id_materia,
                    m.codigo,
                    m.nombre,
                    u.simbolo,
                    m.stock_minimo,
                    m.activo,

                    COALESCE(SUM(
                        COALESCE(s.saldo, 0)
                    ), 0) AS stock_fisico,

                    COALESCE(SUM(
                        CASE
                            WHEN m.activo = 1
                            AND l.estado_calidad = 'APROBADO'
                            AND (
                                l.fecha_vencimiento IS NULL
                                OR l.fecha_vencimiento >= CURDATE()
                            )
                            THEN COALESCE(s.saldo, 0)
                            ELSE 0
                        END
                    ), 0) AS disponible,

                    COALESCE(SUM(
                        CASE
                            WHEN l.estado_calidad = 'CUARENTENA'
                            THEN COALESCE(s.saldo, 0)
                            ELSE 0
                        END
                    ), 0) AS cuarentena,

                    COALESCE(SUM(
                        CASE
                            WHEN l.estado_calidad = 'RECHAZADO'
                            THEN COALESCE(s.saldo, 0)
                            ELSE 0
                        END
                    ), 0) AS rechazado,

                    COALESCE(SUM(
                        CASE
                            WHEN l.estado_calidad = 'APROBADO'
                             AND l.fecha_vencimiento < CURDATE()
                            THEN COALESCE(s.saldo, 0)
                            ELSE 0
                        END
                    ), 0) AS vencido

                FROM materias_primas m

                INNER JOIN unidades_medida u
                    ON m.id_unidad = u.id_unidad

                LEFT JOIN lotes_mp l
                    ON m.id_materia = l.id_materia

                LEFT JOIN (
                    SELECT
                        id_lote_mp,
                        SUM(cantidad_firmada) AS saldo
                    FROM movimientos_mp
                    GROUP BY id_lote_mp
                ) s
                    ON l.id_lote_mp = s.id_lote_mp

                

                GROUP BY
                    m.id_materia,
                    m.codigo,
                    m.nombre,
                    m.activo,
                    u.simbolo,
                    m.stock_minimo

                ORDER BY m.nombre
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()
