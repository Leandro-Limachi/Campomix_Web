-- =====================================================================
--  CAMPOMIX - ACTUALIZACIÓN v2.0
--  Módulos: Producción (ejecución), Productos Terminados,
--           Clientes y Ventas
--
--  Ejecutar UNA SOLA VEZ sobre la base campomix_db existente.
--  No borra datos: solo agrega columnas, índices, una vista
--  y datos de ejemplo de clientes.
-- =====================================================================

USE `campomix_db`;
SET NAMES utf8mb4;

-- ---------------------------------------------------------------------
-- 1. PRODUCTOS: stock mínimo de producto terminado (alertas)
-- ---------------------------------------------------------------------
ALTER TABLE `productos`
    ADD COLUMN `stock_minimo` DECIMAL(18,3) NOT NULL DEFAULT 0.000
        AFTER `vida_util_dias`;

ALTER TABLE `productos`
    ADD CONSTRAINT `productos_chk_stock_min` CHECK (`stock_minimo` >= 0);

-- ---------------------------------------------------------------------
-- 2. LOTES DE PRODUCTO TERMINADO: trazabilidad de lo producido
-- ---------------------------------------------------------------------
ALTER TABLE `lotes_pt`
    ADD COLUMN `cantidad_producida` DECIMAL(18,3) NOT NULL DEFAULT 0.000
        AFTER `fecha_vencimiento`,
    ADD COLUMN `observacion` VARCHAR(255) NULL
        AFTER `estado_calidad`;

-- ---------------------------------------------------------------------
-- 3. CLIENTES: tipo de cliente, observación y documento único
-- ---------------------------------------------------------------------
ALTER TABLE `clientes`
    ADD COLUMN `tipo_cliente`
        ENUM('MINORISTA','MAYORISTA','DISTRIBUIDOR','INSTITUCIONAL')
        NOT NULL DEFAULT 'MINORISTA' AFTER `nombre`,
    ADD COLUMN `observacion` VARCHAR(255) NULL AFTER `direccion`,
    ADD UNIQUE KEY `uq_clientes_documento` (`documento`);

-- ---------------------------------------------------------------------
-- 4. VENTAS: totales calculados y fecha de confirmación
-- ---------------------------------------------------------------------
ALTER TABLE `ventas`
    ADD COLUMN `subtotal` DECIMAL(18,2) NOT NULL DEFAULT 0.00 AFTER `estado`,
    ADD COLUMN `descuento_total` DECIMAL(18,2) NOT NULL DEFAULT 0.00 AFTER `subtotal`,
    ADD COLUMN `total` DECIMAL(18,2) NOT NULL DEFAULT 0.00 AFTER `descuento_total`,
    ADD COLUMN `fecha_confirmacion` DATETIME NULL AFTER `total`,
    ADD INDEX `ix_ventas_fecha` (`fecha`),
    ADD INDEX `ix_ventas_estado` (`estado`);

ALTER TABLE `movimientos_pt`
    ADD INDEX `ix_mov_pt_fecha` (`fecha`);

-- ---------------------------------------------------------------------
-- 5. VISTA: inventario de producto terminado por producto
-- ---------------------------------------------------------------------
DROP VIEW IF EXISTS `vw_inventario_pt`;

CREATE VIEW `vw_inventario_pt` AS
SELECT
    p.id_producto,
    p.codigo,
    p.nombre,
    COALESCE(SUM(s.saldo), 0) AS stock_fisico,
    COALESCE(SUM(CASE
        WHEN l.estado_calidad = 'LIBERADO'
         AND l.fecha_vencimiento >= CURDATE()
        THEN s.saldo ELSE 0 END), 0) AS stock_disponible
FROM productos p
LEFT JOIN lotes_pt l ON l.id_producto = p.id_producto
LEFT JOIN (
    SELECT id_lote_pt, SUM(cantidad_firmada) AS saldo
    FROM movimientos_pt
    GROUP BY id_lote_pt
) s ON s.id_lote_pt = l.id_lote_pt
GROUP BY p.id_producto, p.codigo, p.nombre;

-- ---------------------------------------------------------------------
-- 6. DATOS DE EJEMPLO (clientes)
-- ---------------------------------------------------------------------
INSERT INTO `clientes`
    (`nombre`, `tipo_cliente`, `documento`, `telefono`, `correo`, `direccion`, `activo`)
VALUES
    ('Tienda Doña Rosa',              'MINORISTA',     '4567812',    '71122334', 'tiendarosa@gmail.com',     'Av. 6 de Marzo, El Alto', 1),
    ('Minimarket El Alteño',          'MINORISTA',     '6012345015', '72233445', 'minimarket.alteno@gmail.com','Ciudad Satélite, El Alto', 1),
    ('Distribuidora Andina SRL',      'DISTRIBUIDOR',  '1020304050', '22845566', 'ventas@distandina.com.bo', 'Zona 16 de Julio, El Alto', 1),
    ('Unidad Educativa San Andrés',   'INSTITUCIONAL', '3040506070', '22811223', 'ue.sanandres@gmail.com',   'Villa Adela, El Alto', 1),
    ('Comercial Lácteos del Valle',   'MAYORISTA',   '5060708090', '76655443', 'lacteosdelvalle@gmail.com','Mercado Rodríguez, La Paz', 1);

-- Fin de la actualización
