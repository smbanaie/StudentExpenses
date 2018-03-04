-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.2.13-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for project_db
DROP DATABASE IF EXISTS `project_db`;
CREATE DATABASE IF NOT EXISTS `project_db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `project_db`;

-- Dumping structure for table project_db.admin
DROP TABLE IF EXISTS `admin`;
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `user` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table project_db.admin: ~0 rows (approximately)
DELETE FROM `admin`;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;

-- Dumping structure for table project_db.buy
DROP TABLE IF EXISTS `buy`;
CREATE TABLE IF NOT EXISTS `buy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` int(11) DEFAULT NULL,
  `concern` varchar(100) DEFAULT NULL,
  `payer_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `per_share` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table project_db.buy: ~0 rows (approximately)
DELETE FROM `buy`;
/*!40000 ALTER TABLE `buy` DISABLE KEYS */;
/*!40000 ALTER TABLE `buy` ENABLE KEYS */;

-- Dumping structure for table project_db.message
DROP TABLE IF EXISTS `message`;
CREATE TABLE IF NOT EXISTS `message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_reciver` int(11) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `date_buy` date DEFAULT NULL,
  PRIMARY KEY (`id`,`user_id`),
  KEY `fk_message2_user1_idx` (`user_id`),
  CONSTRAINT `fk_message2_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table project_db.message: ~0 rows (approximately)
DELETE FROM `message`;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
/*!40000 ALTER TABLE `message` ENABLE KEYS */;

-- Dumping structure for table project_db.note
DROP TABLE IF EXISTS `note`;
CREATE TABLE IF NOT EXISTS `note` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime DEFAULT NULL,
  `text` varchar(45) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`,`user_id`),
  KEY `fk_job_user1_idx` (`user_id`),
  CONSTRAINT `fk_job_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table project_db.note: ~0 rows (approximately)
DELETE FROM `note`;
/*!40000 ALTER TABLE `note` DISABLE KEYS */;
/*!40000 ALTER TABLE `note` ENABLE KEYS */;

-- Dumping structure for table project_db.payment
DROP TABLE IF EXISTS `payment`;
CREATE TABLE IF NOT EXISTS `payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` int(11) DEFAULT NULL,
  `type` tinyint(1) DEFAULT NULL,
  `payer_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`user_id`),
  KEY `fk_payment_user1_idx` (`user_id`),
  CONSTRAINT `fk_payment_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table project_db.payment: ~0 rows (approximately)
DELETE FROM `payment`;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;

-- Dumping structure for table project_db.user
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `user` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `account` varchar(45) DEFAULT NULL,
  `picture_address` varchar(45) DEFAULT NULL,
  `type` tinyint(1) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`,`user`)
) ENGINE=InnoDB AUTO_INCREMENT=2332150 DEFAULT CHARSET=utf8;

-- Dumping data for table project_db.user: ~0 rows (approximately)
DELETE FROM `user`;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`id`, `name`, `user`, `email`, `password`, `account`, `picture_address`, `type`, `user_id`, `status`) VALUES
	(2332149, 'سید مجتبی بنائی', 'smbanaie', 'mojtaba.banaie@gmail.com', '123456', '0', '1ea2a2de-40fa-495d-9227-531f75285f7a.jpg', 1, 2332149, 3);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

-- Dumping structure for table project_db.user_has_buy
DROP TABLE IF EXISTS `user_has_buy`;
CREATE TABLE IF NOT EXISTS `user_has_buy` (
  `user_id` int(11) NOT NULL,
  `buy_id` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`,`user_id`,`buy_id`),
  KEY `fk_user_has_buy_buy1_idx` (`buy_id`),
  KEY `fk_user_has_buy_user1_idx` (`user_id`),
  CONSTRAINT `fk_user_has_buy_buy1` FOREIGN KEY (`buy_id`) REFERENCES `buy` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_has_buy_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table project_db.user_has_buy: ~0 rows (approximately)
DELETE FROM `user_has_buy`;
/*!40000 ALTER TABLE `user_has_buy` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_has_buy` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
