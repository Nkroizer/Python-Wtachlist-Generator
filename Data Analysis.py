from tkinter import Tk, messagebox, Frame, Label, LEFT, RIGHT, Entry, Button, Listbox, END, Menu, Checkbutton, IntVar, ttk
from WatchListFunctions import getDateOfFirstEpisodeInListFunc, intializeRawFile, turnRawFileIntoExcel, addNewEntryToTimeTrak
from ConversionFunctions import StrToDate
from datetime import date
from tkcalendar import Calendar
import pickle

window = Tk()

window.title("Watchlist Generator")

window.geometry('600x700')


def rClicker(e):
    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()

        nclst = [
            (' Cut', lambda e=e: rClick_Cut(e)),
            (' Copy', lambda e=e: rClick_Copy(e)),
            (' Paste', lambda e=e: rClick_Paste(e)),
        ]

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10, entry="0")
    except:
        print(' - rClick menu, something wrong')
        pass

    return "break"


def rClickbinder(r):
    try:
        for b in ['Text', 'Entry', 'Listbox', 'Label']:
            r.bind_class(b, sequence='<Button-3>',
                         func=rClicker, add='')
    except:
        print(' - rClickbinder, something wrong')
        pass


def addNewEntryToTimeTrakBridge():
    inputDateReachedTMP = calDateReached.selection_get()
    inputDateReached = inputDateReachedTMP.strftime("%m/%d/%Y")
    inputLastEpisodePlace = inputLastEpisodePlaceInput.get()
    InputLastEpisodeReached = InputLastEpisodeReachedInput.get()
    DDRTMP = calDateToday.selection_get()
    TodaysFlag = CheckVar1.get()
    if TodaysFlag == 1:
        DDRTMP = date.today()
    DDR = DDRTMP.strftime("%m/%d/%Y")
    addNewEntryToTimeTrak(inputDateReached, inputLastEpisodePlace, InputLastEpisodeReached, DDR)

# Add show section
frame = Frame(window)
frame.pack()

frame2 = Frame(window)
frame2.pack()

frame3 = Frame(window)
frame3.pack()

frame4 = Frame(window)
frame4.pack()

frame5 = Frame(window)
frame5.pack()

frame6 = Frame(window)
frame6.pack()

frame7 = Frame(window)
frame7.pack()

LatestInfo = pickle.load(open("Files\\OldInfo.p", "rb"))
lastDateReached = LatestInfo["colB"]
LDR = StrToDate(lastDateReached)

lastTodaysDate = LatestInfo["colD"]
LTD = StrToDate(lastTodaysDate)

# ----------------------------------------------------------------------------------

createNewFileBtn = Button(frame, text="Create New Raw File", command=intializeRawFile, width=18)

createNewFileBtn.pack(side=LEFT, padx=10, pady=7)

# ----------------------------------------------------------------------------------

convertRawFileBtn = Button(frame2, text="Convert Raw File to Excel", command=turnRawFileIntoExcel, width=22)

convertRawFileBtn.pack(side=LEFT, padx=10, pady=7)

# ----------------------------------------------------------------------------------

inputDateReachedLbl = Label(frame3, text="Current Date of episode reached")

calDateReached = Calendar(frame3, font="Arial 14", selectmode='day', locale='en_US',
                cursor="hand1", year=LDR.year, month=LDR.month, day=LDR.day)

inputDateReachedLbl.pack(side=LEFT, padx=10, pady=7)
calDateReached.pack()

# ----------------------------------------------------------------------------------

DDLbl = Label(frame4, text="Date Date Reached")

calDateToday = Calendar(frame4, font="Arial 14", selectmode='day', locale='en_US',
                cursor="hand1", year=LTD.year, month=LTD.month, day=LTD.day)

CheckVar1 = IntVar()

C1 = Checkbutton(frame4, text = "Today", variable = CheckVar1, onvalue = 1, offvalue = 0)

DDLbl.pack(side=LEFT, padx=10, pady=7)
calDateToday.pack()
C1.pack()

# ----------------------------------------------------------------------------------


inputLastEpisodePlaceLbl = Label(frame5, text="Last Episode Place")

inputLastEpisodePlaceLbl.pack(side=LEFT, padx=10, pady=7)

inputLastEpisodePlaceInput = Entry(frame5, width=53)

inputLastEpisodePlaceInput.pack(side=LEFT, padx=10, pady=7, anchor="w")

inputLastEpisodePlaceInput.bind('<Button-3>', rClicker, add='')

# ----------------------------------------------------------------------------------

inputLastEpisodeReachedLbl = Label(frame6, text="Last Episode Reached")

inputLastEpisodeReachedLbl.pack(side=LEFT, padx=10, pady=7)

InputLastEpisodeReachedInput = Entry(frame6, width=53)

InputLastEpisodeReachedInput.pack(side=RIGHT, padx=10, pady=7, anchor="w")

InputLastEpisodeReachedInput.bind('<Button-3>', rClicker, add='')

# ----------------------------------------------------------------------------------

convertRawFileBtn = Button(frame7, text="Add TimeTrak Line", command=addNewEntryToTimeTrakBridge, width=22)

convertRawFileBtn.pack(side=LEFT, padx=10, pady=7)

# ----------------------------------------------------------------------------------
window.mainloop()
