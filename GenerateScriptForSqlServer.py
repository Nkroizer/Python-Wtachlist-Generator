from imdb import IMDb
import requests
import json


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
    res2 = data[0]
    tvdbID = res2["id"]
    return tvdbID


def generateAll():
    ia = IMDb()
    f = open("Files\\Show Links.txt", "r")
    token = getToken()
    sqlScript = r"INSERT INTO shows (showName, releaseYear, seasons, active, imdbId, tvdbId, plot, coverUrl, fullSizeCoverUrl)" + "\nVALUES\r"
    fi = open("Files\\Sql script.txt", "w+")
    fi.write(sqlScript)
    fi.close()
    if f.mode == 'r':
        f1 = f.readlines()
        for x in f1:
            text = x.split(' : ')
            showName = text[0]
            imdbId = text[1]
            series = ia.get_movie(imdbId)
            releaseYear = series["year"]
            seasons = series["seasons"]
            # plot = series["plot outline"]
            plot = "plot outline"
            coverUrl = series["cover url"]
            fullSizeCoverUrl = series["full-size cover url"]
            status = text[2]
            active = 0
            if status == "active":
                active = 1
            tvdbId = getTVDBIdByIMDBId(imdbId, token)
            sqlScript = "(\'" + str(showName) + "\'," + str(releaseYear) + "," + str(seasons) + "," + str(active) + "," + str(
                imdbId) + "," + str(tvdbId) + ",\'" + str(plot) + "\',\'" + str(coverUrl) + "\',\'" + str(fullSizeCoverUrl) + "\');\r"
            fi = open("Files\\Sql script.txt", "a+")
            fi.write(sqlScript)
            fi.close()
            print("finished with " + str(showName))
    f.close()


def generateSingle(imdbId):
    ia = IMDb()
    token = getToken()
    sqlScript = r"INSERT INTO shows (showName, releaseYear, seasons, active, imdbId, tvdbId, plot, coverUrl, fullSizeCoverUrl)" + "\nVALUES\r"
    fi = open("Files\\Sql script.txt", "w+")
    fi.write(sqlScript)
    fi.close()

    series = ia.get_movie(imdbId)
    releaseYear = series["year"]
    showName = series["title"]
    seasons = series["seasons"]
    # plot = series["plot outline"]
    plot = "plot outline"
    coverUrl = series["cover url"]
    fullSizeCoverUrl = series["full-size cover url"]
    ShowTitle = series["original title"]
    lastDig = ShowTitle[len(ShowTitle) - 3: len(ShowTitle) - 2]
    active = 0
    if lastDig == '-':
        active = 1
    tvdbId = getTVDBIdByIMDBId(imdbId, token)
    sqlScript = "(\'" + str(showName) + "\'," + str(releaseYear) + "," + str(seasons) + "," + str(active) + "," + str(
        imdbId) + "," + str(tvdbId) + ",\'" + str(plot) + "\',\'" + str(coverUrl) + "\',\'" + str(fullSizeCoverUrl) + "\');\r"
    fi = open("Files\\Sql script.txt", "a+")
    fi.write(sqlScript)
    fi.close()
    print("finished with " + str(showName))
