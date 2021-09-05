select showName, count(*) as cnt from episodes 
where verified = 0
group by showName order by cnt asc;

select verified, count(*) as cnt from episodes 
group by verified order by cnt asc;

select * from episodes where showName like '%The Simpsons%' order by airDate asc;

delete from episodes where episodeCode = 'pokémon(1997)S03E42';

select * from episodes where mainImdbId = '7686464';

UPDATE episodes SET verified = 1 where showName = 'Gravity Falls (2012)';

UPDATE episodes SET watched = 1 where showName = 'Under the Dome (2013)'
and season = 5;

select * from episodes where showName = 'Bleach: Burîchi' and verified = 0 order by airDate, episode asc;

select * from episodes where showName = 'Bleach: Burîchi' and verified = 0 and season = 12 order by airDate, episode asc;


delete from episodes where showName = 'Steven Universe'
and season = 10;

delete from episodes where airDate = '1900-01-01';


UPDATE episodes SET verified = 1 where showName = 'Twin Peaks (1990)';

UPDATE episodes SET watched = 1 where showName = 'Twin Peaks (1990)';

CALL `watchlistdatabase`.`_add_Plus_1_To_Air_Date`('Gravity Falls (2012)');

CALL `watchlistdatabase`.`_Remove_Plus_1_To_Air_Date`('His Dark Materials (2019)');

CALL `watchlistdatabase`.`_add_Days_to_To_Episode`('bleachburîchiS1E5', 1);

UPDATE episodes SET airDate = '2001-05-04' where episodeCode = 'survivorS2E15';

UPDATE episodes SET season = 2, episode = 3, episodeCode = 'yugiohzexalS2E3' where episodeCode = 'yugiohzexalS-1E-1';

UPDATE episodes SET season = 1, episode = 28, episodeCode = 'yugiohzexalS1E28' where episodeCode = 'yugiohzexalS2E3';

UPDATE episodes SET showName = 'The Twilight Zone (2002)' where mainImdbId = 318252;

select count(*) as cnt from episodes where verified = 1;
select count(*) as cnt from episodes where verified = 0;

UPDATE episodes SET title = 'Build the Most Powerful Deck!' where episodeCode = 'thedisastrouslifeofsaikikS3E2';

INSERT INTO episodes (showName, season, episode, title, kind, rating, airDate, year, plot, mainImdbId, mainTvdbId, imdbId, tvdbId, watched, wasIncremented, verified, episodeCode) 
VALUES ('King Arthur and the Knights of Justice', 2, 13, 'Tone\'s Triumph', 'episode', 0, '1993-12-12', 1993, 'N/A', 292411, 70453, 0, 0, 0, 0, 0, 'kingarthurandtheknightsofjusticeS2E13');

select * from episodes where showName like '%King Arthur and the Knights of Justice%' order by airDate asc;

select distinct showName, imdbId from episodes where showName not in (select distinct showName from shows);
select distinct showName from shows where showName not in (select distinct showName from episodes);


select * from watchlistdatabase.episodes es where es.airDate = '1900-01-01' and es.year > 0 order by es.year asc;
select * from watchlistdatabase.episodes es where es.episodeCode = 'saturdaynightliveS10E1';

ALTER TABLE episodes
ADD COLUMN verified BIT AFTER wasIncremented;


UPDATE episodes SET airDate = '2015-05-17' where episodeCode = 'jonathanstrange&mrnorrellS1E1';


DROP PROCEDURE IF EXISTS _add_Plus_1_To_Air_Date;
DELIMITER $$
CREATE PROCEDURE _add_Plus_1_To_Air_Date(
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
END

$$

DELIMITER ;

DROP PROCEDURE IF EXISTS _Remove_Plus_1_To_Air_Date;
DELIMITER $$
CREATE PROCEDURE _Remove_Plus_1_To_Air_Date(
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
END

$$

DELIMITER ;

DROP PROCEDURE IF EXISTS _add_Days_to_To_Episode;
DELIMITER $$
CREATE PROCEDURE _add_Days_to_To_Episode(
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
END

$$

DELIMITER ;

CREATE DATABASE watchlistdatabase;

CREATE DATABASE pokedex;

ALTER TABLE episodes MODIFY episodeCode VARCHAR(255) UNIQUE NOT NULL;
