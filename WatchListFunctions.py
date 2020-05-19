import xlsxwriter
from tkinter import messagebox
from imdb import IMDb
from datetime import datetime, date, timedelta
import csv
import os
import pathlib
import pickle

columnToLetter = {"0": "A",
                  "1": "B",
                  "2": "C",
                  "3": "D",
                  "4": "E",
                  "5": "F",
                  "6": "G",
                  "7": "H",
                  "8": "I",
                  "9": "J",
                  "10": "K",
                  "11": "L",
                  "12": "M",
                  "13": "N",
                  "14": "O",
                  "15": "P",
                  "16": "Q",
                  "17": "R",
                  "18": "S",
                  "19": "T",
                  "20": "U",
                  "21": "V",
                  "22": "W",
                  "23": "X",
                  "24": "Y"}


def StrToDate(strDate):
    print("strDate: " + str(strDate))
    fixedDate = datetime.strptime(strDate, "%m/%d/%Y")
    return fixedDate


def DateFormatToListFormat(DateForm):
    ListForm = DateForm.strftime("%m/%d/%Y")
    return ListForm


def DaysLeftToInt(DL):
    strDl = str(DL)
    if "day" in strDl:
        NDL = strDl[0: strDl.find("day") - 1]
        return int(NDL)
    else:
        return 1


def RemoveEqualFromOldInfo(info):
    oldInfo = info
    if "=" in str(oldInfo):
        oldInfo = oldInfo[1: len(oldInfo)]
    return oldInfo


def cleanFileName(fileName):
    # Windows Unallowed chars: \/:*?"<>|
    cleanTitle = fileName
    if cleanTitle.find('\\'):
        cleanTitle = cleanTitle.replace('\\', '-')
    if cleanTitle.find('/'):
        cleanTitle = cleanTitle.replace('/', '-')
    if cleanTitle.find(':'):
        cleanTitle = cleanTitle.replace(':', '')
    if cleanTitle.find('*'):
        cleanTitle = cleanTitle.replace('*', '')
    if cleanTitle.find('?'):
        cleanTitle = cleanTitle.replace('?', '')
    if cleanTitle.find('"'):
        cleanTitle = cleanTitle.replace('"', '')
    if cleanTitle.find('<'):
        cleanTitle = cleanTitle.replace('<', '')
    if cleanTitle.find('>'):
        cleanTitle = cleanTitle.replace('>', '')
    if cleanTitle.find('|'):
        cleanTitle = cleanTitle.replace('|', '')
    return cleanTitle


def fixedPlaceEquation(rowNum):
    rowPlus1 = str(rowNum + 1)
    return '=IF(INT(G' + rowPlus1 + ')<10,CONCATENATE("00",G' + rowPlus1 + '),IF(INT(G' + rowPlus1 + ')<100,CONCATENATE("0",G' + rowPlus1 + '),G' + rowPlus1 + '))'


def fixedSeasonAndEpisodeNumberEquation(rowNum, letter):
    rowPlus1 = str(rowNum + 1)
    return '=IF(INT(' + letter + rowPlus1 + ')<10,CONCATENATE("0",' + letter + rowPlus1 + '),' + letter + rowPlus1 + ')'


def nameStickerEquation(rowNum):
    rowPlus1 = str(rowNum + 1)
    return '=CONCATENATE(H' + rowPlus1 + ',". ",A' + rowPlus1 + '," S",I' + rowPlus1 + ',"E",J' + rowPlus1 + ', " - ",D' + rowPlus1 + ')'


def mainWatchlistGeneratorFunction(showsToAdd, YOF, showMessage):
    workbook = xlsxwriter.Workbook(YOF + " Watchlist.xlsx")
    sheet1 = workbook.add_worksheet()
    sheet1.write(0, 0, 'Show')
    sheet1.write(0, 1, 'Season')
    sheet1.write(0, 2, 'Episode')
    sheet1.write(0, 3, 'Title')
    sheet1.write(0, 4, 'Air Date')
    sheet1.write(0, 5, 'Rating')
    sheet1.write(0, 6, 'Place In List')
    sheet1.write(0, 7, 'Fixed Place')
    sheet1.write(0, 8, 'Fixed Episode')
    sheet1.write(0, 9, 'Fixed Season')
    sheet1.write(0, 10, 'Name Sticker')
    row = 1
    TotalNumberOfEpisodes = 0
    exceptionString = ''
    formatDate = workbook.add_format({'num_format': 'd mmm yyyy'})
    for show in showsToAdd:
        print("Started working on: " + show)
        with open("Local DB/" + show, newline='') as csvfile:
            showCSV = csv.reader(csvfile, delimiter=' ', quotechar='|')
            try:
                for cell in showCSV:
                    Eshow = cleanFileName(show[0: len(show) - 4])
                    ESeason = cell[0]
                    Eepisode = cell[1]
                    ETitle = cleanFileName(cell[2])
                    EAirdate = cell[3]
                    try:
                        EAirdate = datetime.strptime(EAirdate, '%d %b. %Y')
                    except:
                        EAirdate = '2000-01-01 00:00:00'
                    Erate = cell[4]
                    if not YOF in str(EAirdate):
                        continue
                    TotalNumberOfEpisodes = TotalNumberOfEpisodes + 1
                    print('Season: ' + str(ESeason) +
                          ' Episode: ' + str(Eepisode))
                    sheet1.write(row, 0, Eshow)
                    sheet1.write(row, 1, ESeason)
                    sheet1.write(row, 2, Eepisode)
                    sheet1.write(row, 3, str(ETitle))
                    sheet1.write(row, 4, EAirdate, formatDate)
                    sheet1.write(row, 5, Erate)
                    sheet1.write(row, 6, 0)
                    sheet1.write(row, 7, str(fixedPlaceEquation(row)))
                    sheet1.write(row, 8, str(
                        fixedSeasonAndEpisodeNumberEquation(row, 'B')))
                    sheet1.write(row, 9, str(
                        fixedSeasonAndEpisodeNumberEquation(row, 'C')))
                    sheet1.write(row, 10, str(nameStickerEquation(row)))
                    row = row + 1
            except:
                print('S W W')
    if showMessage:
        messagebox.showinfo(
            "info", YOF + " Watchlist was Generated Successfuly \n Number of Episods: " + str(TotalNumberOfEpisodes))
    workbook.close()
    print('Success!')
    if exceptionString != '':
        print('Bad Shows: \n' + str(exceptionString))


def checkIfContainsYear(show, YOF):
    print("here")
    with open(r"Local DB\\" + show, newline='') as csvfile:
        showReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in showReader:
            if str(YOF) in row[3]:
                print("true true")
                return True
    return False


def extractIMDBIdFromLink(link):
    IdPlace = link.find('title/tt')
    IMDBID = link[IdPlace + 8: IdPlace + 15]
    print(IMDBID)
    return IMDBID


def generatAllWatchlists():
    directory = pathlib.Path().absolute()
    today = date.today()
    ThisYear = today.year
    oldestYear = "1900"
    isExistsFile = os.path.exists(
        str(directory) + '\\First Episode Information.txt')
    if not(isExistsFile):
        getDateOfFirstEpisodeInListFunc()
    f = open("First Episode Information.txt", "r")
    if f.mode == 'r':
        f1 = f.readlines()
        for x in f1:
            if "oldest year" in x:
                l1 = x.split()
                oldestYear = l1[2]
                print(oldestYear)
    f.close()
    year = int(oldestYear)
    ThisYear = int(ThisYear) + 1
    for x in range(year, ThisYear):
        shows = []
        for filename in os.listdir(str(directory) + r"\Local DB"):
            if ".csv" in filename:
                if checkIfContainsYear(filename, str(x)):
                    shows.append(filename)
        mainWatchlistGeneratorFunction(shows, str(x), False)


def getBadDatesFunc():
    directory = pathlib.Path().absolute()
    workbook = xlsxwriter.Workbook("Bad.xlsx")
    sheet1 = workbook.add_worksheet()
    sheet1.write(0, 0, "Show")
    sheet1.write(0, 1, "Season")
    sheet1.write(0, 2, "Episode")
    sheet1.write(0, 3, "Title")
    sheet1.write(0, 4, "Air Date")
    row = 1
    formatDate = workbook.add_format({'num_format': 'd mmm yyyy'})
    for filename in os.listdir(str(directory) + r"\Local DB"):
        if ".csv" in filename:
            with open(r"Local DB\\" + filename, newline='') as csvfile:
                showReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for cell in showReader:
                    if "1 Jan. 2000" in cell[3]:
                        ESeason = cell[0]
                        Eepisode = cell[1]
                        ETitle = cell[2]
                        EAirdate = cell[3]
                        sheet1.write(row, 0, str(cleanFileName(
                            filename[0: len(filename) - 4])))
                        sheet1.write(row, 1, ESeason)
                        sheet1.write(row, 2, Eepisode)
                        sheet1.write(row, 3, str(ETitle))
                        sheet1.write(row, 4, EAirdate, formatDate)
                        row = row + 1
    workbook.close()
    messagebox.showinfo("info", "Bad Dates List was Generated Successfuly")


def addShowClicked(link):
    showToAdd = extractIMDBIdFromLink(link)
    ia = IMDb()
    series = ia.get_movie(showToAdd)
    ia.update(series, "episodes")
    SeasonsArr = sorted(series["episodes"].keys())
    ShowTitle = series["title"]
    cleanTitle = cleanFileName(str(ShowTitle))
    print("Started working on: " + cleanTitle)
    with open("Local DB/" + cleanTitle + ".csv", 'w', newline='') as csvfile:
        showWriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for SeasonNum in SeasonsArr:
            print("Season: " + str(SeasonNum))
            seasonx = series["episodes"][SeasonNum]
            EpisodeArr = sorted(seasonx)
            try:
                for episodz in EpisodeArr:
                    episode = series["episodes"][SeasonNum][episodz]
                    ESeason = episode["season"]
                    Eepisode = episode["episode"]
                    ETitle = episode["title"]
                    if "," in ETitle:
                        ETitle = ETitle.replace(',', ' ')
                    try:
                        EAirdate = episode["original air date"]
                    except:
                        EAirdate = "1 Jan. 2000"
                    if len(EAirdate) < 10:
                        print("E: " + str(EAirdate))
                        EAirdate = "1 Jan. 2000"
                    try:
                        Erate = episode["rating"]
                    except:
                        Erate = 0
                    if Erate > 10:
                        Erate = 0
                    print("Season: " + str(ESeason) +
                          " Episode: " + str(Eepisode))
                    try:
                        showWriter.writerow(
                            [str(ESeason), str(Eepisode), str(ETitle), str(EAirdate), str(Erate)])
                    except:
                        showWriter.writerow(
                            [str(ESeason), str(Eepisode), "bad tite encoding", str(EAirdate), str(Erate)])
            except:
                print("An exception occurred trying to extract an episode")
        print("Finished working on: " + cleanTitle)
        print("-----------------------------------------")
    return cleanTitle


def getDateOfFirstEpisodeInListFunc():
    today = date.today()
    oldestDate = today.strftime("%m/%d/%Y")
    oldestDate = StrToDate(oldestDate)
    oldestYear = today.year
    oldestEpisode = ""
    print("new oldest date: " + str(oldestDate))
    print("new oldest year: " + str(oldestYear))
    directory = pathlib.Path().absolute()
    Oldest_Dates = {}
    for filename in os.listdir(str(directory) + r"\Local DB"):
        if ".csv" in filename:
            with open(r"Local DB\\" + filename, newline='') as csvfile:
                showReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for cell in showReader:
                    show = str(cleanFileName(filename[0: len(filename) - 4]))
                    ESeason = cell[0]
                    Eepisode = cell[1]
                    EAirdate = cell[3]
                    try:
                        EAirdate = datetime.strptime(EAirdate, "%d %b %Y")
                    except:
                        EAirdate = datetime.strptime(EAirdate, "%d %b. %Y")
                    Airdate = EAirdate.strftime("%m/%d/%Y")
                    Airdate = StrToDate(Airdate)
                    newYear = Airdate.year
                    if newYear < oldestYear:
                        print(str(oldestYear) + " ---> " + str(newYear))
                        oldestYear = newYear
                    if Airdate < oldestDate:
                        oldestDate = Airdate
                        oldestEpisode = show + " " + \
                            str(ESeason) + str(Eepisode)
                        print("new oldest date: " + str(oldestDate))
    Oldest_Dates["year"] = str(oldestYear)
    tmpDate = str(oldestDate)
    Oldest_Dates["date"] = tmpDate[0: len(tmpDate) - 9]
    print(Oldest_Dates["date"])
    Oldest_Dates["episode"] = str(oldestEpisode)
    pickle.dump(Oldest_Dates, open("First Episode Information.p", "wb"))


def intializeRawFile():
    directory = pathlib.Path().absolute()
    isExistsFirstDateFile = os.path.exists(
        str(directory) + 'First Episode Information.p')
    isExistsRawFile = os.path.exists(str(directory) + '\\raw.txt')
    if isExistsRawFile:
        messagebox.showinfo("Raw File Allready Exists")
    if not(isExistsFirstDateFile):
        getDateOfFirstEpisodeInListFunc()
    Oldest_Dates = pickle.load(open("First Episode Information.p", "rb"))
    oldestDate = Oldest_Dates["date"]
    oldestYear = Oldest_Dates["year"]
    oldestEpisode = Oldest_Dates["episode"]
    initialDate = datetime.strptime(oldestDate, "%Y-%m-%d")
    initialDateStr = initialDate.strftime("%m/%d/%Y")
    today = date.today() + timedelta(days=-10) 
    FirstDate = today.strftime("%m/%d/%Y") 
    totalDaysLeft = StrToDate(FirstDate) - StrToDate(initialDateStr)
    LatestInfo = {}
    
    f = open("raw.txt", "w+")
    # -------------------------------- Col A:A ---------------------------------- C
    f.write("0,0,DAYS(RMN),Equation_format\r")
    f.write("1,0,TODAY - DATE(RCHD),Equation_format\r")
    f.write("2,0,Days Remaining,Regular_format\r")
    f.write("3,0," + str(DaysLeftToInt(totalDaysLeft)) + " days,Output_format\r")
    LatestInfo["colA"] = str(DaysLeftToInt(totalDaysLeft)) + " days"
    # -------------------------------- Col B:B ---------------------------------- C
    f.write("0,1,DATE(RCHD),Equation_format\r")
    f.write("1,1,DATE(RCHD),Equation_format\r")
    f.write("2,1,Date Reached,Regular_format\r")
    f.write("3,1," + initialDateStr + ",Input_format\r")
    LatestInfo["colB"] = str(initialDateStr)
    # -------------------------------- Col C:C ----------------------------------
    f.write("0,2,DAYS(PSSD),Equation_format\r")
    f.write("1,2,DAYS(PSSD),Equation_format\r")
    f.write("2,2,Days Passed Since Last Log,Regular_format\r")
    f.write("3,2,=0,Nuetral_format\r")
    LatestInfo["colC"] = 0
    # -------------------------------- Col D:D ----------------------------------
    f.write("0,3,TODAY,Equation_format\r")
    f.write("1,3,(TODAY[N - 1]) + DAYS(PSSD),Equation_format\r")
    f.write("2,3,Today,Regular_format\r")
    f.write("3,3," + str(FirstDate) + ",Nuetral_format\r")
    LatestInfo["colD"] = str(FirstDate)
    # -------------------------------- Col E:E ----------------------------------
    f.write("0,4,DAYS(ADV),Equation_format\r")
    f.write("1,4,DAYS(RMN)[N] - DAYS(RMN)[N - 1],Equation_format\r")
    f.write("2,4,# Days Advanced,Regular_format\r")
    f.write("3,4,=0,Nuetral_format\r")
    LatestInfo["colE"] = 0
    # -------------------------------- Col F:F ----------------------------------
    f.write("0,5,XDAYS(ADV),Equation_format\r")
    f.write("1,5,AVG[N - 1]*DAYS(PSSD)[N],Equation_format\r")
    f.write("2,5,Expected Days Advancement,Regular_format\r")
    f.write("3,5,=0,Nuetral_format\r")
    LatestInfo["colF"] = 0
    # -------------------------------- Col G:G ----------------------------------
    f.write("0,6,#LDAYS(PSSD),Equation_format\r")
    f.write("1,6,SUM(DAYS(ADV)),Equation_format\r")
    f.write("2,6,# Of List Days Passed,Regular_format\r")
    f.write("3,6,=0,Nuetral_format\r")
    LatestInfo["colG"] = 0
    # -------------------------------- Col H:H ----------------------------------
    f.write("0,7,PDP,Equation_format\r")
    f.write("1,7,PDP[N] = PDP[N - 1] + DAYS(PSSD)[N],Equation_format\r")
    f.write("2,7,Phisical Days Passed,Regular_format\r")
    f.write("3,7,=0,Nuetral_format\r")
    LatestInfo["colH"] = 0
    # -------------------------------- Col I:I ----------------------------------
    f.write("0,8,AVG,Equation_format\r")
    f.write("1,8,#LDAYS(PSSD)/PDP,Equation_format\r")
    f.write("2,8,Average,Regular_format\r")
    f.write("3,8,=0,Nuetral_format\r")
    LatestInfo["colI"] = 0
    # -------------------------------- Col J:J ----------------------------------
    f.write("0,9,X,Equation_format\r")
    f.write("1,9,DAYS(RMN)/AVG,Equation_format\r")
    f.write("2,9,Days To Reach Current Date,Regular_format\r")
    f.write("3,9,=(A4),Output_format\r")
    LatestInfo["colJ"] = str(totalDaysLeft)
    # -------------------------------- Col K:K ----------------------------------
    f.write("0,10,ADDS,Equation_format\r")
    f.write("1,10,X/AVG,Equation_format\r")
    f.write("2,10,ADD,Regular_format\r")
    f.write("3,10,=0,Nuetral_format\r")
    LatestInfo["colK"] = 0
    # -------------------------------- Col L:L ----------------------------------
    f.write("0,11,#ADDS,Equation_format\r")
    f.write("1,11,ADD1 + ADD2...,Equation_format\r")
    f.write("2,11,ADDS,Regular_format\r")
    f.write("3,11,=1,Nuetral_format\r")
    LatestInfo["colL"] = 1
    # -------------------------------- Col M:M ----------------------------------
    f.write("0,12,TOTAL,Equation_format\r")
    f.write("1,12,X + ADD(N),Equation_format\r")
    f.write("2,12,Total,Regular_format\r")
    f.write("3,12,=(J4 + K4),Output_format\r")
    LatestInfo["colL"] = totalDaysLeft
    # -------------------------------- Col N:N ----------------------------------
    f.write("0,13,ETAC,Equation_format\r")
    f.write("1,13,TODAY + TOTAL,Equation_format\r")
    f.write("2,13,Esitmitade Time Of Complete,Regular_format\r")
    f.write("3,13,=(D4 + M4),N_Colmn_Format\r")
    LatestInfo["colN"] = StrToDate(FirstDate) + totalDaysLeft
    # -------------------------------- Col O:O ----------------------------------
    f.write("0,14,DAYS ADDED,Equation_format\r")
    f.write("1,14,ETAC[N] - ETAC[N-1],Equation_format\r")
    f.write("2,14,Days Extended/Shortend,Regular_format\r")
    f.write("3,14,=0,Nuetral_format\r")
    LatestInfo["colO"] = 0
    # -------------------------------- Col P:P ----------------------------------
    f.write("0,15,LE_YEAR,Equation_format\r")
    f.write("1,15,LE_YEAR,Equation_format\r")
    f.write("2,15,Last Episode Year,Regular_format\r")
    f.write("3,15," + oldestYear + ",Output_format\r")
    LatestInfo["colP"] = str(oldestYear)
    # -------------------------------- Col Q:Q ----------------------------------
    f.write("0,16,LE_PLACE,Equation_format\r")
    f.write("1,16,LE_PLACE,Equation_format\r")
    f.write("2,16,Last Episode Place,Regular_format\r")
    f.write("3,16,=0,Nuetral_format\r")
    LatestInfo["colQ"] = 0
    # -------------------------------- Col R:R ----------------------------------
    f.write("0,17,LE_Reached,Equation_format\r")
    f.write("1,17,LE_Reached,Equation_format\r")
    f.write("2,17,Last Episode Reached,Regular_format\r")
    f.write("3,17," + oldestEpisode + ",Input_format\r")
    LatestInfo["colR"] = str(oldestEpisode)
    # -------------------------------- Col S:S ----------------------------------
    f.write("0,18,EPISODE(ADV),Equation_format\r")
    f.write("1,18,EPISODE(ADV),Equation_format\r")
    f.write("2,18,# Episodes Advanced,Regular_format\r")
    f.write("3,18,=0,Nuetral_format\r")
    LatestInfo["colS"] = 0
    # -------------------------------- Col T:T ----------------------------------
    f.write("0,19,XEPISODE(ADV),Equation_format\r")
    f.write("1,19,EPDAY(AVG)[N - 1]*DAYS(PSSD)[N],Equation_format\r")
    f.write("2,19,Expected Episods Advancement,Regular_format\r")
    f.write("3,19,=0,Nuetral_format\r")
    LatestInfo["colT"] = 0
    # -------------------------------- Col U:U ----------------------------------
    f.write("0,20,E_WA,Equation_format\r")
    f.write("1,20,E_WA[N-1] + EPISODE(ADV),Equation_format\r")
    f.write("2,20,Episodes Watched,Regular_format\r")
    f.write("3,20,=0,Nuetral_format\r")
    LatestInfo["colU"] = 0
    # -------------------------------- Col V:V ----------------------------------
    f.write("0,21,EPDAY(AVG),Equation_format\r")
    f.write("1,21,E_WA/PDP,Equation_format\r")
    f.write("2,21,Episodes Per Day AVG,Regular_format\r")
    f.write("3,21,=0,Nuetral_format\r")
    LatestInfo["colV"] = 0
    # -------------------------------- Col W:W ----------------------------------
    f.write("0,22,ED_RATIO,Equation_format\r")
    f.write("1,22,#LDAYS(PSSD)/E_WA,Equation_format\r")
    f.write("2,22,Episode/Days Ratio,Regular_format\r")
    f.write("3,22,=0,Nuetral_format\r")
    LatestInfo["colW"] = 0
    # -------------------------------- Col X:X ----------------------------------
    f.write("0,23,EST_E_L,Equation_format\r")
    f.write("1,23,DAYS(RMN)/ED_RATIO,Equation_format\r")
    f.write("2,23,Estimated Episodes left,Regular_format\r")
    f.write("3,23,=0,Nuetral_format\r")
    LatestInfo["colX"] = 0
    # -------------------------------- Col Y:Y ----------------------------------
    f.write("0,24,#E_REACH_Q,Equation_format\r")
    f.write("1,24,(AVG/ED_RATIO) + 1,Equation_format\r")
    f.write("2,24,# Episodes To Reach Daily Quota,Regular_format\r")
    f.write("3,24,=0,Nuetral_format\r")
    LatestInfo["colY"] = 0
    f.close()
    LatestInfo["row"] = 4
    pickle.dump(LatestInfo, open("OldInfo.p", "wb"))


def turnRawFileIntoExcel():
    workbook = xlsxwriter.Workbook("Time Track 2.0.xlsx")
    sheet1 = workbook.add_worksheet()
    # ------------------------------------------Formats------------------------------------------------------------
    Equation_format = workbook.add_format(
        {'italic': True, 'font_color': '#959c97', 'align': 'center'})
    Regular_format = workbook.add_format(
        {'bold': True, 'align': 'center', 'border': 1})
    Input_format = workbook.add_format(
        {'font_color': '#3F3F76', 'align': 'center', 'border': 1, 'bg_color': '#FFCC99', 'border_color': '#7F7F7F'})
    Output_format = workbook.add_format(
        {'bold': True, 'font_color': '#3F3F3F', 'align': 'center', 'border': 1, 'bg_color': '#F2F2F2'})
    Nuetral_format = workbook.add_format(
        {'font_color': '#9C5700', 'align': 'center', 'border': 1, 'bg_color': '#FFEB9C', 'border_color': '#575163'})
    N_Colmn_Format = workbook.add_format(
        {'bold': True, 'font_color': '#3F3F3F', 'align': 'center', 'border': 1, 'bg_color': '#F2F2F2', 'num_format': 'd mmmm yyyy'})
    Good_Format = workbook.add_format(
        {'font_color': '#006100', 'align': 'center', 'border': 1, 'bg_color': '#C6EFCE'})
    Bad_Format = workbook.add_format(
        {'font_color': '#9C0006', 'align': 'center', 'border': 1, 'bg_color': '#FFC7CE'})
    # ------------------------------------------Set Colmn Width-----------------------------------------------------------
    sheet1.set_column('A:A', 20)  # 00
    sheet1.set_column('B:B', 13)  # 01
    sheet1.set_column('C:C', 24)  # 02
    sheet1.set_column('D:D', 27)  # 03
    sheet1.set_column('E:E', 33)  # 04
    sheet1.set_column('F:F', 27)  # 05
    sheet1.set_column('G:G', 19)  # 06
    sheet1.set_column('H:H', 34)  # 07
    sheet1.set_column('I:I', 18)  # 08
    sheet1.set_column('J:J', 28)  # 09
    sheet1.set_column('K:K', 15)  # 10
    sheet1.set_column('L:L', 15)  # 11
    sheet1.set_column('M:M', 13)  # 12
    sheet1.set_column('N:N', 31)  # 13
    sheet1.set_column('O:O', 23)  # 14
    sheet1.set_column('P:P', 19)  # 15
    sheet1.set_column('Q:Q', 16)  # 16
    sheet1.set_column('R:R', 17)  # 17
    sheet1.set_column('S:S', 30)  # 18
    sheet1.set_column('T:T', 20)  # 19
    sheet1.set_column('U:U', 33)  # 20
    sheet1.set_column('V:V', 27)  # 21
    sheet1.set_column('W:W', 21)  # 22
    sheet1.set_column('X:X', 20)  # 23
    sheet1.set_column('Y:Y', 22)  # 24

    directory = pathlib.Path().absolute()
    isExistsRawFile = os.path.exists(str(directory) + '\\raw.txt')
    if not(isExistsRawFile):
        intializeRawFile()
    f = open("raw.txt", "r")
    if f.mode == 'r':
        f1 = f.readlines()
        for x in f1:
            y = x.split(',')
            row = int(y[0])
            col = int(y[1])
            title = y[2]
            cellFormat = Regular_format
            if "Equation_format" in str(y[3]):
                cellFormat = Equation_format
            if "Regular_format" in str(y[3]):
                cellFormat = Regular_format
            if "Input_format" in str(y[3]):
                cellFormat = Input_format
            if "Output_format" in str(y[3]):
                cellFormat = Output_format
            if "Nuetral_format" in str(y[3]):
                cellFormat = Nuetral_format
            if "N_Colmn_Format" in str(y[3]):
                cellFormat = N_Colmn_Format
            if "Good_Format" in str(y[3]):
                cellFormat = Good_Format
            if "Bad_Format" in str(y[3]):
                cellFormat = Bad_Format
            sheet1.write(row, col, title, cellFormat)
    f.close()
    workbook.close()
    

def addNewEntryToTimeTrak(inputDateReached, inputLastEpisodePlace, inputLastEpisodeReached):
    LatestInfo = pickle.load( open( "OldInfo.p", "rb" ) ) 
    NewLatestInfo = {}
    today = date.today()
    todaysDate = today.strftime("%m/%d/%Y")
    todaysDate = StrToDate(todaysDate)
    rowNum = LatestInfo["row"]
    print("rowNum: " + str(rowNum))
    #------------------------------------------------------------------------------------
    OldA = LatestInfo["colA"]
    print("OldA: " + str(OldA))
    inputColBStr = inputDateReached
    print("inputColBStr: " + str(inputColBStr))
    inputColB = StrToDate(inputColBStr)
    #OldBStr = LatestInfo["colB"]
    #print("OldBStr: " + str(OldBStr))
    #OldB = StrToDate(OldBStr)
    OldDStr = LatestInfo["colD"]
    OldD = StrToDate(OldDStr)
    print("OldD: " + str(OldD))
    inputColC = todaysDate - OldD
    print("inputColC: " + str(inputColC))
    OldGStr = LatestInfo["colG"]
    OldG = RemoveEqualFromOldInfo(OldGStr)
    print("OldG: " + str(OldG))
    OldHStr = LatestInfo["colH"]
    OldH = RemoveEqualFromOldInfo(OldHStr)
    print("OldH: " + str(OldH))
    OldIStr = LatestInfo["colI"]
    OldI = RemoveEqualFromOldInfo(OldIStr)
    print("OldI: " + str(OldI))
    OldNStr = LatestInfo["colN"]
    OldN = RemoveEqualFromOldInfo(OldNStr)
    print("OldN: " + str(OldN))
    inputColQ = inputLastEpisodePlace
    OldQStr = LatestInfo["colQ"]
    OldQ = RemoveEqualFromOldInfo(OldQStr)
    print("OldQ: " + str(OldQ))
    inputColR = inputLastEpisodeReached
    OldUStr = LatestInfo["colU"]
    OldU = RemoveEqualFromOldInfo(OldUStr)
    print("OldU: " + str(OldU))
    OldYStr = LatestInfo["colY"]
    OldY = RemoveEqualFromOldInfo(OldYStr)
    print("OldY: " + str(OldY))
    # ---------------------------------------------
    colB = inputColB
    print("b: " + str(colB))
    colC = DaysLeftToInt(inputColC)
    print("c: " + str(colC))
    colD = OldD + timedelta(days=colC)
    print("d: " + str(colD))
    colA = colD - colB
    print("a: " + str(colA))
    tmpColA = str(colA)
    tmpColA = DaysLeftToInt(tmpColA)
    colE = int(tmpColA) - DaysLeftToInt(OldA)
    print("e: " + str(colE))
    colF = int(OldI) * colC
    colG = int(OldG) + int(colE)
    print("g: " + str(colG))
    colH = int(OldH) + colC
    print("h: " + str(colH))
    colI = colG / colH
    print("i: " + str(colI))
    colJ = colA / colI
    print("j: " + str(colJ))
    tmpColJ = DaysLeftToInt(colJ)
    print("tmpColJ: " + str(tmpColJ))
    colK = 0
    colL = 0
    while tmpColJ > 1:
        tmpColJ = tmpColJ/colI
        #print("tmpColJ: " + str(tmpColJ))
        colK += tmpColJ
        colL += 1
    colK += 1
    colM = DaysLeftToInt(colJ) + colK
    print("m: " + str(colM))
    colN = colD + timedelta(days=colM)
    print("n: " + str(colN))
    colO = colN - OldN
    print("o: " + str(colO))
    colP = colB
    colQ = inputColQ
    print("q: " + str(colQ))
    colR = inputColR
    colS = int(colQ) - int(OldQ)
    print("s: " + str(colS))
    colT = OldY * colC
    print("t: " + str(colT))
    colU = OldU + colS
    colV = colU / colH
    colW = colG / colU
    colX = colA / colW
    colY = (colI / colW) + 1
    #------------------------------------------------------------------------------------
    directory = pathlib.Path().absolute()
    isExistsRawFile = os.path.exists(str(directory) + '\\raw.txt')
    print('path: ' + str(directory)  + '\\raw.txt')
    print("isExistsRawFile: " + str(isExistsRawFile))
    if not(isExistsRawFile):
        intializeRawFile()
    f = open("raw.txt", "a+")
    # -------------------------------- Col A:A ---------------------------------- DAYS(RMN)
    f.write(str(rowNum) + ",0," + str(DaysLeftToInt(colA)) + " days,Output_format\r")
    print(str(rowNum) + ",0," + str(DaysLeftToInt(colA)) + ",Output_format\r")
    NewLatestInfo["colA"] = str(DaysLeftToInt(colA)) + " days"
    # -------------------------------- Col B:B ---------------------------------- DATE(RCHD)
    f.write(str(rowNum) + ",1," + str(DateFormatToListFormat(colB)) + ",Input_format\r")
    print(str(rowNum) + ",1," + str(DateFormatToListFormat(colB)) + ",Input_format\r")
    NewLatestInfo["colB"] = DateFormatToListFormat(colB)
    # -------------------------------- Col C:C ---------------------------------- DAYS(PSSD)
    f.write(str(rowNum) + ",2," + str(colC) + ",Input_format\r")
    print(str(rowNum) + ",2," + str(colC) + ",Input_format\r")
    NewLatestInfo["colC"] = colC
    # -------------------------------- Col D:D ---------------------------------- TODAY
    f.write(str(rowNum) + ",3," + str(DateFormatToListFormat(colD)) + ",Input_format\r")
    print(str(rowNum) + ",3," + str(DateFormatToListFormat(colD)) + ",Input_format\r")
    NewLatestInfo["colD"] = DateFormatToListFormat(colD)
    # -------------------------------- Col E:E ---------------------------------- DAYS(ADV)
    if colE > (colF - 1):
        f.write(str(rowNum) + ",4," + str(colE) + ",Good_Format\r")
        print(str(rowNum) + ",4," + str(colE) + ",Good_Format\r")
    else:
        f.write(str(rowNum) + ",4," + str(colE) + ",Bad_Format\r")
        print(str(rowNum) + ",4," + str(colE) + ",Bad_Format\r")
    NewLatestInfo["colE"] = colE
    # -------------------------------- Col F:F ---------------------------------- XDAYS(ADV)
    f.write(str(rowNum) + ",5," + str(colF) + ",Output_format\r")
    print(str(rowNum) + ",5," + str(colF) + ",Output_format\r")
    NewLatestInfo["colF"] = colF
    # -------------------------------- Col G:G ---------------------------------- #LDAYS(PSSD)
    f.write(str(rowNum) + ",6," + str(colG) + ",Output_format\r")
    NewLatestInfo["colG"] = colG
    # -------------------------------- Col H:H ---------------------------------- PDP
    f.write(str(rowNum) + ",7," + str(colH) + ",Output_format\r")
    NewLatestInfo["colH"] = colH
    # -------------------------------- Col I:I ---------------------------------- AVG
    f.write(str(rowNum) + ",8," + str(colI) + ",Output_format\r")
    NewLatestInfo["colI"] = colI
    # -------------------------------- Col J:J ---------------------------------- X
    f.write(str(rowNum) + ",9," + str(colJ) + ",Output_format\r")
    NewLatestInfo["colJ"] = colJ
    # -------------------------------- Col K:K ---------------------------------- ADDS
    f.write(str(rowNum) + ",10," + str(colK) + ",Output_format\r")
    NewLatestInfo["colK"] = colK
    # -------------------------------- Col L:L ---------------------------------- #ADDS
    f.write(str(rowNum) + ",11," + str(colL) + ",Output_format\r")
    NewLatestInfo["colL"] = colL
    # -------------------------------- Col M:M ---------------------------------- TOTAL
    f.write(str(rowNum) + ",12," + str(colM) + ",Output_format\r")
    NewLatestInfo["colM"] = colM
    # -------------------------------- Col N:N ---------------------------------- ETAC
    f.write(str(rowNum) + ",13," + str(colN) + ",Output_format\r")
    NewLatestInfo["colN"] = colN
    # -------------------------------- Col O:O ----------------------------------DAYS ADDED
    if DaysLeftToInt(colO) > 0:
        f.write(str(rowNum) + ",14," + str(colO) + ",Good_Format\r")
    else:
        f.write(str(rowNum) + ",14," + str(colO) + ",Bad_Format\r")
    NewLatestInfo["colO"] = colO
    # -------------------------------- Col P:P ---------------------------------- LE_YEAR
    f.write(str(rowNum) + ",15," + str(colP) + ",Output_format\r")
    NewLatestInfo["colP"] = colP
    # -------------------------------- Col Q:Q ---------------------------------- LE_PLACE
    f.write(str(rowNum) + ",16," + str(colQ) + ",Input_format\r")
    NewLatestInfo["colQ"] = colQ
    # -------------------------------- Col R:R ---------------------------------- LE_Reached
    f.write(str(rowNum) + ",17," + str(colR) + ",Input_format\r")
    NewLatestInfo["colR"] = colR
    # -------------------------------- Col S:S ---------------------------------- EPISODE(ADV)
    if colS > (int(colT) - 1):
        f.write(str(rowNum) + ",18," + str(colS) + ",Good_Format\r")
    else:
        f.write(str(rowNum) + ",18," + str(colS) + ",Bad_Format\r")
    NewLatestInfo["colS"] = colS
    # -------------------------------- Col T:T ---------------------------------- XEPISODE(ADV)
    f.write(str(rowNum) + ",19," + str(colT) + ",Output_format\r")
    NewLatestInfo["colT"] = colT
    # -------------------------------- Col U:U ---------------------------------- E_WA
    f.write(str(rowNum) + ",20," + str(colU) + ",Output_format\r")
    NewLatestInfo["colU"] = colU
    # -------------------------------- Col V:V ---------------------------------- EPDAY(AVG)
    f.write(str(rowNum) + ",21," + str(colV) + ",Output_format\r")
    NewLatestInfo["colV"] = colV
    # -------------------------------- Col W:W ---------------------------------- ED_RATIO
    f.write(str(rowNum) + ",22," + str(colW) + ",Output_format\r")
    NewLatestInfo["colW"] = colW
    # -------------------------------- Col X:X ---------------------------------- EST_E_L
    f.write(str(rowNum) + ",23," + str(colX) + ",Output_format\r")
    NewLatestInfo["colX"] = colX
    # -------------------------------- Col Y:Y ---------------------------------- #E_REACH_Q
    f.write(str(rowNum) + ",24," + str(colY) + ",Output_format\r")
    NewLatestInfo["colY"] = colY
    NewLatestInfo["row"] = rowNum + 1
    pickle.dump(NewLatestInfo, open("OldInfo.p", "wb"))
    f.close()
