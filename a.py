# Reading an excel file using Python 
import xlrd 
  
# Give the location of the file 
loc = ("C:\\Users\\Quickode\\Desktop\\xyz\\Watchlists\\2002 Watchlist.xlsx") 
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
# For row 0 and column 0 
r = 0
true1 = True
while true1:
    for c in range(0, 11):
        try:
            a = sheet.cell_value(r, c)
        except:
            true1 = False
        print(a) 
    r += 1
