import xlsxwriter
from tkinter import messagebox
from imdb import IMDb
from datetime import datetime, date
import csv
import os
import pathlib

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
    isExistsFile = os.path.exists(str(directory) + 'First Episode Information.txt')
    if not(isExistsFile):
        getDateOfFirstEpisodeInListFunc()
    f=open("First Episode Information.txt", "r")
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
                        sheet1.write(row, 0, str(filename))
                        sheet1.write(row, 1, ESeason)
                        sheet1.write(row, 2, Eepisode)
                        sheet1.write(row, 3, str(ETitle))
                        sheet1.write(row, 4, EAirdate, formatDate)
                        row = row + 1
    workbook.close()
    messagebox.showinfo("info", "Bad Dates List was Generated Successfuly")


def getDateOfFirstEpisodeInListFunc():
    today = date.today()
    oldestDate = today.strftime("%m/%d/%Y")
    oldestDate = datetime.strptime(oldestDate, "%m/%d/%Y")
    oldestYear = today.year
    print("new oldest date: " + str(oldestDate))
    print("new oldest year: " + str(oldestYear))
    directory = pathlib.Path().absolute()
    f=open("First Episode Information.txt","w+")
    for filename in os.listdir(str(directory) + r"\Local DB"):
        if ".csv" in filename:
            with open(r"Local DB\\" + filename, newline='') as csvfile:
                showReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for cell in showReader:
                    EAirdate = cell[3]
                    try:
                        EAirdate = datetime.strptime(EAirdate, "%d %b %Y")
                    except:
                        EAirdate = datetime.strptime(EAirdate, "%d %b. %Y")
                    Airdate = EAirdate.strftime("%m/%d/%Y")
                    Airdate = datetime.strptime(Airdate, "%m/%d/%Y")
                    newYear = Airdate.year
                    if newYear < oldestYear:
                        print (str(oldestYear) + " ---> " + str(newYear))
                        oldestYear = newYear
                    if Airdate < oldestDate:
                        oldestDate = Airdate
                        print("new oldest date: " + str(oldestDate))
    f.write("oldest year: " + str(oldestYear) + "\r")
    f.write("oldest date: " + str(oldestDate))
    f.close()


def intializeRawFile():
    directory = pathlib.Path().absolute()
    isExistsFirstDateFile = os.path.exists(str(directory) + 'First Episode Information.txt')
    isExistsRawFile = os.path.exists(str(directory) + 'raw.txt')
    if isExistsRawFile:
        messagebox.showinfo("Raw File Allready Exists")
    if not(isExistsFirstDateFile):
        getDateOfFirstEpisodeInListFunc()
    f=open("First Episode Information.txt", "r")
    if f.mode == 'r':
        f1 = f.readlines()
        for x in f1:
            if "oldest date" in x:
                l1 = x.split()
                oldestDate = l1[2]
    f.close()
    initialDate = datetime.strptime(oldestDate, "%Y-%m-%d")
    initialDateStr = initialDate.strftime("%m/%d/%Y")
    today = date.today()
    FirstDate = today.strftime("%m/%d/%Y")
    f=open("raw.txt","w+")
    #-------------------------------- Col A:A ---------------------------------- C
    f.write("0,0,DAYS(RMN),Equation_format\r")
    f.write("1,0,TODAY - DATE(RCHD),Equation_format\r")
    f.write("2,0,Days Remaining,Regular_format\r")
    f.write("3,0,'=(D-B)',Output_format")
    #-------------------------------- Col B:B ---------------------------------- C
    f.write("0,1,DATE(RCHD),Equation_format\r")
    f.write("1,1,DATE(RCHD),Equation_format\r")
    f.write("2,1,Date Reached,Regular_format\r")
    f.write("3,1," + initialDateStr + ",Input_format")
    #-------------------------------- Col C:C ----------------------------------
    f.write("0,2,DAYS(PSSD),Equation_format\r")
    f.write("1,2,DAYS(PSSD),Equation_format\r")
    f.write("2,2,Days Passed Since Last Log,Regular_format\r")
    f.write("3,2,0,Nuetral_format")
    #-------------------------------- Col D:D ----------------------------------
    f.write("0,3,TODAY,Equation_format\r")
    f.write("1,3,(TODAY[N - 1]) + DAYS(PSSD),Equation_format\r")
    f.write("2,3,Today,Regular_format\r")
    f.write("3,3," + str(FirstDate) + ",Nuetral_format")
    #-------------------------------- Col E:E ----------------------------------
    f.write("0,4,DAYS(ADV),Equation_format\r")
    f.write("1,4,DAYS(RMN)[N] - DAYS(RMN)[N - 1],Equation_format\r")
    f.write("2,4,# Days Advanced,Regular_format\r")
    f.write("3,4,0,Nuetral_format")
    #-------------------------------- Col F:F ----------------------------------
    f.write("0,5,XDAYS(ADV),Equation_format\r")
    f.write("1,5,AVG[N - 1]*DAYS(PSSD)[N],Equation_format\r")
    f.write("2,5,Expected Days Advancement,Regular_format\r")
    f.write("3,5,0,Nuetral_format")
    #-------------------------------- Col G:G ----------------------------------
    f.write("0,6,#LDAYS(PSSD),Equation_format\r")
    f.write("1,6,SUM(DAYS(ADV)),Equation_format\r")
    f.write("2,6,# Of List Days Passed,Regular_format\r")
    f.write("3,6,0,Nuetral_format")
    #-------------------------------- Col H:H ----------------------------------
    f.write("0,7,PDP,Equation_format\r")
    f.write("1,7,PDP[N] = PDP[N - 1] + DAYS(PSSD)[N],Equation_format\r")
    f.write("2,7,Phisical Days Passed,Regular_format\r")
    f.write("3,7,0,Nuetral_format")
    #-------------------------------- Col I:I ----------------------------------
    f.write("0,8,AVG,Equation_format\r")
    f.write("1,8,#LDAYS(PSSD)/PDP,Equation_format\r")
    f.write("2,8,Average,Regular_format\r")
    f.write("3,8,0,Nuetral_format")
    #-------------------------------- Col J:J ----------------------------------
    f.write("0,9,X,Equation_format\r")
    f.write("1,9,DAYS(RMN)/AVG,Equation_format\r")
    f.write("2,9,Days To Reach Current Date,Regular_format\r")
    f.write("3,9,(need equation),Output_format")
    #-------------------------------- Col K:K ----------------------------------
    f.write("0,10,ADD1,Equation_format\r")
    f.write("1,10,X/AVG,Equation_format\r")
    f.write("2,10,ADD1,Regular_format\r")
    f.write("3,10,0,Nuetral_format")
    #-------------------------------- Col L:L ----------------------------------
    f.write("0,11,ADD2,Equation_format\r")
    f.write("1,11,ADD1/AVG,Equation_format\r")
    f.write("2,11,ADD2,Regular_format\r")
    f.write("3,11,0,Nuetral_format")
    #-------------------------------- Col M:M ----------------------------------
    f.write("0,12,TOTAL,Equation_format\r")
    f.write("1,12,X + ADD(N),Equation_format\r")
    f.write("2,12,Total,Regular_format\r")
    f.write("3,12,(need equation),Output_format")
    #-------------------------------- Col N:N ----------------------------------
    f.write("0,13,ETAC,Equation_format\r")
    f.write("1,13,TODAY + TOTAL,Equation_format\r")
    f.write("2,13,Esitmitade Time Of Complete,Regular_format\r")
    f.write("3,13,(need equation),Output_format")
    #-------------------------------- Col O:O ----------------------------------
    f.write("0,14,DAYS ADDED,Equation_format\r")
    f.write("1,14,ETAC[N] - ETAC[N-1],Equation_format\r")
    f.write("2,14,Days Extended/Shortend,Regular_format\r")
    f.write("3,14,0,Nuetral_format")
    #-------------------------------- Col P:P ----------------------------------
    f.write("0,15,ADD FLAG,Equation_format\r")
    f.write("1,15,IF(ADD(N) > AVG),Equation_format\r")
    f.write("2,15,ADD(N) > AVG,Regular_format\r")
    f.write("3,15,False,Nuetral_format")
    #-------------------------------- Col Q:Q ----------------------------------
    f.write("0,16,ADD DIFF,Equation_format\r")
    f.write("1,16,AVG - ADD(N),Equation_format\r")
    f.write("2,16,Diff AVG & ADD(N),Regular_format\r")
    f.write("3,16,0,Nuetral_format")
    #-------------------------------- Col R:R ----------------------------------
    f.write("0,17,LE_YEAR,Equation_format\r")
    f.write("1,17,LE_YEAR,Equation_format\r")
    f.write("2,17,Last Episode Year,Regular_format\r")
    f.write("3,17,---,Output_format")
    #-------------------------------- Col S:S ----------------------------------
    f.write("0,18,LE_PLACE,Equation_format\r")
    f.write("1,18,LE_PLACE,Equation_format\r")
    f.write("2,18,Last Episode Place,Regular_format\r")
    f.write("3,18,---,Input_format")
    #------------------------------------------------------------------
    f.write("0,19,LE_Reached,Equation_format\r")
    f.write("1,19,LE_Reached,Equation_format\r")
    f.write("2,19,Last Episode Reached,Regular_format\r")
    f.write("3,19,---,Input_format")
    #------------------------------------------------------------------
    f.write("0,20,EPISODE(ADV),Equation_format\r")
    f.write("1,20,EPISODE(ADV),Equation_format\r")
    f.write("2,20,# Episodes Advanced,Regular_format\r")
    f.write("3,20,0,Nuetral_format")
    #------------------------------------------------------------------
    f.write("0,21,XEPISODE(ADV),Equation_format\r")
    f.write("1,21,EPDAY(AVG)[N - 1]*DAYS(PSSD)[N],Equation_format\r")
    f.write("2,21,Expected Episods Advancement,Regular_format\r")
    f.write("3,21,0,Nuetral_format")
    #------------------------------------------------------------------
    f.write("0,22,E_WA,Equation_format\r")
    f.write("1,22,E_WA[N-1] + EPISODE(ADV),Equation_format\r")
    f.write("2,22,Episodes Watched,Regular_format\r")
    f.write("3,22,0,Nuetral_format")
    #------------------------------------------------------------------
    f.write("0,23,EPDAY(AVG),Equation_format\r")
    f.write("1,23,E_WA/PDP,Equation_format\r")
    f.write("2,23,Episodes Per Day AVG,Regular_format\r")
    f.write("3,23,0,Nuetral_format")
    #------------------------------------------------------------------
    f.write("0,24,ED_RATIO,Equation_format\r")
    f.write("1,24,#LDAYS(PSSD)/E_WA,Equation_format\r")
    f.write("2,24,Episode/Days Ratio,Regular_format\r")
    f.write("3,24,0,Nuetral_format")
    #------------------------------------------------------------------
    f.write("0,25,EST_E_L,Equation_format\r")
    f.write("1,25,DAYS(RMN)/ED_RATIO,Equation_format\r")
    f.write("2,25,Estimated Episodes left,Regular_format\r")
    f.write("3,25,---,Output_format")
    #------------------------------------------------------------------
    f.write("0,26,#E_REACH_Q,Equation_format\r")
    f.write("1,26,(AVG/ED_RATIO) + 1,Equation_format\r")
    f.write("2,26,# Episodes To Reach Daily Quota,Regular_format\r")
    f.write("3,26,0,Nuetral_format")
    f.close() 


def turnRawFileIntoExcel():
    workbook = xlsxwriter.Workbook("Time Track 2.0.xlsx")
    sheet1 = workbook.add_worksheet()
    #------------------------------------------Formats------------------------------------------------------------
    Equation_format = workbook.add_format({'italic': True, 'font_color': '#959c97', 'align': 'center'})
    Regular_format = workbook.add_format({'bold': True, 'align': 'center', 'border': 1})
    Input_format = workbook.add_format({'font_color': '#3F3F76', 'align': 'center', 'border': 1, 'bg_color': '#FFCC99', 'border_color': '#7F7F7F'})
    Output_format = workbook.add_format({'bold': True, 'font_color': '#3F3F3F', 'align': 'center', 'border': 1, 'bg_color': '#F2F2F2'})
    Nuetral_format = workbook.add_format({'font_color': '#9C5700', 'align': 'center', 'border': 1, 'bg_color': '#FFEB9C', 'border_color': '#575163'})
    #------------------------------------------Set Colmn Width-----------------------------------------------------------
    sheet1.set_column('A:A', 20) #00
    sheet1.set_column('B:B', 13) #01
    sheet1.set_column('C:C', 24) #02
    sheet1.set_column('D:D', 27) #03
    sheet1.set_column('E:E', 33) #04
    sheet1.set_column('F:F', 27) #05
    sheet1.set_column('G:G', 19) #06
    sheet1.set_column('H:H', 34) #07
    sheet1.set_column('I:I', 18) #08
    sheet1.set_column('J:J', 28) #09
    sheet1.set_column('K:K', 15) #10
    sheet1.set_column('L:L', 15) #11
    sheet1.set_column('M:M', 13) #12
    sheet1.set_column('N:N', 31) #13
    sheet1.set_column('O:O', 23) #14
    sheet1.set_column('P:P', 18) #15
    sheet1.set_column('Q:Q', 19) #16
    sheet1.set_column('R:R', 16) #17
    sheet1.set_column('S:S', 17) #18
    sheet1.set_column('T:T', 30) #19
    sheet1.set_column('U:U', 20) #20
    sheet1.set_column('V:V', 33) #21
    sheet1.set_column('W:W', 27) #22
    sheet1.set_column('X:X', 21) #23
    sheet1.set_column('Y:Y', 20) #24
    sheet1.set_column('Z:Z', 22) #25
    sheet1.set_column('AA:AA', 31) #26
    f=open("raw.txt", "r")
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
            sheet1.write(row, col, title, cellFormat)
    f.close() 
    workbook.close()