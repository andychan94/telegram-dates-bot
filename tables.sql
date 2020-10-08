--
-- Table structure for table `group_dates`
--

DROP TABLE IF EXISTS `group_dates`;

CREATE TABLE `group_dates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `date_type` varchar(40) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `img_path` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `user_state`
--

DROP TABLE IF EXISTS `user_state`;

CREATE TABLE `user_state` (
  `id` varchar(40) NOT NULL,
  `state` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;