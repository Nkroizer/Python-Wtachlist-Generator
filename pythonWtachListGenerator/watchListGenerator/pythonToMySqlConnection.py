import mysql.connector
import csv
from imdb import IMDb
import requests
import json
import pythonWtachListGenerator.watchListGenerator.conversionFunctions as conversionFunctions


def responseToData(response):
    x = response.text.encode('utf8')
    res = json.loads(x)
    try:
        return res["data"]
    except:
        print(res)
        return []


def getToken():
    url = "https://api.thetvdb.com/login"

    payload = "{\r\n  \"apikey\": \"68598ddce1a4c00eb4043bcf3675a4ea\",\r\n  \"userkey\": \"5E95993E26FF76.31716214\",\r\n  \"username\": \"kroizer21\"\r\n}"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    x = response.text.encode('utf8')
    res = json.loads(x)
    return res["token"]


def getTVDBIdByIMDBId(imdbID, token):
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


def getRating(episode_obj):
    try:
        rating = episode_obj["rating"]
        return rating
    except:
        return 0


def getAirDate(episode_obj):
    try:
        EAirdate = episode_obj["original air date"]
    except:
        EAirdate = "1 Jan. 1900"

    if len(EAirdate) < 10:
        EAirdate = "1 Jan. 1900"
    if "May" in str(EAirdate) and not("May." in str(EAirdate)):
        EAirdate = EAirdate.replace('May', 'May.')

    return conversionFunctions.DateFormatToMySqlFormat(EAirdate)


def getYear(episode_obj):
    try:
        year = episode_obj["year"]
        return year
    except:
        return 0


def getPlot(episode_obj):
    try:
        plot = episode_obj["plot outline"]
        return plot
    except:
        return "No plot ouline"


def getCleanShowName(showName):
    cleanName = showName.replace(" ", "")
    cleanName = cleanName.replace(":", "")
    cleanName = cleanName.replace("-", "")
    cleanName = cleanName.replace("!", "")
    cleanName = cleanName.replace("?", "")
    cleanName = cleanName.replace(".", "")
    cleanName = cleanName.lower()
    return cleanName


def insertAllShowRecords():
    f = open(
        "pythonWtachListGenerator\\watchListGenerator\\Files\\Show Links.txt", "r")
    if f.mode == 'r':
        f1 = f.readlines()
        for x in f1:
            text = x.split(' : ')
            imdbId = text[1]
            insertSingleShowRecord(imdbId)
    f.close()


def insertSingleShowRecord(imdbId):
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
    ShowTitle = series["original title"]
    lastDig = ShowTitle[len(ShowTitle) - 3: len(ShowTitle) - 2]
    active = 0
    if lastDig == '-':
        active = 1
    tvdbId = getTVDBIdByIMDBId(imdbId, token)
    sql = "INSERT INTO shows (showName, releaseYear, seasons, active, imdbId, tvdbId, plot, coverUrl, fullSizeCoverUrl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (str(showName), releaseYear, seasons, active, imdbId,
           tvdbId, str(plot), str(coverUrl), str(fullSizeCoverUrl))
    try:
        mycursor.execute(sql, val)
        mydb.commit()
    except:
        print("E?")
        print(val)
    print("finished with " + str(showName))
    print(mycursor.rowcount, "record inserted.")


def insertAllEpisodeRecords():
    f = open(
        "pythonWtachListGenerator\\watchListGenerator\\Files\\Show Links.txt", "r")
    if f.mode == 'r':
        f1 = f.readlines()
        for x in f1:
            text = x.split(' : ')
            imdbId = text[1]
            insertSingleEpisodeRecord(imdbId)
    f.close()


def insertSingleEpisodeRecord(imdbIdIns):
    mainImdbId = int(imdbIdIns)
    ia = IMDb()
    token = getToken()
    tvdbId = getTVDBIdByIMDBId(imdbIdIns, token)
    mainTvdbId = tvdbId
    series = ia.get_movie(imdbIdIns)
    showName = series["title"]
    ia.update(series, "episodes")
    SeasonsArr = sorted(series["episodes"].keys())
    for SeasonNum in SeasonsArr:
        seasonx = series["episodes"][SeasonNum]
        EpisodeArr = sorted(seasonx)
        for episodz in EpisodeArr:
            episode_obj = series["episodes"][SeasonNum][episodz]
            season = episode_obj["season"]
            episode = episode_obj["episode"]
            title = episode_obj["title"]
            kind = episode_obj["kind"]
            rating = getRating(episode_obj)
            airDate = getAirDate(episode_obj)
            year = getYear(episode_obj)
            plot = episode_obj["plot"]
            imdbId = 0
            tvdbId = 0
            watched = 0
            wasIncremented = 0
            verified = 0
            episodeCode = getCleanShowName(
                showName) + "S" + str(season) + "E" + str(episode)
            sql = "INSERT INTO episodes (showName, season, episode, title, kind, rating, airDate, year, plot, mainImdbId, mainTvdbId, imdbId, tvdbId, watched, wasIncremented, verified, episodeCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (str(showName), season, episode, str(title), str(kind),
                   rating, airDate, year, str(plot), mainImdbId, mainTvdbId, imdbId, tvdbId, watched, wasIncremented, verified, str(episodeCode))
            try:
                mycursor.execute(sql, val)
                mydb.commit()
            except:
                print("E?")
                print(val)
    print("finished with " + str(showName))


def selectAllFromShows():
    mycursor.execute("SELECT * FROM shows")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)


def createdatabase():
    sql = r"CREATE DATABASE watchlistdatabase"
    return sql


def createShowsTabel():
    sql = r"CREATE TABLE shows (id INT AUTO_INCREMENT PRIMARY KEY, showName VARCHAR(255), releaseYear INT, seasons INT, active BIT, imdbId INT UNIQUE, tvdbId INT UNIQUE, plot VARCHAR(1500), coverUrl VARCHAR(255), fullSizeCoverUrl VARCHAR(255))"
    return sql


def createEpisodesTabel():
    sql = r"CREATE TABLE episodes (showName VARCHAR(255), season INT, episode INT, title VARCHAR(255), kind VARCHAR(255), rating FLOAT, airDate DATE, year INT, plot VARCHAR(1500), mainImdbId INT, mainTvdbId INT, imdbId INT, tvdbId INT, watched BIT, wasIncremented BIT, verified BIT, episodeCode VARCHAR(255) UNIQUE)"
    return sql


def initDataBases():
    command = createdatabase()
    mycursor.execute(command)
    command = createShowsTabel()
    mycursor.execute(command)
    command = createEpisodesTabel()
    mycursor.execute(command)


def checkIfTableExists():
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print(x)


def ImdbFileToDb():
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


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pwlg2020",
    database="watchlistDatabase"
)

mycursor = mydb.cursor()

# mycursor.execute("SELECT imdbId FROM shows")

# myresult = mycursor.fetchall()

# initDataBases()
# mycursor.execute(sql)

# insertAllShowRecords()
# ImdbFileToDb()
# insertSingleEpisodeRecord("0318252")
