from helpers import _CF,_json,requests,IMDb,csv,mysql

class PythonToMySqlConnection:
    def responseToData(self, response):
        x = response.text.encode('utf8')
        res = _json.loads(x)
        try:
            return res["data"]
        except:
            print(res)
            return []


    def getToken(self):
        url = "https://api.thetvdb.com/login"

        payload = "{\r\n  \"apikey\": \"68598ddce1a4c00eb4043bcf3675a4ea\",\r\n  \"userkey\": \"5E95993E26FF76.31716214\",\r\n  \"username\": \"kroizer21\"\r\n}"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        x = response.text.encode('utf8')
        res = _json.loads(x)
        return res["token"]


    def getTVDBIdByIMDBId(self, imdbID, token):
        url = "https://api.thetvdb.com/search/series?imdbId=tt" + str(imdbID)
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + str(token)
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        data = responseToData(response)
        try:
            res2 = data[0]
            tvdbID = res2["id"]
            return tvdbID
        except:
            return 0


    def getRating(self, episode_obj):
        try:
            rating = episode_obj["rating"]
            return rating
        except:
            return 0


    def getAirDate(self, episode_obj):
        try:
            EAirdate = episode_obj["original air date"]
        except:
            EAirdate = "1 Jan. 1900"

        if len(EAirdate) < 10:
            EAirdate = "1 Jan. 1900"
        if "May" in str(EAirdate) and not("May." in str(EAirdate)):
            EAirdate = EAirdate.replace('May', 'May.')

        return _CF.ConversionFunctions.DateFormatToMySqlFormat(EAirdate)


    def getYear(self, episode_obj):
        try:
            year = episode_obj["year"]
            return year
        except:
            return 0


    def getPlot(self, episode_obj):
        try:
            plot = episode_obj["plot outline"]
            return plot
        except:
            return "No plot ouline"


    def getCleanShowName(self, showName):
        cleanName = showName.replace(" ", "")
        cleanName = cleanName.replace(":", "")
        cleanName = cleanName.replace("-", "")
        cleanName = cleanName.replace("!", "")
        cleanName = cleanName.replace("?", "")
        cleanName = cleanName.replace(".", "")
        cleanName = cleanName.replace("'", "")
        cleanName = cleanName.lower()
        return cleanName


    def insertAllShowRecords(self):
        f = open(
            "pythonWtachListGenerator\\watchListGenerator\\Files\\Show Links.txt", "r")
        if f.mode == 'r':
            f1 = f.readlines()
            for x in f1:
                text = x.split(' : ')
                imdbId = text[1]
                insertSingleShowRecord(imdbId)
        f.close()


    def insertSingleShowRecord(self, imdbId):
        ia = IMDb()
        token = getToken()
        series = ia.get_movie(imdbId)
        releaseYear = series["year"]
        showName = series["title"]
        seasons = series["seasons"]
        plot = getPlot(series)
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
        tvdbId = getTVDBIdByIMDBId(imdbId, token)
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


    def insertAllEpisodeRecords(self):
        f = open("pythonWtachListGenerator\\watchListGenerator\\Files\\Show Links.txt", "r")
        if f.mode == 'r':
            f1 = f.readlines()
            for x in f1:
                text = x.split(' : ')
                imdbId = text[1]
                insertSingleEpisodeRecord(imdbId)
        f.close()


    def insertSingleEpisodeRecord(self, imdbIdIns):
        mainImdbId = int(imdbIdIns)
        ia = IMDb()
        token = getToken()
        tvdbId = getTVDBIdByIMDBId(imdbIdIns, token)
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
                            rating = getRating(episode_obj)
                            airDate = getAirDate(episode_obj)
                            year = getYear(episode_obj)
                            if firstYear == 0:
                                firstYear = year
                            plot = episode_obj["plot"]
                            imdbId = 0
                            tvdbId = 0
                            watched = 0
                            wasIncremented = 0
                            verified = 0
                            episodeCode = getCleanShowName(showName) + "(" + str(firstYear) + ")" + "S" + fixedSeason + "E" + fixedEpisode
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


    def selectAllFromShows(self):
        mycursor.execute("SELECT * FROM shows")

        myresult = mycursor.fetchall()

        for x in myresult:
            print(x)


    def createdatabase(self):
        sql = r"CREATE DATABASE watchlistdatabase"
        return sql


    def createShowsTabel(self):
        sql = r"CREATE TABLE shows (id INT AUTO_INCREMENT PRIMARY KEY, showName VARCHAR(255), releaseYear INT, seasons INT, active BIT, imdbId INT UNIQUE, tvdbId INT UNIQUE, plot VARCHAR(1500), coverUrl VARCHAR(255), fullSizeCoverUrl VARCHAR(255))"
        return sql


    def createEpisodesTabel(self):
        sql = r"CREATE TABLE episodes (showName VARCHAR(255), season INT, episode INT, title VARCHAR(255), kind VARCHAR(255), rating FLOAT, airDate DATE, year INT, plot VARCHAR(1500), mainImdbId INT, mainTvdbId INT, imdbId INT, tvdbId INT, watched BIT, wasIncremented BIT, verified BIT, episodeCode VARCHAR(255) UNIQUE)"
        return sql


    def initDataBases(self):
        command = createdatabase()
        mycursor.execute(command)
        command = createShowsTabel()
        mycursor.execute(command)
        command = createEpisodesTabel()
        mycursor.execute(command)


    def checkIfTableExists(self):
        mycursor.execute("SHOW TABLES")
        for x in mycursor:
            print(x)


    def ImdbFileToDb(self):
        with open("pythonWtachListGenerator\\watchListGenerator\\Tv Shows I Watch.csv", newline='') as csvfile:
            showCSV = csv.reader(csvfile, delimiter=',', quotechar='|')
            for cell in showCSV:
                x = cell[0]
                x = x[2: len(x)+2]
                print(x)
                mycursor.execute("SELECT imdbId FROM shows WHERE imdbId =" + x)
                myresult = mycursor.fetchall()
                if(len(myresult) < 1):
                    insertSingleShowRecord(x)
                    insertSingleEpisodeRecord(x)


    def forceUpdateEpisodesYear(self, imdbIdIns, showName, year):
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
            episodeCode = getCleanShowName(showName) + "(" + str(year) + ")" + "S" + fixedSeason + "E" + fixedEpisode
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
# forceUpdateEpisodesYear(168366, "Pokémon" ,1997)

# mycursor.execute("SELECT imdbId FROM shows")

# myresult = mycursor.fetchall()

# initDataBases()
# mycursor.execute(sql)

# insertAllShowRecords()
# ImdbFileToDb()

# '121955',
# '397306',
# '475784',
# '1236246',
# '1305826',
# '1641384',
# '1898069',
# '2364582',
# '2560140',
# '2919910',
# '3107288',
# '4532368',
# '4955642',
# '5034326',
# '6279576',
# '8005374',
# '8425308',
# '8712204',
# '11192306',
# '98936',
# '4093826',
updatetArry = ['6741278']
for show in updatetArry:
    insertSingleEpisodeRecord(show)


