import xlsxwriter
from ConversionFunctions import StrToDate, DateFormatToListFormat, DaysLeftToInt, cleanFileName, LinkToIMDBId, showStatus
from tkinter import messagebox
from imdb import IMDb
from datetime import datetime, date, timedelta
import csv
import os
import pathlib
import pickle
import shutil


def checkIfFolderExistAndCreate(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)


def checkIfContainsYear(show, YOF):
    checkIfFolderExistAndCreate("Local DB")
    with open(r"Local DB\\" + show, newline='') as csvfile:
        showReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in showReader:
            if str(YOF) in row[3]:
                return True
    return False


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
    checkIfFolderExistAndCreate("Watchlists")
    workbook = xlsxwriter.Workbook("Watchlists\\" + YOF + " Watchlist.xlsx")
    sheet1 = workbook.add_worksheet()
    sheet1.set_column('A:A', 25)  # 00
    sheet1.set_column('B:B', 7)  # 01
    sheet1.set_column('C:C', 8)  # 02
    sheet1.set_column('D:D', 47)  # 03
    sheet1.set_column('E:E', 11)  # 04
    sheet1.set_column('F:F', 6)  # 05
    sheet1.set_column('G:G', 11)  # 06
    sheet1.set_column('H:H', 11)  # 07
    sheet1.set_column('I:I', 13)  # 08
    sheet1.set_column('J:J', 12)  # 09
    sheet1.set_column('K:K', 77)  # 10
    Number_format = workbook.add_format(
        {'align': 'center', 'num_format': '0', 'border': 1})
    float_format = workbook.add_format(
        {'align': 'center', 'num_format': '0.00', 'border': 1})
    String_format = workbook.add_format({'align': 'center', 'border': 1})
    String_format_No_Align = workbook.add_format({'border': 1})
    Header_format = workbook.add_format(
        {'bold': True, 'align': 'center', 'border': 1, 'bg_color': '#C4BD97'})
    date_Format = workbook.add_format(
        {'align': 'center', 'num_format': 'd mmm yyyy', 'border': 1})
    sheet1.write(0, 0, 'Show', Header_format)
    sheet1.write(0, 1, 'Season', Header_format)
    sheet1.write(0, 2, 'Episode', Header_format)
    sheet1.write(0, 3, 'Title', Header_format)
    sheet1.write(0, 4, 'Air Date', Header_format)
    sheet1.write(0, 5, 'Rating', Header_format)
    sheet1.write(0, 6, 'Place In List', Header_format)
    sheet1.write(0, 7, 'Fixed Place', Header_format)
    sheet1.write(0, 8, 'Fixed Episode', Header_format)
    sheet1.write(0, 9, 'Fixed Season', Header_format)
    sheet1.write(0, 10, 'Name Sticker', Header_format)
    row = 1
    TotalNumberOfEpisodes = 0
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
                    sheet1.write(row, 0, Eshow, String_format_No_Align)
                    sheet1.write(row, 1, int(ESeason), Number_format)
                    sheet1.write(row, 2, int(Eepisode), Number_format)
                    sheet1.write(row, 3, str(ETitle), String_format_No_Align)
                    sheet1.write(row, 4, EAirdate, date_Format)
                    sheet1.write(row, 5, float(Erate), float_format)
                    sheet1.write(row, 6, 0, String_format)
                    sheet1.write(row, 7, str(
                        fixedPlaceEquation(row)), String_format)
                    sheet1.write(row, 8, str(
                        fixedSeasonAndEpisodeNumberEquation(row, 'B')), String_format)
                    sheet1.write(row, 9, str(
                        fixedSeasonAndEpisodeNumberEquation(row, 'C')), String_format)
                    sheet1.write(row, 10, str(
                        nameStickerEquation(row)), String_format_No_Align)
                    row = row + 1
            except:
                print('S W W')
    workbook.close()


def generatAllWatchlists():
    directory = pathlib.Path().absolute()
    today = date.today()
    ThisYear = today.year
    oldestYear = "1900"
    checkIfFolderExistAndCreate("Files")
    isExistsFile = os.path.exists(
        str(directory) + '\\Files\\First Episode Information.p')
    if not(isExistsFile):
        getDateOfFirstEpisodeInListFunc()
    Oldest_Dates = pickle.load(
        open("Files\\First Episode Information.p", "rb"))
    oldestYear = Oldest_Dates["year"]
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
    checkIfFolderExistAndCreate("Files")
    checkIfFolderExistAndCreate("Local DB")
    workbook = xlsxwriter.Workbook("Files\\Bad.xlsx")
    sheet1 = workbook.add_worksheet()
    sheet1.write(0, 0, "Show")
    sheet1.write(0, 1, "Season")
    sheet1.write(0, 2, "Episode")
    sheet1.write(0, 3, "Title")
    sheet1.write(0, 4, "Air Date")
    row = 1
    formatDate = workbook.add_format({'num_format': 'd mmm yyyy'})
    for filename in os.listdir(str(directory) + r"\\Local DB"):
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


def addShowClickedMed(Link):
    showToAdd = LinkToIMDBId(Link)
    return addShowClicked(showToAdd)


def addShowClicked(IMDBID):
    checkIfFolderExistAndCreate("Files")
    directory = pathlib.Path().absolute()
    ia = IMDb()
    series = ia.get_movie(IMDBID)
    ia.update(series, "episodes")
    kind = series["kind"]
    if not(kind == "tv series"):
        return "The Link enterd is not a TV Series"
    SeasonsArr = sorted(series["episodes"].keys())
    ShowTitle = series["title"]
    cleanTitle = cleanFileName(str(ShowTitle))
    status = showStatus(str(series["original title"]))
    isExistsShowLinkFile = os.path.exists(
        str(directory) + '\\Files\\Show Links.txt')
    if isExistsShowLinkFile:
        f = open("Files\\Show Links.txt", "a+")
    else:
        f = open("Files\\Show Links.txt", "w+")
    f.write(str(cleanTitle) + " : " + IMDBID + " : " + status + "\r")
    f.close()
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
                        EAirdate = "1 Jan. 2000"
                    if "May" in str(EAirdate) and not("May." in str(EAirdate)):
                        EAirdate = EAirdate.replace('May', 'May.')
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
                            [str(ESeason), str(Eepisode), "bad title encoding", str(EAirdate), str(Erate)])
            except:
                print("An exception occurred trying to extract an episode")
        print("Finished working on: " + cleanTitle)
        print("-----------------------------------------")
    return cleanTitle + " Added successfuly"


def getDateOfFirstEpisodeInListFunc():
    checkIfFolderExistAndCreate("Files")
    checkIfFolderExistAndCreate("Local DB")
    today = date.today()
    oldestDate = today.strftime("%m/%d/%Y")
    oldestDate = StrToDate(oldestDate)
    oldestYear = today.year
    oldestEpisode = ""
    directory = pathlib.Path().absolute()
    Oldest_Dates = {}
    for filename in os.listdir(str(directory) + r"\\Local DB"):
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
                        oldestYear = newYear
                    if Airdate < oldestDate:
                        oldestDate = Airdate
                        oldestEpisode = show + " " + \
                            str(ESeason) + str(Eepisode)
    Oldest_Dates["year"] = str(oldestYear)
    tmpDate = str(oldestDate)
    Oldest_Dates["date"] = tmpDate[0: len(tmpDate) - 9]
    Oldest_Dates["episode"] = str(oldestEpisode)
    pickle.dump(Oldest_Dates, open("Files\\First Episode Information.p", "wb"))


def refreshShowStatus():
    ia = IMDb()
    directory = pathlib.Path().absolute()
    checkIfFolderExistAndCreate("Files")
    checkIfFolderExistAndCreate("TmpFiles")
    original = str(directory) + r'\\Files\\Show Links.txt'
    target = str(directory) + r'\\TmpFiles\\Show Links.txt'
    shutil.copyfile(original, target)
    os.remove(str(directory) + r'\\Files\\Show Links.txt')
    f = open("TmpFiles\\Show Links.txt", "r")
    if f.mode == 'r':
        f1 = f.readlines()
        for x in f1:
            text = x.split(' : ')
            cleanTitle = text[0]
            showToAdd = text[1]
            series = ia.get_movie(showToAdd)
            ShowTitle = series["original title"]
            lastDig = ShowTitle[len(ShowTitle) - 3: len(ShowTitle) - 2]
            status = '?'
            if lastDig == '-':
                status = 'active'
            else:
                status = 'ended'
            f2 = open("Files\\Show Links.txt", "a+")
            f2.write(str(cleanTitle) + " : " +
                     showToAdd + " : " + status + "\r")
            f2.close()
    f.close()
    os.remove(str(directory) + r'\\TmpFiles\\Show Links.txt')


def refreshDB():
    directory = pathlib.Path().absolute()
    checkIfFolderExistAndCreate("Files")
    checkIfFolderExistAndCreate("TmpFiles")
    original = str(directory) + r'\\Files\\Show Links.txt'
    target = str(directory) + r'\\TmpFiles\\Show Links.txt'
    shutil.copyfile(original, target)
    os.remove(str(directory) + r'\\Files\\Show Links.txt')
    f = open("TmpFiles\\Show Links.txt", "r")
    if f.mode == 'r':
        f1 = f.readlines()
        for x in f1:
            text = x.split(' : ')
            showToAdd = text[1]
            status = text[2]
            if "active" in status:
                addShowClicked(showToAdd)
    f.close()
    os.remove(str(directory) + r'\\Files\\Show Links.txt')
    shutil.copyfile(target, original)
    os.remove(str(directory) + r'\\TmpFiles\\Show Links.txt')


def intializeRawFile():
    checkIfFolderExistAndCreate("Files")
    directory = pathlib.Path().absolute()
    isExistsFirstDateFile = os.path.exists(
        str(directory) + '\\Files\\First Episode Information.p')
    isExistsRawFile = os.path.exists(str(directory) + '\\Files\\raw.txt')
    if isExistsRawFile:
        messagebox.showinfo("Raw File Allready Exists")
    if not(isExistsFirstDateFile):
        getDateOfFirstEpisodeInListFunc()
    #Oldest_Dates = pickle.load(open("Files\\First Episode Information.p", "rb"))
    #oldestDate = Oldest_Dates["date"]
    #oldestYear = Oldest_Dates["year"]
    #oldestEpisode = Oldest_Dates["episode"]
    #initialDate = datetime.strptime(oldestDate, "%Y-%m-%d")
    #initialDateStr = initialDate.strftime("%m/%d/%Y")
    #today = date.today() + timedelta(days=-206)
    #FirstDate = today.strftime("%m/%d/%Y")
    #totalDaysLeft = StrToDate(FirstDate) - StrToDate(initialDateStr)
    LatestInfo = {}

    f = open("Files\\raw.txt", "w+")
    # -------------------------------- Col A:A ---------------------------------- C
    f.write("0,0,DAYS(RMN),EQU\r")
    f.write("1,0,TODAY - DATE(RCHD),EQU\r")
    f.write("2,0,Days Remaining,REG\r")
    f.write("3,0,8932,A\r")
    #f.write("3,0," + str(DaysLeftToInt(totalDaysLeft)) + ",A\r")
    #LatestInfo["colA"] = str(DaysLeftToInt(totalDaysLeft))
    LatestInfo["colA"] = "8932"
    # -------------------------------- Col B:B ---------------------------------- C
    f.write("0,1,DATE(RCHD),EQU\r")
    f.write("1,1,DATE(RCHD),EQU\r")
    f.write("2,1,Date Reached,REG\r")
    f.write("3,1,5/14/1995,NUEB\r")
    #f.write("3,1," + initialDateStr + ",B\r")
    # LatestInfo["colB"] = str(initialDateStr)
    LatestInfo["colB"] = "5/14/1995"
    # -------------------------------- Col C:C ----------------------------------
    f.write("0,2,DAYS(PSSD),EQU\r")
    f.write("1,2,DAYS(PSSD),EQU\r")
    f.write("2,2,Days Passed Since Last Log,REG\r")
    f.write("3,2,0,NUE\r")
    LatestInfo["colC"] = 0
    # -------------------------------- Col D:D ----------------------------------
    f.write("0,3,TODAY,EQU\r")
    f.write("1,3,(TODAY[N - 1]) + DAYS(PSSD),EQU\r")
    f.write("2,3,Today,REG\r")
    f.write("3,3,10/27/2019,D\r")
    #f.write("3,3," + str(FirstDate) + ",D\r")
    #LatestInfo["colD"] = str(FirstDate)
    LatestInfo["colD"] = "10/27/2019"
    # -------------------------------- Col E:E ----------------------------------
    f.write("0,4,DAYS(ADV),EQU\r")
    f.write("1,4,DAYS(RMN)[N] - DAYS(RMN)[N - 1],EQU\r")
    f.write("2,4,# Days Advanced,REG\r")
    f.write("3,4,0,NUE\r")
    LatestInfo["colE"] = 0
    # -------------------------------- Col F:F ----------------------------------
    f.write("0,5,XDAYS(ADV),EQU\r")
    f.write("1,5,AVG[N - 1]*DAYS(PSSD)[N],EQU\r")
    f.write("2,5,Expected Days Advancement,REG\r")
    f.write("3,5,0,A\r")
    LatestInfo["colF"] = 0
    # -------------------------------- Col G:G ----------------------------------
    f.write("0,6,#LDAYS(PSSD),EQU\r")
    f.write("1,6,SUM(DAYS(ADV)),EQU\r")
    f.write("2,6,# Of List Days Passed,REG\r")
    f.write("3,6,0,A\r")
    LatestInfo["colG"] = 0
    # -------------------------------- Col H:H ----------------------------------
    f.write("0,7,PDP,EQU\r")
    f.write("1,7,PDP[N] = PDP[N - 1] + DAYS(PSSD)[N],EQU\r")
    f.write("2,7,Phisical Days Passed,REG\r")
    f.write("3,7,0,A\r")
    LatestInfo["colH"] = 0
    # -------------------------------- Col I:I ----------------------------------
    f.write("0,8,AVG,EQU\r")
    f.write("1,8,#LDAYS(PSSD)/PDP,EQU\r")
    f.write("2,8,Average,REG\r")
    f.write("3,8,0,I\r")
    LatestInfo["colI"] = 0
    # -------------------------------- Col J:J ----------------------------------
    f.write("0,9,X,EQU\r")
    f.write("1,9,DAYS(RMN)/AVG,EQU\r")
    f.write("2,9,Days To Reach Current Date,REG\r")
    f.write("3,9,8932,I\r")
    LatestInfo["colJ"] = "8932"
    # f.write("3,9,=(A4),REGO\r")
    # LatestInfo["colJ"] = str(totalDaysLeft)
    # -------------------------------- Col K:K ----------------------------------
    f.write("0,10,ADDS,EQU\r")
    f.write("1,10,X/AVG,EQU\r")
    f.write("2,10,ADD,REG\r")
    f.write("3,10,0,I\r")
    LatestInfo["colK"] = 0
    # -------------------------------- Col L:L ----------------------------------
    f.write("0,11,#ADDS,EQU\r")
    f.write("1,11,ADD1 + ADD2...,EQU\r")
    f.write("2,11,ADDS,REG\r")
    f.write("3,11,1,A\r")
    LatestInfo["colL"] = 1
    # -------------------------------- Col M:M ----------------------------------
    f.write("0,12,TOTAL,EQU\r")
    f.write("1,12,X + ADD(N),EQU\r")
    f.write("2,12,Total,REG\r")
    f.write("3,12,=(J4 + K4),REGO\r")
    #LatestInfo["colL"] = totalDaysLeft
    LatestInfo["colL"] = "8933"
    # -------------------------------- Col N:N ----------------------------------
    f.write("0,13,ETAC,EQU\r")
    f.write("1,13,TODAY + TOTAL,EQU\r")
    f.write("2,13,Esitmitade Time Of Complete,REG\r")
    f.write("3,13,4/11/2044,N\r")
    #LatestInfo["colN"] = StrToDate(FirstDate) + totalDaysLeft
    LatestInfo["colN"] = "4/11/2044"
    # -------------------------------- Col O:O ----------------------------------
    f.write("0,14,DAYS ADDED,EQU\r")
    f.write("1,14,ETAC[N] - ETAC[N-1],EQU\r")
    f.write("2,14,Days Extended/Shortend,REG\r")
    f.write("3,14,0,NUE\r")
    LatestInfo["colO"] = 0
    # -------------------------------- Col P:P ----------------------------------
    f.write("0,15,LE_YEAR,EQU\r")
    f.write("1,15,LE_YEAR,EQU\r")
    f.write("2,15,Last Episode Year,REG\r")
    f.write("3,15,5/14/1995,P\r")
    #f.write("3,15," + oldestYear + ",P\r")
    # LatestInfo["colP"] = str(oldestYear)
    LatestInfo["colP"] = "1995"
    # -------------------------------- Col Q:Q ----------------------------------
    f.write("0,16,LE_PLACE,EQU\r")
    f.write("1,16,LE_PLACE,EQU\r")
    f.write("2,16,Last Episode Place,REG\r")
    f.write("3,16,112,C\r")
    LatestInfo["colQ"] = 112
    # f.write("3,16,0,C\r")
    # LatestInfo["colQ"] = 0
    # -------------------------------- Col R:R ----------------------------------
    f.write("0,17,LE_Reached,EQU\r")
    f.write("1,17,LE_Reached,EQU\r")
    f.write("2,17,Last Episode Reached,REG\r")
    f.write("3,17,DS9 323,R\r")
    LatestInfo["colR"] = "DS9 323"
    # f.write("3,17," + oldestEpisode + ",R\r")
    # LatestInfo["colR"] = str(oldestEpisode)
    # -------------------------------- Col S:S ----------------------------------
    f.write("0,18,EPISODE(ADV),EQU\r")
    f.write("1,18,EPISODE(ADV),EQU\r")
    f.write("2,18,# Episodes Advanced,REG\r")
    f.write("3,18,0,NUE\r")
    LatestInfo["colS"] = 0
    # -------------------------------- Col T:T ----------------------------------
    f.write("0,19,XEPISODE(ADV),EQU\r")
    f.write("1,19,EPDAY(AVG)[N - 1]*DAYS(PSSD)[N],EQU\r")
    f.write("2,19,Expected Episods Advancement,REG\r")
    f.write("3,19,0,A\r")
    LatestInfo["colT"] = 0
    # -------------------------------- Col U:U ----------------------------------
    f.write("0,20,E_WA,EQU\r")
    f.write("1,20,E_WA[N-1] + EPISODE(ADV),EQU\r")
    f.write("2,20,Episodes Watched,REG\r")
    f.write("3,20,0,A\r")
    LatestInfo["colU"] = 0
    # -------------------------------- Col V:V ----------------------------------
    f.write("0,21,EPDAY(AVG),EQU\r")
    f.write("1,21,E_WA/PDP,EQU\r")
    f.write("2,21,Episodes Per Day AVG,REG\r")
    f.write("3,21,0,I\r")
    LatestInfo["colV"] = 0
    # -------------------------------- Col W:W ----------------------------------
    f.write("0,22,ED_RATIO,EQU\r")
    f.write("1,22,#LDAYS(PSSD)/E_WA,EQU\r")
    f.write("2,22,Episode/Days Ratio,REG\r")
    f.write("3,22,0,W\r")
    LatestInfo["colW"] = 0
    # -------------------------------- Col X:X ----------------------------------
    f.write("0,23,EST_E_L,EQU\r")
    f.write("1,23,DAYS(RMN)/ED_RATIO,EQU\r")
    f.write("2,23,Estimated Episodes left,REG\r")
    f.write("3,23,0,A\r")
    LatestInfo["colX"] = 0
    # -------------------------------- Col Y:Y ----------------------------------
    f.write("0,24,#E_REACH_Q,EQU\r")
    f.write("1,24,(AVG/ED_RATIO) + 1,EQU\r")
    f.write("2,24,# Episodes To Reach Daily Quota,REG\r")
    f.write("3,24,0,Y\r")
    LatestInfo["colY"] = 0
    f.close()
    LatestInfo["row"] = 4
    pickle.dump(LatestInfo, open("Files\\OldInfo.p", "wb"))


def turnRawFileIntoExcel():
    checkIfFolderExistAndCreate("Files")
    workbook = xlsxwriter.Workbook("Files\\Time Track 2.0.xlsx")
    sheet1 = workbook.add_worksheet()
    # ------------------------------------------Formats------------------------------------------------------------
    formats = {}
    cell_A_Format = workbook.add_format(
        {'bold': True, 'font_color': '#3F3F3F', 'align': 'center', 'border': 1, 'bg_color': '#F2F2F2', 'num_format': '0'})
    formats["A"] = cell_A_Format
    cell_B_Format = workbook.add_format({'font_color': '#3F3F76', 'align': 'center', 'border': 1,
                                         'bg_color': '#FFCC99', 'border_color': '#7F7F7F', 'num_format': 'mmmm d, yyyy'})
    formats["B"] = cell_B_Format
    cell_C_Format = workbook.add_format({'font_color': '#3F3F76', 'align': 'center',
                                         'border': 1, 'bg_color': '#FFCC99', 'border_color': '#7F7F7F', 'num_format': '0'})
    formats["C"] = cell_C_Format
    cell_D_Format = workbook.add_format({'bold': True, 'font_color': '#3F3F3F', 'align': 'center',
                                         'border': 1, 'bg_color': '#F2F2F2', 'num_format': '[$-en-US]mmmm d, yyyy;@'})
    formats["D"] = cell_D_Format
    cell_E_Format_Good = workbook.add_format(
        {'font_color': '#006100', 'align': 'center', 'border': 1, 'bg_color': '#C6EFCE', 'num_format': '0'})
    formats["EG"] = cell_E_Format_Good
    cell_E_Format_Bad = workbook.add_format(
        {'font_color': '#9C0006', 'align': 'center', 'border': 1, 'bg_color': '#FFC7CE', 'num_format': '0'})
    formats["EB"] = cell_E_Format_Bad
    cell_I_Format = workbook.add_format({'bold': True, 'font_color': '#3F3F3F',
                                         'align': 'center', 'border': 1, 'bg_color': '#F2F2F2', 'num_format': '0.00'})
    formats["I"] = cell_I_Format
    cell_N_Format = workbook.add_format({'bold': True, 'font_color': '#3F3F3F', 'align': 'center',
                                         'border': 1, 'bg_color': '#F2F2F2', 'num_format': '[$-x-sysdate]dddd, mmmm dd, yyyy'})
    formats["N"] = cell_N_Format
    cell_O_Format_Good = workbook.add_format(
        {'font_color': '#006100', 'align': 'center', 'border': 1, 'bg_color': '#C6EFCE'})
    formats["OG"] = cell_O_Format_Good
    cell_O_Format_Bad = workbook.add_format(
        {'font_color': '#9C0006', 'align': 'center', 'border': 1, 'bg_color': '#FFC7CE'})
    formats["OB"] = cell_O_Format_Bad
    cell_P_Format = workbook.add_format({'bold': True, 'font_color': '#3F3F3F', 'align': 'center',
                                         'border': 1, 'bg_color': '#F2F2F2', 'num_format': '[$-en-US]mmmmm-yy'})
    formats["P"] = cell_P_Format
    cell_R_Format = workbook.add_format(
        {'font_color': '#3F3F76', 'align': 'center', 'border': 1, 'bg_color': '#FFCC99', 'border_color': '#7F7F7F'})
    formats["R"] = cell_R_Format
    cell_W_Format = workbook.add_format({'bold': True, 'font_color': '#3F3F3F',
                                         'align': 'center', 'border': 1, 'bg_color': '#F2F2F2', 'num_format': '0.000'})
    formats["W"] = cell_W_Format
    cell_Y_Format = workbook.add_format({'bold': True, 'font_color': '#3F3F3F',
                                         'align': 'center', 'border': 1, 'bg_color': '#F2F2F2', 'num_format': '0.0'})
    formats["Y"] = cell_Y_Format
    Equation_format = workbook.add_format(
        {'italic': True, 'font_color': '#959c97', 'align': 'center'})
    formats["EQU"] = Equation_format
    Regular_format = workbook.add_format(
        {'bold': True, 'align': 'center', 'border': 1})
    formats["REG"] = Regular_format
    Regular_format = workbook.add_format(
        {'bold': True, 'font_color': '#3F3F3F', 'align': 'center', 'border': 1, 'bg_color': '#F2F2F2'})
    formats["REGO"] = Regular_format
    Nuetral_format = workbook.add_format({'font_color': '#9C5700', 'align': 'center',
                                          'border': 1, 'bg_color': '#FFEB9C', 'border_color': '#575163', 'num_format': '0'})
    formats["NUE"] = Nuetral_format
    Nuetral_format_B = workbook.add_format({'font_color': '#9C5700', 'align': 'center', 'border': 1,
                                            'bg_color': '#FFEB9C', 'border_color': '#575163', 'num_format': '[$-en-US]mmmm d, yyyy;@'})
    formats["NUEB"] = Nuetral_format_B
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
    sheet1.set_column('S:S', 19)  # 18
    sheet1.set_column('T:T', 33)  # 19
    sheet1.set_column('U:U', 33)  # 20
    sheet1.set_column('V:V', 27)  # 21
    sheet1.set_column('W:W', 21)  # 22
    sheet1.set_column('X:X', 22)  # 23
    sheet1.set_column('Y:Y', 30)  # 24

    directory = pathlib.Path().absolute()
    isExistsRawFile = os.path.exists(str(directory) + '\\Files\\raw.txt')
    if not(isExistsRawFile):
        intializeRawFile()
    f = open("Files\\raw.txt", "r")
    if f.mode == 'r':
        f1 = f.readlines()
        for x in f1:
            y = x.split(',')
            row = int(y[0])
            col = int(y[1])
            title = y[2]
            format = str(y[3])
            format = format[0:len(format)-1]
            if (format == "A") or (format == "C") or (format == "EG") or (format == "EB") or (format == "NUE"):
                title = int(title)
            elif (format == "B") or (format == "D") or (format == "N") or (format == "P") or (format == "NUEB"):
                title = StrToDate(title)
            elif (format == "I") or (format == "W") or (format == "Y"):
                title = float(title)
            sheet1.write(row, col, title, formats[format])
    f.close()
    workbook.close()


def addNewEntryToTimeTrak(inputDateReached, inputLastEpisodePlace, inputLastEpisodeReached, DDR):
    checkIfFolderExistAndCreate("Files")
    LatestInfo = pickle.load(open("Files\\OldInfo.p", "rb"))
    NewLatestInfo = {}
    # today = date.today()
    # todaysDate = today.strftime("%m/%d/%Y")
    # todaysDate = StrToDate(todaysDate)
    todaysDate = DDR
    todaysDate = StrToDate(todaysDate)
    rowNum = LatestInfo["row"]
    # ------------------------------------------------------------------------------------
    OldA = LatestInfo["colA"]
    print("OldA: " + str(OldA))
    inputColBStr = inputDateReached
    print("inputColBStr: " + str(inputColBStr))
    inputColB = StrToDate(inputColBStr)
    OldDStr = LatestInfo["colD"]
    OldD = StrToDate(OldDStr)
    print("OldD: " + str(OldD))
    inputColC = todaysDate - OldD
    print("inputColC: " + str(inputColC))
    OldG = LatestInfo["colG"]
    print("OldG: " + str(OldG))
    OldH = LatestInfo["colH"]
    print("OldH: " + str(OldH))
    OldI = LatestInfo["colI"]
    print("OldI: " + str(OldI))
    OldNDate = StrToDate(LatestInfo["colN"])
    OldN = OldNDate.strftime("%m/%d/%Y")
    print("OldN: " + str(OldN))
    inputColQ = inputLastEpisodePlace
    OldQ = LatestInfo["colQ"]
    print("OldQ: " + str(OldQ))
    inputColR = inputLastEpisodeReached
    OldU = LatestInfo["colU"]
    print("OldU: " + str(OldU))
    OldY = LatestInfo["colY"]
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
    tempOldColA = 0
    if "day" in str(OldA):
        tempOldColA = DaysLeftToInt(OldA)
    else:
        tempOldColA = int(OldA)
    colE = tempOldColA - int(tmpColA)
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
        colK += tmpColJ
        colL += 1
    colK += 1
    colM = DaysLeftToInt(colJ) + colK
    print("m: " + str(colM))
    colNDate = colD + timedelta(days=colM)
    print("colNDate: " + str(colNDate))
    colN = colNDate.strftime("%m/%d/%Y")
    print("n: " + str(colN))
    colO = colNDate - StrToDate(OldN)
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
    # ------------------------------------------------------------------------------------
    directory = pathlib.Path().absolute()
    isExistsRawFile = os.path.exists(str(directory) + '\\Files\\raw.txt')
    print('path: ' + str(directory) + '\\Files\\raw.txt')
    print("isExistsRawFile: " + str(isExistsRawFile))
    if not(isExistsRawFile):
        intializeRawFile()
    f = open("Files\\raw.txt", "a+")
    # -------------------------------- Col A:A ---------------------------------- DAYS(RMN)
    f.write(str(rowNum) + ",0," + str(DaysLeftToInt(colA)) + ",A\r")
    print(str(rowNum) + ",0," + str(DaysLeftToInt(colA)) + ",A\r")
    NewLatestInfo["colA"] = str(DaysLeftToInt(colA))
    # -------------------------------- Col B:B ---------------------------------- DATE(RCHD)
    f.write(str(rowNum) + ",1," + DateFormatToListFormat(colB) + ",B\r")
    print(str(rowNum) + ",1," + str(DateFormatToListFormat(colB)) + ",B\r")
    NewLatestInfo["colB"] = DateFormatToListFormat(colB)
    # -------------------------------- Col C:C ---------------------------------- DAYS(PSSD)
    f.write(str(rowNum) + ",2," + str(colC) + ",C\r")
    print(str(rowNum) + ",2," + str(colC) + ",C\r")
    NewLatestInfo["colC"] = colC
    # -------------------------------- Col D:D ---------------------------------- TODAY
    f.write(str(rowNum) + ",3," + str(DateFormatToListFormat(colD)) + ",D\r")
    print(str(rowNum) + ",3," + str(DateFormatToListFormat(colD)) + ",D\r")
    NewLatestInfo["colD"] = DateFormatToListFormat(colD)
    # -------------------------------- Col E:E ---------------------------------- DAYS(ADV)
    if colE > (colF - 1):
        f.write(str(rowNum) + ",4," + str(colE) + ",EG\r")
        print(str(rowNum) + ",4," + str(colE) + ",EG\r")
    else:
        f.write(str(rowNum) + ",4," + str(colE) + ",EB\r")
        print(str(rowNum) + ",4," + str(colE) + ",EB\r")
    NewLatestInfo["colE"] = colE
    # -------------------------------- Col F:F ---------------------------------- XDAYS(ADV)
    f.write(str(rowNum) + ",5," + str(colF) + ",A\r")
    print(str(rowNum) + ",5," + str(colF) + ",A\r")
    NewLatestInfo["colF"] = colF
    # -------------------------------- Col G:G ---------------------------------- #LDAYS(PSSD)
    f.write(str(rowNum) + ",6," + str(colG) + ",A\r")
    print(str(rowNum) + ",6," + str(colG) + ",A\r")
    NewLatestInfo["colG"] = colG
    # -------------------------------- Col H:H ---------------------------------- PDP
    f.write(str(rowNum) + ",7," + str(colH) + ",A\r")
    NewLatestInfo["colH"] = colH
    # -------------------------------- Col I:I ---------------------------------- AVG
    f.write(str(rowNum) + ",8," + str(colI) + ",I\r")
    NewLatestInfo["colI"] = colI
    # -------------------------------- Col J:J ---------------------------------- X
    f.write(str(rowNum) + ",9," + str(DaysLeftToInt(colJ)) + ",I\r")
    NewLatestInfo["colJ"] = str(DaysLeftToInt(colJ))
    # -------------------------------- Col K:K ---------------------------------- ADDS
    f.write(str(rowNum) + ",10," + str(colK) + ",I\r")
    NewLatestInfo["colK"] = colK
    # -------------------------------- Col L:L ---------------------------------- #ADDS
    f.write(str(rowNum) + ",11," + str(colL) + ",A\r")
    NewLatestInfo["colL"] = colL
    # -------------------------------- Col M:M ---------------------------------- TOTAL
    f.write(str(rowNum) + ",12," + str(colM) + ",I\r")
    NewLatestInfo["colM"] = colM
    # -------------------------------- Col N:N ---------------------------------- ETAC
    f.write(str(rowNum) + ",13," + str(DateFormatToListFormat(colNDate)) + ",N\r")
    NewLatestInfo["colN"] = str(DateFormatToListFormat(colNDate))
    # -------------------------------- Col O:O ----------------------------------DAYS ADDED
    if DaysLeftToInt(colO) > 0:
        f.write(str(rowNum) + ",14," + str(DaysLeftToInt(colO)) + " days,OB\r")
    else:
        f.write(str(rowNum) + ",14," + str(DaysLeftToInt(colO)) + " days,OG\r")
    NewLatestInfo["colO"] = str(DaysLeftToInt(colO)) + " days"
    # -------------------------------- Col P:P ---------------------------------- LE_YEAR
    f.write(str(rowNum) + ",15," + str(DateFormatToListFormat(colP)) + ",P\r")
    NewLatestInfo["colP"] = str(DateFormatToListFormat(colP))
    # -------------------------------- Col Q:Q ---------------------------------- LE_PLACE
    f.write(str(rowNum) + ",16," + str(colQ) + ",C\r")
    NewLatestInfo["colQ"] = colQ
    # -------------------------------- Col R:R ---------------------------------- LE_Reached
    f.write(str(rowNum) + ",17," + str(colR) + ",R\r")
    NewLatestInfo["colR"] = colR
    # -------------------------------- Col S:S ---------------------------------- EPISODE(ADV)
    if colS > (int(colT) - 1):
        f.write(str(rowNum) + ",18," + str(colS) + ",EG\r")
    else:
        f.write(str(rowNum) + ",18," + str(colS) + ",EB\r")
    NewLatestInfo["colS"] = colS
    # -------------------------------- Col T:T ---------------------------------- XEPISODE(ADV)
    f.write(str(rowNum) + ",19," + str(int(colT)) + ",A\r")
    NewLatestInfo["colT"] = int(colT)
    # -------------------------------- Col U:U ---------------------------------- E_WA
    f.write(str(rowNum) + ",20," + str(colU) + ",A\r")
    NewLatestInfo["colU"] = colU
    # -------------------------------- Col V:V ---------------------------------- EPDAY(AVG)
    f.write(str(rowNum) + ",21," + str(colV) + ",I\r")
    NewLatestInfo["colV"] = colV
    # -------------------------------- Col W:W ---------------------------------- ED_RATIO
    f.write(str(rowNum) + ",22," + str(colW) + ",W\r")
    NewLatestInfo["colW"] = colW
    # -------------------------------- Col X:X ---------------------------------- EST_E_L
    f.write(str(rowNum) + ",23," + str(DaysLeftToInt(colX)) + ",A\r")
    NewLatestInfo["colX"] = str(DaysLeftToInt(colX))
    # -------------------------------- Col Y:Y ---------------------------------- #E_REACH_Q
    f.write(str(rowNum) + ",24," + str(colY) + ",Y\r")
    NewLatestInfo["colY"] = colY
    NewLatestInfo["row"] = rowNum + 1
    pickle.dump(NewLatestInfo, open("Files\\OldInfo.p", "wb"))
    f.close()
