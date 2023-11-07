import ConversionFunctions as _CF
from imdb import IMDb
import requests
import json
import mysql.connector
import csv

class PythonToMySqlConnection:
    def response_to_data(self, response):
        x = response.text.encode('utf8')
        res = json.loads(x)
        try:
            return res["data"]
        except:
            print(res)
            return []


    def get_token(self):
        url = "https://api.thetvdb.com/login"

        payload = "{\r\n  \"apikey\": \"68598ddce1a4c00eb4043bcf3675a4ea\",\r\n  \"userkey\": \"5E95993E26FF76.31716214\",\r\n  \"username\": \"kroizer21\"\r\n}"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        x = response.text.encode('utf8')
        res = json.loads(x)
        return res["token"]


    def get_tvdb_id_by_imdb_id(self, imdbID, token):
        url = "https://api.thetvdb.com/search/series?imdbId=tt" + str(imdbID)
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + str(token)
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        data = self.response_to_data(response)
        try:
            res2 = data[0]
            tvdbID = res2["id"]
            return tvdbID
        except:
            return 0


    def get_rating(self, episode_obj):
        try:
            rating = episode_obj["rating"]
            return rating
        except:
            return 0


    def get_air_date(self, episode_obj):
        try:
            EAirdate = episode_obj["original air date"]
        except:
            EAirdate = "1 Jan. 1900"

        if len(EAirdate) < 10:
            EAirdate = "1 Jan. 1900"
        if "May" in str(EAirdate) and not("May." in str(EAirdate)):
            EAirdate = EAirdate.replace('May', 'May.')

        return _CF.ConversionFunctions.date_format_to_mySql_format(EAirdate)


    def get_year(self, episode_obj):
        try:
            year = episode_obj["year"]
            return year
        except:
            return 0


    def get_plot(self, episode_obj):
        try:
            plot = episode_obj["plot outline"]
            return plot
        except:
            return "No plot ouline"


    def get_clean_show_name(self, showName):
        cleanName = showName.replace(" ", "")
        cleanName = cleanName.replace(":", "")
        cleanName = cleanName.replace("-", "")
        cleanName = cleanName.replace("!", "")
        cleanName = cleanName.replace("?", "")
        cleanName = cleanName.replace(".", "")
        cleanName = cleanName.replace("'", "")
        cleanName = cleanName.lower()
        return cleanName


    def insert_all_show_records(self):
        f = open(
            "pythonWtachListGenerator\\watchListGenerator\\Files\\Show Links.txt", "r")
        if f.mode == 'r':
            f1 = f.readlines()
            for x in f1:
                text = x.split(' : ')
                imdbId = text[1]
                self.insert_single_show_record(imdbId)
        f.close()


    def insert_single_show_record(self, imdbId):
        ia = IMDb()
        token = self.get_token()
        series = ia.get_movie(imdbId)
        releaseYear = series["year"]
        showName = series["title"]
        seasons = series["seasons"]
        plot = self.get_plot(series)
        plot = plot[0: 1499]
        coverUrl = series["cover url"]
        fullSizeCoverUrl = series["full-size cover url"]
        try:
            ShowTitle = series["original title"]
        except:
            ShowTitle = series["title"]
        lastDig = ShowTitle[len(ShowTitle) - 3: len(ShowTitle) - 2]
        active = 0
        if lastDig == '-':
            active = 1
        tvdbId = self.get_tvdb_id_by_imdb_id(imdbId, token)
        sql = "INSERT INTO shows (showName, releaseYear, seasons, active, imdbId, tvdbId, plot, coverUrl, fullSizeCoverUrl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (str(showName), releaseYear, seasons, active, imdbId, tvdbId, str(plot), str(coverUrl), str(fullSizeCoverUrl))
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except:
            print("E?")
            print(val)
        print("finished with " + str(showName))
        print(mycursor.rowcount, "record inserted.")


    def insert_all_episode_records(self):
        f = open("pythonWtachListGenerator\\watchListGenerator\\Files\\Show Links.txt", "r")
        if f.mode == 'r':
            f1 = f.readlines()
            for x in f1:
                text = x.split(' : ')
                imdbId = text[1]
                self.insert_single_episode_record(imdbId)
        f.close()


    def insert_single_episode_record(self, imdbIdIns):
        mainImdbId = int(imdbIdIns)
        ia = IMDb()
        token = self.get_token()
        tvdbId = self.get_tvdb_id_by_imdb_id(imdbIdIns, token)
        mainTvdbId = tvdbId
        series = ia.get_movie(imdbIdIns)
        showName = series["title"]
        ia.update(series, "episodes")
        SeasonsArr = sorted(series["episodes"].keys())
        firstYear = 0
        latestSeason = 0
        mycursor.execute("select season from episodes where mainImdbId = '" + str(imdbIdIns) + "' and verified = 1 order by season, episode desc LIMIT 1")
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            latestSeason = myresult[0][0]
        for SeasonNum in SeasonsArr:
            if SeasonNum >= latestSeason: 
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
                        if not episode == 0:
                            if episode < 10:
                                fixedEpisode = "0" + str(episode)
                            else:
                                fixedEpisode = str(episode)
                            title = episode_obj["title"]
                            kind = episode_obj["kind"]
                            rating = self.get_rating(episode_obj)
                            airDate = self.get_air_date(episode_obj)
                            year = self.get_year(episode_obj)
                            if firstYear == 0:
                                firstYear = year
                            plot = episode_obj["plot"]
                            imdbId = 0
                            tvdbId = 0
                            watched = 0
                            wasIncremented = 0
                            verified = 0
                            episodeCode = self.get_clean_show_name(showName) + "(" + str(firstYear) + ")" + "S" + fixedSeason + "E" + fixedEpisode
                            fullShowName =  str(showName) + " (" + str(firstYear) + ")"
                            print(episodeCode)
                            mycursor.execute("SELECT * FROM episodes WHERE episodeCode = '" + str(episodeCode) + "'")
                            myresult = mycursor.fetchall()
                            if((len(myresult) > 0) and (myresult[0][17] == 1)):
                                print("entry allready exists and verified")
                            else:
                                sql = "INSERT INTO episodes (showName, season, episode, title, kind, rating, airDate, year, plot, canonUniverse, nonCanonUniverse, mainImdbId, mainTvdbId, imdbId, tvdbId, watched, wasIncremented, verified, episodeCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                val = ( str(fullShowName), season, episode, str(title), str(kind),
                                    rating, airDate, year, str(plot), "", "", mainImdbId, mainTvdbId, imdbId, tvdbId, watched, wasIncremented, verified, str(episodeCode))
                                try:
                                    mycursor.execute(sql, val)
                                    mydb.commit()
                                    print("Done with: " +str(episodeCode))
                                except:
                                    print("E?")
                                    print(val)
        print("finished with " + str(showName))


    def select_all_from_shows(self):
        mycursor.execute("SELECT * FROM shows")

        myresult = mycursor.fetchall()

        for x in myresult:
            print(x)


    def create_database(self):
        sql = r"CREATE DATABASE watchlistdatabase"
        return sql


    def create_shows_table(self):
        sql = r"CREATE TABLE shows (id INT AUTO_INCREMENT PRIMARY KEY, showName VARCHAR(255), releaseYear INT, seasons INT, active BIT, imdbId INT UNIQUE, tvdbId INT UNIQUE, plot VARCHAR(1500), coverUrl VARCHAR(255), fullSizeCoverUrl VARCHAR(255))"
        return sql


    def create_episodes_table(self):
        sql = r"CREATE TABLE episodes (showName VARCHAR(255), season INT, episode INT, title VARCHAR(255), kind VARCHAR(255), rating FLOAT, airDate DATE, year INT, plot VARCHAR(1500), mainImdbId INT, mainTvdbId INT, imdbId INT, tvdbId INT, watched BIT, wasIncremented BIT, verified BIT, episodeCode VARCHAR(255) UNIQUE)"
        return sql


    def init_databases(self):
        command = self.create_database()
        mycursor.execute(command)
        command = self.create_shows_table()
        mycursor.execute(command)
        command = self.create_episodes_table()
        mycursor.execute(command)


    def check_if_table_exists(self):
        mycursor.execute("SHOW TABLES")
        for x in mycursor:
            print(x)


    def imdb_file_to_db(self):
        with open("pythonWtachListGenerator\\watchListGenerator\\Tv Shows I Watch.csv", newline='') as csvfile:
            showCSV = csv.reader(csvfile, delimiter=',', quotechar='|')
            for cell in showCSV:
                x = cell[0]
                x = x[2: len(x)+2]
                print(x)
                mycursor.execute("SELECT imdbId FROM shows WHERE imdbId =" + x)
                myresult = mycursor.fetchall()
                if(len(myresult) < 1):
                    self.insert_single_show_record(x)
                    self.insert_single_episode_record(x)


    def force_update_episodes_year(self, imdbIdIns, showName, year):
        mycursor.execute("SELECT  * FROM episodes WHERE mainImdbId = '" + str(imdbIdIns) +"'")
        myresult = mycursor.fetchall()
        for i in range(len(myresult)):
            row = myresult[i]
            season = row[1]
            print("Season: " + str(season))
            if season < 10:
                fixedSeason = "0" + str(season)
            else:
                fixedSeason = str(season)
            episode = row[2]
            print("Episode: " + str(episode))
            if episode < 10:
                fixedEpisode = "0" + str(episode)
            else:
                fixedEpisode = str(episode)
            oldEpisodeCode = row[len(row) - 1]
            episodeCode = self.get_clean_show_name(showName) + "(" + str(year) + ")" + "S" + fixedSeason + "E" + fixedEpisode
            fullShowName =  str(showName) + " (" + str(year) + ")"
            mycursor.execute("UPDATE episodes SET showName = '" + str(fullShowName) + "', episodeCode = '" + str(episodeCode) + "' WHERE episodeCode = '" + str(oldEpisodeCode) + "'")
            print("episode code :" + str(oldEpisodeCode) + " Updated to " + str(episodeCode))
            mydb.commit()
        

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pwlg2020",
    database="watchlistDatabase"
)

mycursor = mydb.cursor()

