from imdb import IMDb
import requests
import json

class GenerateScriptForSqlServer:
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
        res2 = data[0]
        tvdbID = res2["id"]
        return tvdbID


    def generate_all(self):
        ia = IMDb()
        f = open("pythonWtachListGenerator\\watchListGenerator\\Files\\Show Links.txt", "r")
        token = self.get_token()
        sqlScript = r"INSERT INTO shows (showName, releaseYear, seasons, active, imdbId, tvdbId, plot, coverUrl, fullSizeCoverUrl)" + "\nVALUES\r"
        fi = open("pythonWtachListGenerator\\watchListGenerator\\Files\\Sql script.txt", "w+")
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
                tvdbId = self.get_tvdb_id_by_imdb_id(imdbId, token)
                sqlScript = "(\'" + str(showName) + "\'," + str(releaseYear) + "," + str(seasons) + "," + str(active) + "," + str(imdbId) + "," + str(tvdbId) + ",\'" + str(plot) + "\',\'" + str(coverUrl) + "\',\'" + str(fullSizeCoverUrl) + "\');\r"
                fi = open("pythonWtachListGenerator\\watchListGenerator\\Files\\Sql script.txt", "a+")
                fi.write(sqlScript)
                fi.close()
                print("finished with " + str(showName))
        f.close()


    def generate_single(self, imdbId):
        ia = IMDb()
        token = self.get_token()
        sqlScript = r"INSERT INTO shows (showName, releaseYear, seasons, active, imdbId, tvdbId, plot, coverUrl, fullSizeCoverUrl)" + "\nVALUES\r"
        fi = open("pythonWtachListGenerator\\watchListGenerator\\Files\\Sql script.txt", "w+")
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
        tvdbId = self.get_tvdb_id_by_imdb_id(imdbId, token)
        sqlScript = "(\'" + str(showName) + "\'," + str(releaseYear) + "," + str(seasons) + "," + str(active) + "," + str(imdbId) + "," + str(tvdbId) + ",\'" + str(plot) + "\',\'" + str(coverUrl) + "\',\'" + str(fullSizeCoverUrl) + "\');\r"
        fi = open("pythonWtachListGenerator\\watchListGenerator\\Files\\Sql script.txt", "a+")
        fi.write(sqlScript)
        fi.close()
        print("finished with " + str(showName))
        