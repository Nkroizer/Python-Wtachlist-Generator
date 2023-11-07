from datetime import datetime

class ConversionFunctions:
    def string_to_date(self, strDate):
        fixedDate = datetime.strptime(str(strDate), "%m/%d/%Y")
        return fixedDate


    def date_format_to_list_format(self, DateForm):
        ListForm = DateForm.strftime("%m/%d/%Y")
        return ListForm


    def date_format_to_mySql_format(self, DateForm):
        fixedDate = datetime.strptime(str(DateForm), "%d %b. %Y")
        ListForm = fixedDate.strftime("%Y-%m-%d")
        return ListForm


    def days_left_to_int(self, DL):
        strDl = str(DL)
        if "day" in strDl:
            NDL = strDl[0: strDl.find("day") - 1]
            return int(NDL)
        else:
            return 1


    def clean_file_name(self, fileName):
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


    def link_to_imdb_id(self, link):
        IdPlace = link.find('title/tt')
        IMDBID = link[IdPlace + 8: IdPlace + 15]
        return IMDBID


    def show_status(self, showTitle):
        lastDig = showTitle[len(showTitle) - 3: len(showTitle) - 2]
        status = '?'
        if lastDig == '-':
            status = 'active'
        else:
            status = 'ended'
        return status