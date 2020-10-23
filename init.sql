USE mydb;
DROP TABLE IF EXISTS `mytest`;
SET character_set_client = utf8mb4 ;

CREATE TABLE `mytest`
(
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(20) NOT NULL,
	PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
