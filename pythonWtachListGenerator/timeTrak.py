from helpers import _DAF,_CF,_pickle,Tk,Menu,Frame,date,Button,Label,Entry,RIGHT,LEFT,Checkbutton,IntVar,Calendar

window = Tk()

window.title("Data Analysis")

window.geometry('700x800')


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
            r.bind_class(b, sequence='<Button-3>', func=rClicker, add='')
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
    _DAF.DataAnalysisFunctions.addNewEntryToTimeTrak(inputDateReached, inputLastEpisodePlace, InputLastEpisodeReached, DDR)


def intializeRawFileFunc():
    _DAF.DataAnalysisFunctions.intializeRawFile()


def turnRawFileIntoExcelFunc():
    _DAF.DataAnalysisFunctions.turnRawFileIntoExcel()


# Add show section

LatestInfo = _pickle.load(open("pythonWtachListGenerator\\watchListGenerator\\Files\\OldInfo.p", "rb"))
lastDateReached = LatestInfo["colB"]
LDR = _CF.ConversionFunctions.StrToDate(lastDateReached)

lastTodaysDate = LatestInfo["colD"]
LTD = _CF.ConversionFunctions.StrToDate(lastTodaysDate)

# ----------------------------------------------------------------------------------

frame = Frame(window)

createNewFileBtn = Button(frame, text="Create New Raw File", command=intializeRawFileFunc, width=18)

createNewFileBtn.pack(side=LEFT, padx=7, pady=7)

frame.pack()

# ----------------------------------------------------------------------------------

frame2 = Frame(window)

convertRawFileBtn = Button(frame2, text="Convert Raw File to Excel", command=turnRawFileIntoExcelFunc, width=22)

convertRawFileBtn.pack(side=LEFT, padx=10, pady=7)

frame2.pack()

# ----------------------------------------------------------------------------------

frame3 = Frame(window)

inputDateReachedLbl = Label(frame3, text="Current Date of episode reached")

calDateReached = Calendar(frame3, font="Arial 14", selectmode='day', locale='en_US', cursor="hand1", year=LDR.year, month=LDR.month, day=LDR.day)

inputDateReachedLbl.pack(side=LEFT, padx=10, pady=7)

calDateReached.pack()

frame3.pack()

# ----------------------------------------------------------------------------------

frame4 = Frame(window)

DDLbl = Label(frame4, text="Date Date Reached")

calDateToday = Calendar(frame4, font="Arial 14", selectmode='day', locale='en_US', cursor="hand1", year=LTD.year, month=LTD.month, day=LTD.day)

CheckVar1 = IntVar()

C1 = Checkbutton(frame4, text="Today", variable=CheckVar1, onvalue=1, offvalue=0)

DDLbl.pack(side=LEFT, padx=45, pady=30)

calDateToday.pack(pady=30)

C1.pack()

frame4.pack()

# ----------------------------------------------------------------------------------

frame5 = Frame(window)

inputLastEpisodePlaceLbl = Label(frame5, text="Last Episode Place")

inputLastEpisodePlaceInput = Entry(frame5, width=53)

inputLastEpisodePlaceInput.bind('<Button-3>', rClicker, add='')

inputLastEpisodePlaceLbl.pack(side=LEFT, padx=10, pady=7)

inputLastEpisodePlaceInput.pack(side=LEFT, padx=30, pady=7, anchor="w")

frame5.pack()

# ----------------------------------------------------------------------------------

frame6 = Frame(window)

inputLastEpisodeReachedLbl = Label(frame6, text="Last Episode Reached")

InputLastEpisodeReachedInput = Entry(frame6, width=53)

InputLastEpisodeReachedInput.bind('<Button-3>', rClicker, add='')

inputLastEpisodeReachedLbl.pack(side=LEFT, padx=3, pady=7)

InputLastEpisodeReachedInput.pack(side=RIGHT, padx=30, pady=7, anchor="w")

frame6.pack()

# ----------------------------------------------------------------------------------

frame7 = Frame(window)

convertRawFileBtn = Button(frame7, text="Add TimeTrak Line", command=addNewEntryToTimeTrakBridge, width=22)

convertRawFileBtn.pack(side=LEFT, padx=10, pady=7)

frame7.pack()

# ----------------------------------------------------------------------------------
window.mainloop()
