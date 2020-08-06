from datetime import datetime


def StrToDate(strDate):
    fixedDate = datetime.strptime(str(strDate), "%m/%d/%Y")
    return fixedDate


def DateFormatToListFormat(DateForm):
    ListForm = DateForm.strftime("%m/%d/%Y")
    return ListForm


def DateFormatToMySqlFormat(DateForm):
    fixedDate = datetime.strptime(str(DateForm), "%d %b. %Y")
    ListForm = fixedDate.strftime("%Y-%m-%d")
    return ListForm


def DaysLeftToInt(DL):
    strDl = str(DL)
    if "day" in strDl:
        NDL = strDl[0: strDl.find("day") - 1]
        return int(NDL)
    else:
        return 1


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


def LinkToIMDBId(link):
    IdPlace = link.find('title/tt')
    IMDBID = link[IdPlace + 8: IdPlace + 15]
    return IMDBID


def showStatus(showTitle):
    lastDig = showTitle[len(showTitle) - 3: len(showTitle) - 2]
    status = '?'
    if lastDig == '-':
        status = 'active'
    else:
        status = 'ended'
    return status


class ConversionFunctions:
    pass
