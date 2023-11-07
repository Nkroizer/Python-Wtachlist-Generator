import pythonWtachListGenerator.watchListGenerator.PythonToMySqlConnection as _PTMC
from imdb import IMDb
import mysql.connector

def insert_single_episode_record(imdbIdIns):
    mainImdbId = int(imdbIdIns)
    ia = IMDb()
    token = _PTMC.PythonToMySqlConnection.get_token()
    tvdbId = _PTMC.PythonToMySqlConnection.get_tvdb_id_by_imdb_id(imdbIdIns, token)
    mainTvdbId = tvdbId
    series = ia.get_movie(imdbIdIns)
    showName = series["title"]
    ia.update(series, "episodes")
    SeasonsArr = sorted(series["episodes"].keys())
    firstYear = 0
    for SeasonNum in SeasonsArr:
        seasonx = series["episodes"][SeasonNum]
        EpisodeArr = sorted(seasonx)
        for episodz in EpisodeArr:
            episode_obj = series["episodes"][SeasonNum][episodz]
            season = episode_obj["season"]
            if not season == -1:
                if season < 10:
                    fixedSeason = "0" + str(season)
                else:
                    fixedSeason = str(season)
                episode = episode_obj["episode"]
                if episode < 10:
                    fixedEpisode = "0" + str(episode)
                else:
                    fixedEpisode = str(episode)
                title = episode_obj["title"]
                kind = episode_obj["kind"]
                rating = _PTMC.PythonToMySqlConnection.get_rating(episode_obj)
                airDate = _PTMC.PythonToMySqlConnection.get_air_date(episode_obj)
                year = _PTMC.PythonToMySqlConnection.get_year(episode_obj)
                if firstYear == 0:
                    firstYear = year
                plot = episode_obj["plot"]
                imdbId = 0
                tvdbId = 0
                watched = 0
                wasIncremented = 0
                verified = 0
                episodeCode = _PTMC.PythonToMySqlConnection.get_clean_show_name(showName) + "(" + str(firstYear) + ")" + "S" + fixedSeason + "E" + fixedEpisode
                oldEpisodeCode = _PTMC.PythonToMySqlConnection.get_clean_show_name(showName) + "S" + str(season) + "E" + str(episode)
                print(oldEpisodeCode)
                mycursor.execute("SELECT * FROM episodes WHERE episodeCode = '" + str(oldEpisodeCode) + "'")
                myresult = mycursor.fetchall()
                if((len(myresult) > 0) and (myresult[0][17] == 1)):
                    mycursor.execute("UPDATE episodes SET showName = '" + str(showName) + " (" + str(firstYear) + ")', episodeCode = '" + str(episodeCode) + "' WHERE episodeCode = '" + str(episodeCode) + "'")
                else:
                    print(episodeCode)
                    mycursor.execute("SELECT * FROM episodes WHERE episodeCode = '" + str(episodeCode) + "'")
                    myresult = mycursor.fetchall()
                    if((len(myresult) > 0) and (myresult[0][17] == 1)):
                        print("entry allready exists and verified")
                    else:
                        sql = "INSERT INTO episodes (showName, season, episode, title, kind, rating, airDate, year, plot, canonUniverse, nonCanonUniverse, mainImdbId, mainTvdbId, imdbId, tvdbId, watched, wasIncremented, verified, episodeCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        val = (str(showName) + " (" + str(firstYear) + ")", season, episode, str(title), str(kind),
                            rating, airDate, year, str(plot), "", "", mainImdbId, mainTvdbId, imdbId, tvdbId, watched, wasIncremented, verified, str(episodeCode))
                        try:
                            mycursor.execute(sql, val)
                            mydb.commit()
                            print("Done with: " +str(episodeCode))
                        except:
                            print("E?")
                            print(val)
    print("finished with " + str(showName))

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pwlg2020",
    database="watchlistDatabase"
)

mycursor = mydb.cursor()
# mycursor.execute("SELECT * FROM episodes WHERE mainImdbId = 8421350")
# myresult = mycursor.fetchall()
# print(myresult[0][17])
insert_single_episode_record(2243973)