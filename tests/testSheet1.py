# # Reading an excel file using Python
# import xlrd

# # Give the location of the file
# loc = ("C:\\Users\\Quickode\\Desktop\\xyz\\Watchlists\\2002 Watchlist.xlsx")

# # To open Workbook
# wb = xlrd.open_workbook(loc)
# sheet = wb.sheet_by_index(0)

# # For row 0 and column 0
# r = 0
# true1 = True
# while true1:
#     for c in range(0, 11):
#         try:
#             a = sheet.cell_value(r, c)
#         except:
#             true1 = False
#         print(a)
#     r += 1


# import time
# import sys

# toolbar_width = 40

# # setup toolbar
# sys.stdout.write("[%s]" % (" " * toolbar_width))
# sys.stdout.flush()
# sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

# for i in range(toolbar_width):
#     time.sleep(0.1) # do real work here
#     # update the bar
#     sys.stdout.write("-")
#     sys.stdout.flush()

# sys.stdout.write("]\n") # this ends the progress bar

# importing tkinter module

import pathlib
from imdb import IMDb
import requests
import json

# INSERT INTO shows (showName, releaseYear, seasons, active, imdbId, tvdbId, plot, coverUrl, fullSizeCoverUrl)
# VALUES (value1, value2, value3, ...);


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


ia = IMDb()
directory = pathlib.Path().absolute()
f = open("pythonWtachListGenerator\\watchListGenerator\\Files\\Show Links.txt", "r")
token = getToken()
sqlScript = r"INSERT INTO shows (showName, releaseYear, seasons, active, imdbId, tvdbId, plot, coverUrl, fullSizeCoverUrl)" + "\nVALUES"
fi = open("pythonWtachListGenerator\\watchListGenerator\\Files\\Sql script.txt", "w+")
if f.mode == 'r':
    f1 = f.readlines()
    for x in f1:
        text = x.split(' : ')
        showName = text[0]
        imdbId = text[1]
        series = ia.get_movie(imdbId)
        a1 = series.keys()
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
        sqlScript += "(\'" + str(showName) + "\'," + str(releaseYear) + "," + str(seasons) + "," + str(active) + "," + str(
            imdbId) + "," + str(tvdbId) + ",\'" + str(plot) + "\',\'" + str(coverUrl) + "\',\'" + str(fullSizeCoverUrl) + "\');\n"
fi.write(sqlScript)
fi.close()
f.close()
