select showName, count(*) as cnt from watchlistdatabase.episodes 
where verified = 0 and watched = 0
group by showName order by cnt asc;

select * from episodes where showName = 'The Mandalorian';

select * from episodes where showName = 'Saturday Night Live' and season = 15;

select * from episodes where showName = 'The Simpsons' and season = 4;

select * from episodes where episodeCode = 'agentsofs.h.i.e.l.d.S7E13';

CALL `watchlistdatabase`.`_add_Plus_1_To_Air_Date`('Watchmen');

UPDATE episodes SET airDate = '2020-07-15' where episodeCode = 'pokémontwilightwingsS1E6';

UPDATE episodes SET episodeCode = 'saturdaynightliveS10E17' where episodeCode = 'saturdaynightliveS10E18';

UPDATE episodes SET airDate = '1984-10-07' where showName = 'Pokémon Origins';

UPDATE episodes SET verified = 1 where showName = 'The Mandalorian';

UPDATE episodes SET watched = 1 where showName = 'Inhumans';

UPDATE episodes SET watched = 1 where showName = 'Pokémon' and season = 10;

UPDATE episodes SET verified = 1 where showName = 'Saturday Night Live' and season = 15;

UPDATE episodes SET verified = 1 where showName = 'The Simpsons' and season = 4;

select count(*) as cnt from episodes where verified = 1;

DELETE FROM episodes WHERE episodeCode = 'themandalorianS3E1';

INSERT INTO episodes (showName, season, episode, title, kind, rating, airDate, year, plot, mainImdbId, mainTvdbId, imdbId, tvdbId, watched, wasIncremented, verified, episodeCode) 
VALUES ('Pokémon Chronicles', 1, 22, 'Pikachu''s Winter Vacation', 'episode', 0, '2006-11-26', 2006, 'N/A', 1294022, 0, 0, 0, 1, 0, 1, 'pokémonchroniclesS1E22');


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

INSERT INTO episodes (showName, season, episode, title, kind, rating, airDate, year, plot, mainImdbId, mainTvdbId, imdbId, tvdbId, watched, wasIncremented, verified, episodeCode) 
VALUES ('South Park', 24, 1, 'Episode #24.1', 'episode', 0, '1900-01-01', 0, '\n  Know what this is about?\n Be the first one to add a plot.\n    ', 121955, 75897, 0, 0, 0, 0, 0, 'southparkS24E1')


