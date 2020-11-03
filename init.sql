USE mydb;
DROP TABLE IF EXISTS `mytest`;
SET character_set_client = utf8mb4 ;

-- mydb.mytest definition

CREATE TABLE `mytest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `password` blob DEFAULT NULL,
  `file` varchar(100) NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;