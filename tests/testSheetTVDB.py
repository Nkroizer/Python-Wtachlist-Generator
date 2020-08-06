import requests
import json
from WatchListFunctions import cleanFileName
import csv


def responseToData(response):
    x = response.text.encode('utf8')
    res = json.loads(x)
    return res["data"]


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


def refreshToken():
    url = "https://api.thetvdb.com/refresh_token"
    token = getToken()
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + str(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    x = response.text.encode('utf8')
    res = json.loads(x)
    return res["token"]


def searchDB(strSeasrch, token):
    url = "https://api.thetvdb.com/search/series?name=" + str(strSeasrch)
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + str(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = responseToData(response)

    res2 = data[0]

    for y in res2:
        print(y)
        print(res2[y])

    print(len(data))


def getSeriesName(tvdbID, token):
    url = "https://api.thetvdb.com/series/" + str(tvdbID)

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + str(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = responseToData(response)

    return data["seriesName"]


def EpisodesInformation(showId, token):
    url = "https://api.thetvdb.com/series/" + str(showId) + "/episodes"
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + str(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = responseToData(response)

    title = getSeriesName(showId, token)
    cleanTitle = cleanFileName(title)
    with open("pythonWtachListGenerator\\watchListGenerator\\Local DB2\\" + cleanTitle + ".csv", 'w', newline='') as csvfile:
        showWriter = csv.writer(csvfile)
        for a in data:
            try:
                ESeason = str(a["airedSeason"])
                print(ESeason)
                Eepisode = str(a["airedEpisodeNumber"])
                print(Eepisode)
                ETitle = str(a["episodeName"])
                print(ETitle)
                if "," in ETitle:
                    ETitle = ETitle.replace(',', ' ')
                EAirdate = str(a["firstAired"])
                print(EAirdate)
                Erate = str(a["siteRating"])
                print(Erate)
                print("Season: " + str(ESeason) + " Episode: " + str(Eepisode))
                try:
                    showWriter.writerow(
                        [str(ESeason), str(Eepisode), str(ETitle), str(EAirdate), str(Erate)])
                except:
                    print("a?")
                    showWriter.writerow(
                        [str(ESeason), str(Eepisode), "bad tite encoding", str(EAirdate), str(Erate)])
                print("Finished working on: " + cleanTitle)
            except:
                print("oops")
        print("------------------------------------------------------")


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


def RegenerateLocalDB():
    token = getToken()
    f = open(
        "pythonWtachListGenerator\\watchListGenerator\\Files\\Show Links.txt", "r")
    if f.mode == 'r':
        f1 = f.readlines()
        for x in f1:
            text = x.split(' : ')
            strid = text[1]
            strid = strid[0: len(strid) - 1]
            tvdbId = getTVDBIdByIMDBId(strid, token)
            EpisodesInformation(tvdbId, token)


RegenerateLocalDB()
# searchDB("Naruto") #78857
# EpisodesInformation(78857)
