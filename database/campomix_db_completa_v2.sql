CREATE DATABASE  IF NOT EXISTS `campomix_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `campomix_db`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: campomix_db
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `almacenes`
--

DROP TABLE IF EXISTS `almacenes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `almacenes` (
  `id_almacen` bigint unsigned NOT NULL AUTO_INCREMENT,
  `codigo` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo` enum('MP','PT','MIXTO') COLLATE utf8mb4_unicode_ci NOT NULL,
  `ubicacion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_almacen`),
  UNIQUE KEY `codigo` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `almacenes`
--

LOCK TABLES `almacenes` WRITE;
/*!40000 ALTER TABLE `almacenes` DISABLE KEYS */;
INSERT INTO `almacenes` VALUES (1,'AMP','Almacen de materias primas','MP',NULL,1),(2,'APT','Almacen de productos terminados','PT',NULL,1);
/*!40000 ALTER TABLE `almacenes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias_producto`
--

DROP TABLE IF EXISTS `categorias_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias_producto` (
  `id_categoria` bigint unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_categoria`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias_producto`
--

LOCK TABLES `categorias_producto` WRITE;
/*!40000 ALTER TABLE `categorias_producto` DISABLE KEYS */;
INSERT INTO `categorias_producto` VALUES (1,'Yogures','Productos fermentados',1),(2,'Quesos','Variedades de queso',1),(3,'Leche','Leche procesada',1),(4,'Mantequilla','Productos grasos lacteos',1);
/*!40000 ALTER TABLE `categorias_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` bigint unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `documento` varchar(35) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `correo` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direccion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compra_detalles`
--

DROP TABLE IF EXISTS `compra_detalles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compra_detalles` (
  `id_detalle` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_compra` bigint unsigned NOT NULL,
  `id_materia` bigint unsigned NOT NULL,
  `cantidad` decimal(18,3) NOT NULL,
  `precio_unitario` decimal(18,4) NOT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `id_compra` (`id_compra`),
  KEY `id_materia` (`id_materia`),
  CONSTRAINT `compra_detalles_ibfk_1` FOREIGN KEY (`id_compra`) REFERENCES `compras` (`id_compra`),
  CONSTRAINT `compra_detalles_ibfk_2` FOREIGN KEY (`id_materia`) REFERENCES `materias_primas` (`id_materia`),
  CONSTRAINT `compra_detalles_chk_1` CHECK ((`cantidad` > 0)),
  CONSTRAINT `compra_detalles_chk_2` CHECK ((`precio_unitario` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compra_detalles`
--

LOCK TABLES `compra_detalles` WRITE;
/*!40000 ALTER TABLE `compra_detalles` DISABLE KEYS */;
/*!40000 ALTER TABLE `compra_detalles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compras`
--

DROP TABLE IF EXISTS `compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compras` (
  `id_compra` bigint unsigned NOT NULL AUTO_INCREMENT,
  `numero` varchar(35) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_proveedor` bigint unsigned NOT NULL,
  `fecha` date NOT NULL,
  `estado` enum('BORRADOR','CONFIRMADA','PARCIAL','RECIBIDA','CANCELADA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'BORRADOR',
  `observacion` text COLLATE utf8mb4_unicode_ci,
  `id_usuario` bigint unsigned NOT NULL,
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_compra`),
  UNIQUE KEY `numero` (`numero`),
  KEY `id_proveedor` (`id_proveedor`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`),
  CONSTRAINT `compras_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras`
--

LOCK TABLES `compras` WRITE;
/*!40000 ALTER TABLE `compras` DISABLE KEYS */;
/*!40000 ALTER TABLE `compras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consumos_produccion`
--

DROP TABLE IF EXISTS `consumos_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consumos_produccion` (
  `id_consumo` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_orden` bigint unsigned NOT NULL,
  `id_lote_mp` bigint unsigned NOT NULL,
  `id_almacen` bigint unsigned NOT NULL,
  `cantidad` decimal(18,3) NOT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_consumo`),
  KEY `id_orden` (`id_orden`),
  KEY `id_lote_mp` (`id_lote_mp`),
  KEY `id_almacen` (`id_almacen`),
  CONSTRAINT `consumos_produccion_ibfk_1` FOREIGN KEY (`id_orden`) REFERENCES `ordenes_produccion` (`id_orden`),
  CONSTRAINT `consumos_produccion_ibfk_2` FOREIGN KEY (`id_lote_mp`) REFERENCES `lotes_mp` (`id_lote_mp`),
  CONSTRAINT `consumos_produccion_ibfk_3` FOREIGN KEY (`id_almacen`) REFERENCES `almacenes` (`id_almacen`),
  CONSTRAINT `consumos_produccion_chk_1` CHECK ((`cantidad` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consumos_produccion`
--

LOCK TABLES `consumos_produccion` WRITE;
/*!40000 ALTER TABLE `consumos_produccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `consumos_produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `despacho_detalles`
--

DROP TABLE IF EXISTS `despacho_detalles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `despacho_detalles` (
  `id_detalle` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_despacho` bigint unsigned NOT NULL,
  `id_venta_detalle` bigint unsigned NOT NULL,
  `id_lote_pt` bigint unsigned NOT NULL,
  `id_almacen` bigint unsigned NOT NULL,
  `cantidad` decimal(18,3) NOT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `id_despacho` (`id_despacho`),
  KEY `id_venta_detalle` (`id_venta_detalle`),
  KEY `id_lote_pt` (`id_lote_pt`),
  KEY `id_almacen` (`id_almacen`),
  CONSTRAINT `despacho_detalles_ibfk_1` FOREIGN KEY (`id_despacho`) REFERENCES `despachos` (`id_despacho`),
  CONSTRAINT `despacho_detalles_ibfk_2` FOREIGN KEY (`id_venta_detalle`) REFERENCES `venta_detalles` (`id_detalle`),
  CONSTRAINT `despacho_detalles_ibfk_3` FOREIGN KEY (`id_lote_pt`) REFERENCES `lotes_pt` (`id_lote_pt`),
  CONSTRAINT `despacho_detalles_ibfk_4` FOREIGN KEY (`id_almacen`) REFERENCES `almacenes` (`id_almacen`),
  CONSTRAINT `despacho_detalles_chk_1` CHECK ((`cantidad` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `despacho_detalles`
--

LOCK TABLES `despacho_detalles` WRITE;
/*!40000 ALTER TABLE `despacho_detalles` DISABLE KEYS */;
/*!40000 ALTER TABLE `despacho_detalles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `despachos`
--

DROP TABLE IF EXISTS `despachos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `despachos` (
  `id_despacho` bigint unsigned NOT NULL AUTO_INCREMENT,
  `numero` varchar(35) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_venta` bigint unsigned NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('BORRADOR','CONFIRMADO','ANULADO') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'BORRADOR',
  `id_usuario` bigint unsigned NOT NULL,
  PRIMARY KEY (`id_despacho`),
  UNIQUE KEY `numero` (`numero`),
  KEY `id_venta` (`id_venta`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `despachos_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`),
  CONSTRAINT `despachos_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `despachos`
--

LOCK TABLES `despachos` WRITE;
/*!40000 ALTER TABLE `despachos` DISABLE KEYS */;
/*!40000 ALTER TABLE `despachos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devolucion_detalles`
--

DROP TABLE IF EXISTS `devolucion_detalles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devolucion_detalles` (
  `id_detalle` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_devolucion` bigint unsigned NOT NULL,
  `id_despacho_detalle` bigint unsigned NOT NULL,
  `cantidad` decimal(18,3) NOT NULL,
  `destino` enum('CUARENTENA','DESCARTE') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'CUARENTENA',
  PRIMARY KEY (`id_detalle`),
  KEY `id_devolucion` (`id_devolucion`),
  KEY `id_despacho_detalle` (`id_despacho_detalle`),
  CONSTRAINT `devolucion_detalles_ibfk_1` FOREIGN KEY (`id_devolucion`) REFERENCES `devoluciones_venta` (`id_devolucion`),
  CONSTRAINT `devolucion_detalles_ibfk_2` FOREIGN KEY (`id_despacho_detalle`) REFERENCES `despacho_detalles` (`id_detalle`),
  CONSTRAINT `devolucion_detalles_chk_1` CHECK ((`cantidad` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devolucion_detalles`
--

LOCK TABLES `devolucion_detalles` WRITE;
/*!40000 ALTER TABLE `devolucion_detalles` DISABLE KEYS */;
/*!40000 ALTER TABLE `devolucion_detalles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devoluciones_venta`
--

DROP TABLE IF EXISTS `devoluciones_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devoluciones_venta` (
  `id_devolucion` bigint unsigned NOT NULL AUTO_INCREMENT,
  `numero` varchar(35) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_venta` bigint unsigned NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `motivo` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estado` enum('BORRADOR','CONFIRMADA','ANULADA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'BORRADOR',
  `id_usuario` bigint unsigned NOT NULL,
  PRIMARY KEY (`id_devolucion`),
  UNIQUE KEY `numero` (`numero`),
  KEY `id_venta` (`id_venta`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `devoluciones_venta_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`),
  CONSTRAINT `devoluciones_venta_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devoluciones_venta`
--

LOCK TABLES `devoluciones_venta` WRITE;
/*!40000 ALTER TABLE `devoluciones_venta` DISABLE KEYS */;
/*!40000 ALTER TABLE `devoluciones_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entregas`
--

DROP TABLE IF EXISTS `entregas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entregas` (
  `id_entrega` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_despacho` bigint unsigned NOT NULL,
  `id_vehiculo` bigint unsigned DEFAULT NULL,
  `responsable` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direccion_entrega` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_programada` datetime DEFAULT NULL,
  `fecha_entregada` datetime DEFAULT NULL,
  `estado` enum('PENDIENTE','EN_RUTA','ENTREGADA','FALLIDA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDIENTE',
  PRIMARY KEY (`id_entrega`),
  UNIQUE KEY `id_despacho` (`id_despacho`),
  KEY `id_vehiculo` (`id_vehiculo`),
  CONSTRAINT `entregas_ibfk_1` FOREIGN KEY (`id_despacho`) REFERENCES `despachos` (`id_despacho`),
  CONSTRAINT `entregas_ibfk_2` FOREIGN KEY (`id_vehiculo`) REFERENCES `vehiculos` (`id_vehiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entregas`
--

LOCK TABLES `entregas` WRITE;
/*!40000 ALTER TABLE `entregas` DISABLE KEYS */;
/*!40000 ALTER TABLE `entregas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lotes_mp`
--

DROP TABLE IF EXISTS `lotes_mp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lotes_mp` (
  `id_lote_mp` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_materia` bigint unsigned NOT NULL,
  `id_proveedor` bigint unsigned DEFAULT NULL,
  `codigo_lote` varchar(70) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_recepcion` date NOT NULL,
  `fecha_vencimiento` date DEFAULT NULL,
  `estado_calidad` enum('CUARENTENA','APROBADO','RECHAZADO') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'CUARENTENA',
  PRIMARY KEY (`id_lote_mp`),
  UNIQUE KEY `id_materia` (`id_materia`,`codigo_lote`),
  KEY `id_proveedor` (`id_proveedor`),
  CONSTRAINT `lotes_mp_ibfk_1` FOREIGN KEY (`id_materia`) REFERENCES `materias_primas` (`id_materia`),
  CONSTRAINT `lotes_mp_ibfk_2` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`),
  CONSTRAINT `lotes_mp_chk_1` CHECK (((`fecha_vencimiento` is null) or (`fecha_vencimiento` >= `fecha_recepcion`)))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lotes_mp`
--

LOCK TABLES `lotes_mp` WRITE;
/*!40000 ALTER TABLE `lotes_mp` DISABLE KEYS */;
INSERT INTO `lotes_mp` VALUES (1,1,1,'LEC-2026-001','2026-10-08','2026-12-30','APROBADO'),(2,2,2,'AZU-2026-001','2026-10-08','2027-07-01','CUARENTENA'),(3,4,3,'CUA-2026-001','2026-10-08','2027-01-31','CUARENTENA'),(4,2,5,'AZU-2026-002','2026-10-15','2027-01-31','APROBADO'),(5,2,6,'AZU-2026-003','2026-10-15','2027-01-31','APROBADO');
/*!40000 ALTER TABLE `lotes_mp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lotes_pt`
--

DROP TABLE IF EXISTS `lotes_pt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lotes_pt` (
  `id_lote_pt` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_producto` bigint unsigned NOT NULL,
  `id_orden` bigint unsigned NOT NULL,
  `codigo_lote` varchar(70) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_fabricacion` date NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `estado_calidad` enum('CUARENTENA','LIBERADO','BLOQUEADO') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'CUARENTENA',
  PRIMARY KEY (`id_lote_pt`),
  UNIQUE KEY `codigo_lote` (`codigo_lote`),
  KEY `id_producto` (`id_producto`),
  KEY `id_orden` (`id_orden`),
  CONSTRAINT `lotes_pt_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `lotes_pt_ibfk_2` FOREIGN KEY (`id_orden`) REFERENCES `ordenes_produccion` (`id_orden`),
  CONSTRAINT `lotes_pt_chk_1` CHECK ((`fecha_vencimiento` >= `fecha_fabricacion`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lotes_pt`
--

LOCK TABLES `lotes_pt` WRITE;
/*!40000 ALTER TABLE `lotes_pt` DISABLE KEYS */;
/*!40000 ALTER TABLE `lotes_pt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materias_primas`
--

DROP TABLE IF EXISTS `materias_primas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materias_primas` (
  `id_materia` bigint unsigned NOT NULL AUTO_INCREMENT,
  `codigo` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre` varchar(130) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `id_unidad` bigint unsigned NOT NULL,
  `stock_minimo` decimal(18,3) NOT NULL DEFAULT '0.000',
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_materia`),
  UNIQUE KEY `codigo` (`codigo`),
  KEY `id_unidad` (`id_unidad`),
  CONSTRAINT `materias_primas_ibfk_1` FOREIGN KEY (`id_unidad`) REFERENCES `unidades_medida` (`id_unidad`),
  CONSTRAINT `materias_primas_chk_1` CHECK ((`stock_minimo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materias_primas`
--

LOCK TABLES `materias_primas` WRITE;
/*!40000 ALTER TABLE `materias_primas` DISABLE KEYS */;
INSERT INTO `materias_primas` VALUES (1,'MP-001','Leche cruda','',1,100.000,1),(2,'MP-002','Azúcar','Azúcar fina',2,100.000,1),(3,'MP-003','Fermento láctico','',3,500.000,1),(4,'MP-004','Cuajo líquido','',5,250.000,1),(5,'MP-005','Envase plástico','',4,100.000,1),(6,'MP-007','Edulcorantes','',1,20.000,1);
/*!40000 ALTER TABLE `materias_primas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos_mp`
--

DROP TABLE IF EXISTS `movimientos_mp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_mp` (
  `id_movimiento` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_lote_mp` bigint unsigned NOT NULL,
  `id_almacen` bigint unsigned NOT NULL,
  `cantidad_firmada` decimal(18,3) NOT NULL,
  `tipo` enum('RECEPCION','CONSUMO','AJUSTE','DEVOLUCION','TRANSFERENCIA') COLLATE utf8mb4_unicode_ci NOT NULL,
  `referencia_tipo` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `referencia_id` bigint unsigned DEFAULT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_usuario` bigint unsigned NOT NULL,
  `observacion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_movimiento`),
  KEY `id_almacen` (`id_almacen`),
  KEY `id_usuario` (`id_usuario`),
  KEY `ix_mp_stock` (`id_lote_mp`,`id_almacen`),
  CONSTRAINT `movimientos_mp_ibfk_1` FOREIGN KEY (`id_lote_mp`) REFERENCES `lotes_mp` (`id_lote_mp`),
  CONSTRAINT `movimientos_mp_ibfk_2` FOREIGN KEY (`id_almacen`) REFERENCES `almacenes` (`id_almacen`),
  CONSTRAINT `movimientos_mp_ibfk_3` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `movimientos_mp_chk_1` CHECK ((`cantidad_firmada` <> 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos_mp`
--

LOCK TABLES `movimientos_mp` WRITE;
/*!40000 ALTER TABLE `movimientos_mp` DISABLE KEYS */;
INSERT INTO `movimientos_mp` VALUES (1,1,1,100.000,'RECEPCION','RECEPCION_MP',1,'2026-10-08 13:46:05',1,'Entrada por recepción confirmada'),(2,4,1,200.000,'RECEPCION','RECEPCION_MP',4,'2026-10-15 01:00:00',1,'Entrada por recepción confirmada'),(3,5,1,200.000,'RECEPCION','RECEPCION_MP',5,'2026-10-15 01:18:22',1,'Entrada por recepción confirmada');
/*!40000 ALTER TABLE `movimientos_mp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos_pt`
--

DROP TABLE IF EXISTS `movimientos_pt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_pt` (
  `id_movimiento` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_lote_pt` bigint unsigned NOT NULL,
  `id_almacen` bigint unsigned NOT NULL,
  `cantidad_firmada` decimal(18,3) NOT NULL,
  `tipo` enum('PRODUCCION','VENTA','DEVOLUCION','AJUSTE','TRANSFERENCIA','MERMA') COLLATE utf8mb4_unicode_ci NOT NULL,
  `referencia_tipo` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `referencia_id` bigint unsigned DEFAULT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_usuario` bigint unsigned NOT NULL,
  `observacion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_movimiento`),
  KEY `id_almacen` (`id_almacen`),
  KEY `id_usuario` (`id_usuario`),
  KEY `ix_pt_stock` (`id_lote_pt`,`id_almacen`),
  CONSTRAINT `movimientos_pt_ibfk_1` FOREIGN KEY (`id_lote_pt`) REFERENCES `lotes_pt` (`id_lote_pt`),
  CONSTRAINT `movimientos_pt_ibfk_2` FOREIGN KEY (`id_almacen`) REFERENCES `almacenes` (`id_almacen`),
  CONSTRAINT `movimientos_pt_ibfk_3` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `movimientos_pt_chk_1` CHECK ((`cantidad_firmada` <> 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos_pt`
--

LOCK TABLES `movimientos_pt` WRITE;
/*!40000 ALTER TABLE `movimientos_pt` DISABLE KEYS */;
/*!40000 ALTER TABLE `movimientos_pt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordenes_produccion`
--

DROP TABLE IF EXISTS `ordenes_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordenes_produccion` (
  `id_orden` bigint unsigned NOT NULL AUTO_INCREMENT,
  `numero` varchar(35) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_receta` bigint unsigned NOT NULL,
  `cantidad_planificada` decimal(18,3) NOT NULL,
  `cantidad_obtenida` decimal(18,3) DEFAULT NULL,
  `fecha_inicio` datetime DEFAULT NULL,
  `fecha_fin` datetime DEFAULT NULL,
  `estado` enum('PLANIFICADA','EN_PROCESO','FINALIZADA','CANCELADA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PLANIFICADA',
  `id_usuario` bigint unsigned NOT NULL,
  `observacion` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id_orden`),
  UNIQUE KEY `numero` (`numero`),
  KEY `id_receta` (`id_receta`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `ordenes_produccion_ibfk_1` FOREIGN KEY (`id_receta`) REFERENCES `recetas` (`id_receta`),
  CONSTRAINT `ordenes_produccion_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `ordenes_produccion_chk_1` CHECK ((`cantidad_planificada` > 0)),
  CONSTRAINT `ordenes_produccion_chk_2` CHECK (((`cantidad_obtenida` is null) or (`cantidad_obtenida` >= 0)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordenes_produccion`
--

LOCK TABLES `ordenes_produccion` WRITE;
/*!40000 ALTER TABLE `ordenes_produccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `ordenes_produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagos_venta`
--

DROP TABLE IF EXISTS `pagos_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagos_venta` (
  `id_pago` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_venta` bigint unsigned NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `monto` decimal(18,2) NOT NULL,
  `metodo` enum('EFECTIVO','TRANSFERENCIA','QR','TARJETA','OTRO') COLLATE utf8mb4_unicode_ci NOT NULL,
  `referencia` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_usuario` bigint unsigned NOT NULL,
  PRIMARY KEY (`id_pago`),
  KEY `id_venta` (`id_venta`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `pagos_venta_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`),
  CONSTRAINT `pagos_venta_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `pagos_venta_chk_1` CHECK ((`monto` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagos_venta`
--

LOCK TABLES `pagos_venta` WRITE;
/*!40000 ALTER TABLE `pagos_venta` DISABLE KEYS */;
/*!40000 ALTER TABLE `pagos_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permisos`
--

DROP TABLE IF EXISTS `permisos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permisos` (
  `id_permiso` bigint unsigned NOT NULL AUTO_INCREMENT,
  `codigo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_permiso`),
  UNIQUE KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permisos`
--

LOCK TABLES `permisos` WRITE;
/*!40000 ALTER TABLE `permisos` DISABLE KEYS */;
/*!40000 ALTER TABLE `permisos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` bigint unsigned NOT NULL AUTO_INCREMENT,
  `codigo` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_categoria` bigint unsigned NOT NULL,
  `nombre` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `id_unidad` bigint unsigned NOT NULL,
  `precio_referencia` decimal(18,2) NOT NULL DEFAULT '0.00',
  `vida_util_dias` int unsigned DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_producto`),
  UNIQUE KEY `codigo` (`codigo`),
  KEY `id_categoria` (`id_categoria`),
  KEY `id_unidad` (`id_unidad`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias_producto` (`id_categoria`),
  CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`id_unidad`) REFERENCES `unidades_medida` (`id_unidad`),
  CONSTRAINT `productos_chk_1` CHECK ((`precio_referencia` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'YOG-001',1,'Yogurt de frutilla','Yogurt de sabor frutilla',1,15.00,35,1),(2,'YOG-002',1,'Yogurt de Mango','',5,20.00,60,1);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `id_proveedor` bigint unsigned NOT NULL AUTO_INCREMENT,
  `razon_social` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nit` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contacto` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `correo` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direccion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_proveedor`),
  UNIQUE KEY `uq_proveedores_correo` (`correo`),
  UNIQUE KEY `uq_proveedores_nit` (`nit`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (1,'Proveedor de Leche','1234567890','Juan Pérez','71234567','proveedor@ejemplo.com','El Alto, La Paz',1,'2026-10-08 12:10:00'),(2,'Proveedor de Azucar','1234567811','Juana Pérez Mamani','61234567','proveedor2@ejemplo.com','El Alto, La Paz',1,'2026-10-08 12:15:07'),(3,'Proveedor de Colorantes','12345678900','Carlos Mamani','77777711','correo@gmail.com','Chuquisaca',1,'2026-10-08 12:43:55'),(4,'Proveedor de Colorantes para queso','8000000','Juan Pérez','78888888','ejemplo@gmail.com','El Alto Bolivia',1,'2026-10-15 00:46:12'),(5,'Proveedor de Azucar 2','7777777','Carlos Mamani','88888888','provedor@gmail.com','El Alto',0,'2026-10-15 00:52:48'),(6,'Proveedor de Azucar 3','5555555','Carlos Mamani','5555555','a@gmail.com','El ALTO',1,'2026-10-15 01:14:26');
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recepcion_mp_detalles`
--

DROP TABLE IF EXISTS `recepcion_mp_detalles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recepcion_mp_detalles` (
  `id_detalle` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_recepcion` bigint unsigned NOT NULL,
  `id_lote_mp` bigint unsigned NOT NULL,
  `cantidad` decimal(18,3) NOT NULL,
  `costo_unitario` decimal(18,4) NOT NULL DEFAULT '0.0000',
  PRIMARY KEY (`id_detalle`),
  KEY `id_recepcion` (`id_recepcion`),
  KEY `id_lote_mp` (`id_lote_mp`),
  CONSTRAINT `recepcion_mp_detalles_ibfk_1` FOREIGN KEY (`id_recepcion`) REFERENCES `recepciones_mp` (`id_recepcion`),
  CONSTRAINT `recepcion_mp_detalles_ibfk_2` FOREIGN KEY (`id_lote_mp`) REFERENCES `lotes_mp` (`id_lote_mp`),
  CONSTRAINT `recepcion_mp_detalles_chk_1` CHECK ((`cantidad` > 0)),
  CONSTRAINT `recepcion_mp_detalles_chk_2` CHECK ((`costo_unitario` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recepcion_mp_detalles`
--

LOCK TABLES `recepcion_mp_detalles` WRITE;
/*!40000 ALTER TABLE `recepcion_mp_detalles` DISABLE KEYS */;
INSERT INTO `recepcion_mp_detalles` VALUES (1,1,1,100.000,10.0000),(2,2,2,200.000,20.0000),(3,3,3,1000.000,40.0000),(4,4,4,200.000,150.0000),(5,5,5,200.000,10.0000);
/*!40000 ALTER TABLE `recepcion_mp_detalles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recepciones_mp`
--

DROP TABLE IF EXISTS `recepciones_mp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recepciones_mp` (
  `id_recepcion` bigint unsigned NOT NULL AUTO_INCREMENT,
  `numero` varchar(35) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_compra` bigint unsigned DEFAULT NULL,
  `id_proveedor` bigint unsigned NOT NULL,
  `id_almacen` bigint unsigned NOT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('BORRADOR','CONFIRMADA','ANULADA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'BORRADOR',
  `id_usuario` bigint unsigned NOT NULL,
  PRIMARY KEY (`id_recepcion`),
  UNIQUE KEY `numero` (`numero`),
  KEY `id_compra` (`id_compra`),
  KEY `id_proveedor` (`id_proveedor`),
  KEY `id_almacen` (`id_almacen`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `recepciones_mp_ibfk_1` FOREIGN KEY (`id_compra`) REFERENCES `compras` (`id_compra`),
  CONSTRAINT `recepciones_mp_ibfk_2` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`),
  CONSTRAINT `recepciones_mp_ibfk_3` FOREIGN KEY (`id_almacen`) REFERENCES `almacenes` (`id_almacen`),
  CONSTRAINT `recepciones_mp_ibfk_4` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recepciones_mp`
--

LOCK TABLES `recepciones_mp` WRITE;
/*!40000 ALTER TABLE `recepciones_mp` DISABLE KEYS */;
INSERT INTO `recepciones_mp` VALUES (1,'REC-89AF8E0ED5B6',NULL,1,1,'2026-10-08 13:32:34','CONFIRMADA',1),(2,'REC-000002',NULL,2,1,'2026-10-08 14:53:38','ANULADA',1),(3,'REC-000003',NULL,3,1,'2026-10-08 15:08:33','BORRADOR',1),(4,'REC-000004',NULL,5,1,'2026-10-15 00:58:53','CONFIRMADA',1),(5,'REC-000005',NULL,6,1,'2026-10-15 01:17:35','CONFIRMADA',1);
/*!40000 ALTER TABLE `recepciones_mp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receta_detalles`
--

DROP TABLE IF EXISTS `receta_detalles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta_detalles` (
  `id_detalle` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_receta` bigint unsigned NOT NULL,
  `id_materia` bigint unsigned NOT NULL,
  `cantidad` decimal(18,3) NOT NULL,
  PRIMARY KEY (`id_detalle`),
  UNIQUE KEY `id_receta` (`id_receta`,`id_materia`),
  KEY `id_materia` (`id_materia`),
  CONSTRAINT `receta_detalles_ibfk_1` FOREIGN KEY (`id_receta`) REFERENCES `recetas` (`id_receta`),
  CONSTRAINT `receta_detalles_ibfk_2` FOREIGN KEY (`id_materia`) REFERENCES `materias_primas` (`id_materia`),
  CONSTRAINT `receta_detalles_chk_1` CHECK ((`cantidad` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta_detalles`
--

LOCK TABLES `receta_detalles` WRITE;
/*!40000 ALTER TABLE `receta_detalles` DISABLE KEYS */;
INSERT INTO `receta_detalles` VALUES (5,1,2,5.000),(6,1,5,50.000),(7,1,3,800.000),(8,1,1,100.000),(9,2,2,5.000),(10,2,1,20.000);
/*!40000 ALTER TABLE `receta_detalles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recetas`
--

DROP TABLE IF EXISTS `recetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recetas` (
  `id_receta` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_producto` bigint unsigned NOT NULL,
  `version` int unsigned NOT NULL DEFAULT '1',
  `cantidad_base` decimal(18,3) NOT NULL,
  `estado` enum('BORRADOR','VIGENTE','INACTIVA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'BORRADOR',
  `observacion` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id_receta`),
  UNIQUE KEY `id_producto` (`id_producto`,`version`),
  CONSTRAINT `recetas_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `recetas_chk_1` CHECK ((`cantidad_base` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recetas`
--

LOCK TABLES `recetas` WRITE;
/*!40000 ALTER TABLE `recetas` DISABLE KEYS */;
INSERT INTO `recetas` VALUES (1,1,1,100.000,'VIGENTE',''),(2,2,1,1000.000,'VIGENTE','');
/*!40000 ALTER TABLE `recetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_rol` bigint unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_rol`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Administrador','Acceso general',1),(2,'Produccion','Operaciones de produccion',1),(3,'Almacen','Inventarios y almacenes',1),(4,'Ventas','Ventas y cobros',1);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles_permisos`
--

DROP TABLE IF EXISTS `roles_permisos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles_permisos` (
  `id_rol` bigint unsigned NOT NULL,
  `id_permiso` bigint unsigned NOT NULL,
  PRIMARY KEY (`id_rol`,`id_permiso`),
  KEY `id_permiso` (`id_permiso`),
  CONSTRAINT `roles_permisos_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`),
  CONSTRAINT `roles_permisos_ibfk_2` FOREIGN KEY (`id_permiso`) REFERENCES `permisos` (`id_permiso`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_permisos`
--

LOCK TABLES `roles_permisos` WRITE;
/*!40000 ALTER TABLE `roles_permisos` DISABLE KEYS */;
/*!40000 ALTER TABLE `roles_permisos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidades_medida`
--

DROP TABLE IF EXISTS `unidades_medida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidades_medida` (
  `id_unidad` bigint unsigned NOT NULL AUTO_INCREMENT,
  `codigo` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `simbolo` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_unidad`),
  UNIQUE KEY `codigo` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades_medida`
--

LOCK TABLES `unidades_medida` WRITE;
/*!40000 ALTER TABLE `unidades_medida` DISABLE KEYS */;
INSERT INTO `unidades_medida` VALUES (1,'L','Litro','L'),(2,'KG','Kilogramo','kg'),(3,'G','Gramo','g'),(4,'UND','Unidad','u'),(5,'ML','Mililitro','mL');
/*!40000 ALTER TABLE `unidades_medida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_rol` bigint unsigned NOT NULL,
  `nombre_completo` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usuario` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `correo` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `creado_en` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `usuario` (`usuario`),
  UNIQUE KEY `correo` (`correo`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,1,'Administrador Campomix','admin','scrypt:32768:8:1$VohutdCP7FDHcKiS$1f0384083ab436d9ac2ba0c22edf78846285b5850f230feccd5782fb33cbe0fe2ada1786d8545e8370cbd46699a7469e1e64bdc63e2f32369637ee922f15ddcf',NULL,NULL,1,'2026-10-08 11:33:49');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehiculos`
--

DROP TABLE IF EXISTS `vehiculos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehiculos` (
  `id_vehiculo` bigint unsigned NOT NULL AUTO_INCREMENT,
  `placa` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_vehiculo`),
  UNIQUE KEY `placa` (`placa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehiculos`
--

LOCK TABLES `vehiculos` WRITE;
/*!40000 ALTER TABLE `vehiculos` DISABLE KEYS */;
/*!40000 ALTER TABLE `vehiculos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta_detalles`
--

DROP TABLE IF EXISTS `venta_detalles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta_detalles` (
  `id_detalle` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_venta` bigint unsigned NOT NULL,
  `id_producto` bigint unsigned NOT NULL,
  `cantidad` decimal(18,3) NOT NULL,
  `precio_unitario` decimal(18,4) NOT NULL,
  `descuento` decimal(18,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`id_detalle`),
  KEY `id_venta` (`id_venta`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `venta_detalles_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`),
  CONSTRAINT `venta_detalles_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `venta_detalles_chk_1` CHECK ((`cantidad` > 0)),
  CONSTRAINT `venta_detalles_chk_2` CHECK ((`precio_unitario` >= 0)),
  CONSTRAINT `venta_detalles_chk_3` CHECK ((`descuento` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta_detalles`
--

LOCK TABLES `venta_detalles` WRITE;
/*!40000 ALTER TABLE `venta_detalles` DISABLE KEYS */;
/*!40000 ALTER TABLE `venta_detalles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `id_venta` bigint unsigned NOT NULL AUTO_INCREMENT,
  `numero` varchar(35) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_cliente` bigint unsigned NOT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('BORRADOR','CONFIRMADA','PARCIAL','ENTREGADA','CANCELADA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'BORRADOR',
  `id_usuario` bigint unsigned NOT NULL,
  `observacion` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id_venta`),
  UNIQUE KEY `numero` (`numero`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`),
  CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vw_stock_mp`
--

DROP TABLE IF EXISTS `vw_stock_mp`;
/*!50001 DROP VIEW IF EXISTS `vw_stock_mp`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_stock_mp` AS SELECT 
 1 AS `id_materia`,
 1 AS `codigo`,
 1 AS `nombre`,
 1 AS `id_lote_mp`,
 1 AS `codigo_lote`,
 1 AS `fecha_vencimiento`,
 1 AS `estado_calidad`,
 1 AS `id_almacen`,
 1 AS `almacen`,
 1 AS `stock`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_stock_pt`
--

DROP TABLE IF EXISTS `vw_stock_pt`;
/*!50001 DROP VIEW IF EXISTS `vw_stock_pt`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_stock_pt` AS SELECT 
 1 AS `id_producto`,
 1 AS `codigo`,
 1 AS `nombre`,
 1 AS `id_lote_pt`,
 1 AS `codigo_lote`,
 1 AS `fecha_vencimiento`,
 1 AS `estado_calidad`,
 1 AS `id_almacen`,
 1 AS `almacen`,
 1 AS `stock`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vw_stock_mp`
--

/*!50001 DROP VIEW IF EXISTS `vw_stock_mp`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_stock_mp` AS select `m`.`id_materia` AS `id_materia`,`m`.`codigo` AS `codigo`,`m`.`nombre` AS `nombre`,`l`.`id_lote_mp` AS `id_lote_mp`,`l`.`codigo_lote` AS `codigo_lote`,`l`.`fecha_vencimiento` AS `fecha_vencimiento`,`l`.`estado_calidad` AS `estado_calidad`,`a`.`id_almacen` AS `id_almacen`,`a`.`nombre` AS `almacen`,coalesce(sum(`mov`.`cantidad_firmada`),0) AS `stock` from (((`lotes_mp` `l` join `materias_primas` `m` on((`m`.`id_materia` = `l`.`id_materia`))) join `almacenes` `a`) left join `movimientos_mp` `mov` on(((`mov`.`id_lote_mp` = `l`.`id_lote_mp`) and (`mov`.`id_almacen` = `a`.`id_almacen`)))) where (`a`.`tipo` in ('MP','MIXTO')) group by `m`.`id_materia`,`m`.`codigo`,`m`.`nombre`,`l`.`id_lote_mp`,`l`.`codigo_lote`,`l`.`fecha_vencimiento`,`l`.`estado_calidad`,`a`.`id_almacen`,`a`.`nombre` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_stock_pt`
--

/*!50001 DROP VIEW IF EXISTS `vw_stock_pt`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_stock_pt` AS select `p`.`id_producto` AS `id_producto`,`p`.`codigo` AS `codigo`,`p`.`nombre` AS `nombre`,`l`.`id_lote_pt` AS `id_lote_pt`,`l`.`codigo_lote` AS `codigo_lote`,`l`.`fecha_vencimiento` AS `fecha_vencimiento`,`l`.`estado_calidad` AS `estado_calidad`,`a`.`id_almacen` AS `id_almacen`,`a`.`nombre` AS `almacen`,coalesce(sum(`mov`.`cantidad_firmada`),0) AS `stock` from (((`lotes_pt` `l` join `productos` `p` on((`p`.`id_producto` = `l`.`id_producto`))) join `almacenes` `a`) left join `movimientos_pt` `mov` on(((`mov`.`id_lote_pt` = `l`.`id_lote_pt`) and (`mov`.`id_almacen` = `a`.`id_almacen`)))) where (`a`.`tipo` in ('PT','MIXTO')) group by `p`.`id_producto`,`p`.`codigo`,`p`.`nombre`,`l`.`id_lote_pt`,`l`.`codigo_lote`,`l`.`fecha_vencimiento`,`l`.`estado_calidad`,`a`.`id_almacen`,`a`.`nombre` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-17 21:45:37


-- =====================================================================
-- ACTUALIZACIÓN v2.0 INCLUIDA
-- =====================================================================
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
