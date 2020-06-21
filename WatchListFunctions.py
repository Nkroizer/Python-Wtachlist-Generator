from ConversionFunctions import StrToDate, cleanFileName, LinkToIMDBId, showStatus
from VerifyingFunctions import checkIfFolderExistAndCreate, checkIfContainsYear
from EquationCreator import fixedPlaceEquation, fixedSeasonAndEpisodeNumberEquation, nameStickerEquation
from tkinter import messagebox, Tk, HORIZONTAL, mainloop, Button
from tkinter.ttk import Progressbar
from imdb import IMDb
from datetime import datetime, date
import xlsxwriter
import csv
import os
import pathlib
import pickle
import shutil


def mainWatchlistGeneratorFunction(showsToAdd, YOF, showMessage):
    root = Tk() 
    root.wm_attributes("-topmost", 1)
    root.geometry('100x30')
    progress = Progressbar(root, orient = HORIZONTAL, 
    length = 100, mode = 'determinate') 
    progress.pack(pady = 10)
    root.update()

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
    TotalNumberOfItemsToWork = len(showsToAdd)
    currentProgress = 0
    progressPart = 100/TotalNumberOfItemsToWork
    for show in showsToAdd:
        print("Started working on: " + show)
        with open("Local DB/" + show, newline='') as csvfile:
            showCSV = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for cell in showCSV:
                Eshow = cleanFileName(show[0: len(show) - 4])
                ESeason = cell[0]
                if "unknown season" in ESeason:
                    ESeason = 0
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
        currentProgress += progressPart
        progress['value'] = currentProgress
        root.update_idletasks() 
    root.destroy()
    workbook.close()


def generatAllWatchlists():
    root = Tk() 
    root.wm_attributes("-topmost", 1)
    root.geometry('100x30')
    progress = Progressbar(root, orient = HORIZONTAL, 
    length = 100, mode = 'determinate') 
    progress.pack(pady = 10)
    root.update()
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
    TotalNumberOfItemsToWork = ThisYear - year
    currentProgress = 0
    progressPart = 100/TotalNumberOfItemsToWork
    for x in range(year, ThisYear):
        shows = []
        for filename in os.listdir(str(directory) + r"\Local DB"):
            if ".csv" in filename:
                if checkIfContainsYear(filename, str(x)):
                    shows.append(filename)
        mainWatchlistGeneratorFunction(shows, str(x), False)
        currentProgress += progressPart
        progress['value'] = currentProgress
        root.update_idletasks() 
    root.destroy()


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


def getallYears():
    today = date.today()
    ThisYear = int(today.year)
    years = []
    directory = pathlib.Path().absolute()
    firstYear = "1900"
    checkIfFolderExistAndCreate("Files")
    isExistsFile = os.path.exists(
        str(directory) + '\\Files\\First Episode Information.p')
    if not(isExistsFile):
        getDateOfFirstEpisodeInListFunc()
    Oldest_Dates = pickle.load(
        open("Files\\First Episode Information.p", "rb"))
    firstYear = int(Oldest_Dates["year"])
    for x in range(firstYear, ThisYear):
        years.append(x)
    return years        


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


def refreshDB(active):
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
            if active and "active" in status:
                addShowClicked(showToAdd)
    f.close()
    os.remove(str(directory) + r'\\Files\\Show Links.txt')
    shutil.copyfile(target, original)
    os.remove(str(directory) + r'\\TmpFiles\\Show Links.txt')