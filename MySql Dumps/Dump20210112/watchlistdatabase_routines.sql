-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: watchlistdatabase
-- ------------------------------------------------------
-- Server version	8.0.21

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
-- Dumping events for database 'watchlistdatabase'
--

--
-- Dumping routines for database 'watchlistdatabase'
--
/*!50003 DROP PROCEDURE IF EXISTS `_add_Days_to_To_Episode` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `_add_Days_to_To_Episode`(
	IN episodeCodeFunc VARCHAR(255),
    days int
)
BEGIN
	SELECT 
		airDate
	INTO
		@airDate
	FROM 
		watchlistdatabase.episodes
	WHERE 
		episodeCode = episodeCodeFunc;
    
      UPDATE watchlistdatabase.episodes es SET es.airDate = DATE_ADD(@airDate, INTERVAL days DAY) WHERE es.episodeCode = episodeCodeFunc;
      
      select * from episodes WHERE episodeCode = episodeCodeFunc;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `_add_Plus_1_To_Air_Date` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `_add_Plus_1_To_Air_Date`(
	IN showName VARCHAR(255)
)
BEGIN
   DECLARE cursor_List_isdone BOOLEAN DEFAULT FALSE;
   DECLARE cur_airDate date;
   DECLARE cur_code VARCHAR(250) DEFAULT '';

   DECLARE cursor_List CURSOR FOR 
      select e1.airDate, e1.episodeCode from watchlistdatabase.episodes e1 where e1.showName = showName and e1.wasIncremented = 0 and e1.verified = 0
    ;

   DECLARE CONTINUE HANDLER FOR NOT FOUND SET cursor_List_isdone = TRUE;

   OPEN cursor_List;

   loop_List: LOOP
      FETCH cursor_List INTO cur_airDate, cur_code;
      IF cursor_List_isdone THEN
         LEAVE loop_List;
      END IF;

      UPDATE watchlistdatabase.episodes es SET es.airDate = DATE_ADD(cur_airDate, INTERVAL 1 DAY), es.wasIncremented = 1 WHERE es.episodeCode = cur_code;

   END LOOP loop_List;

   CLOSE cursor_List;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `_Remove_Plus_1_To_Air_Date` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `_Remove_Plus_1_To_Air_Date`(
	IN showName VARCHAR(255)
)
BEGIN
   DECLARE cursor_List_isdone BOOLEAN DEFAULT FALSE;
   DECLARE cur_airDate date;
   DECLARE cur_code VARCHAR(250) DEFAULT '';

   DECLARE cursor_List CURSOR FOR 
      select e1.airDate, e1.episodeCode from watchlistdatabase.episodes e1 where e1.showName = showName and e1.verified = 0
    ;

   DECLARE CONTINUE HANDLER FOR NOT FOUND SET cursor_List_isdone = TRUE;

   OPEN cursor_List;

   loop_List: LOOP
      FETCH cursor_List INTO cur_airDate, cur_code;
      IF cursor_List_isdone THEN
         LEAVE loop_List;
      END IF;

      UPDATE watchlistdatabase.episodes es SET es.airDate = DATE_ADD(cur_airDate, INTERVAL -1 DAY) WHERE es.episodeCode = cur_code;

   END LOOP loop_List;

   CLOSE cursor_List;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-12 15:46:51
