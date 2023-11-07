from tkinter import Frame, Label, LEFT, Entry, Button, Listbox, END, Menu,messagebox,StringVar,OptionMenu, Toplevel
import watchListGenerator.VerifyingFunctions as _VF
import watchListGenerator.WatchListFunctions as _WF
from datetime import datetime
from tkinter import Tk
import pathlib
import os
import csv

root = Tk()

root.title("Watchlist Generator")

root.geometry('600x700')


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
            r.bind_class(b, sequence='<Button-3>',func=rClicker, add='')
    except:
        print(' - rClickbinder, something wrong')
        pass


def addShowClick():
    link = showInput.get()
    cleanTitle = _WF.WatchListFunctions.add_show_clicked_med(link)
    messagebox.showinfo("info", cleanTitle)


def generatWatchlist():
    directory = pathlib.Path().absolute()
    shows = []
    year = variable.get()
    for filename in os.listdir(str(directory) + r"/pythonWtachListGenerator/watchListGenerator/Local DB"):
        if ".csv" in filename:
            if _VF.VerifyingFunctions.check_if_contains_year(filename, year):
                shows.append(filename)
    _WF.WatchListFunctions.main_watchlist_generator_function(shows, year, True)


def showAvilableShowsBtnFunc():
    directory = pathlib.Path().absolute()
    for filename in os.listdir(str(directory) + r"/pythonWtachListGenerator/watchListGenerator/Local DB"):
        if ".csv" in filename:
            showname = filename[0: len(filename) - 4]
            Lb1.insert(END, showname)


def getallYearsFunc():
    return _WF.WatchListFunctions.get_all_years()


def refreshShowStatusFunc():
    _WF.WatchListFunctions.refresh_show_status()


def refreshDBFuncActive():
    _WF.WatchListFunctions.refresh_db(True)


def refreshDBFuncAll():
    _WF.WatchListFunctions.refresh_db(False)


def getBadDatesFunc():
    _WF.WatchListFunctions.get_bad_dates()


def getDateOfFirstEpisodeInListFunc():
    _WF.WatchListFunctions.get_date_of_first_episode_in_list()


def generatAllWatchlistsFunc():
    _WF.WatchListFunctions.generat_all_watchlists()


def create_window(showName):
    window = Toplevel(root)
    window.title(showName)
    frame = Frame(window)
    with open("pythonWtachListGenerator\\watchListGenerator\\Local DB\\" + showName + ".csv", newline='') as csvfile:
        showCSV = csv.reader(csvfile, delimiter=' ', quotechar='|')
        Label(frame, text="Season", borderwidth=2, relief="ridge", width=15).grid(row=0, column=0)
        Label(frame, text="Episode", borderwidth=2, relief="ridge", width=15).grid(row=0, column=1)
        Label(frame, text="Title", borderwidth=2, relief="ridge", width=25).grid(row=0, column=2)
        Label(frame, text="Air Date", borderwidth=2, relief="ridge", width=15).grid(row=0, column=3)
        rowNumber = 1
        for cell in showCSV:
            ESeason = cell[0]
            if "unknown season" in ESeason:
                ESeason = 0
            Eepisode = cell[1]
            print(Eepisode)
            print(cell)
            ETitle = cell[2]
            EAirdate = cell[3]
            try:
                EAirdate = datetime.strptime(EAirdate, '%d %b. %Y')
            except:
                EAirdate = '2000-01-01 00:00:00'
            Label(frame, text=ESeason, borderwidth=2, relief="ridge", width=15).grid(row=rowNumber, column=0)
            Label(frame, text=Eepisode, borderwidth=2, relief="ridge", width=15).grid(row=rowNumber, column=1)
            Label(frame, text=ETitle, borderwidth=2, relief="ridge", width=25).grid(row=rowNumber, column=2)
            Label(frame, text=EAirdate, borderwidth=2, relief="ridge", width=15).grid(row=rowNumber, column=3)
            rowNumber += 1
    frame.pack()


def onselect(evt):
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    create_window(value)


# Add show section
frame = Frame(root)
addShowLbl = Label(frame, text="Add Show: ")

showInput = Entry(frame, width=53)

showInput.bind('<Button-3>', rClicker, add='')

addShowBtn = Button(frame, text="+ Add", command=addShowClick, width=7)

addShowLbl.pack(side=LEFT, padx=10, pady=7)
showInput.pack(side=LEFT, padx=10, pady=7, anchor="w")
addShowBtn.pack(side=LEFT, padx=10, pady=7)
frame.pack()

# ----------------------------------------------------------------------------------
# year watchist generator section
frame2 = Frame(root)
GenListYear = Label(frame2, text="Year: ")

OPTIONS = getallYearsFunc()

variable = StringVar(frame2)
variable.set(OPTIONS[0])  # default value

yearInput = OptionMenu(frame2, variable, OPTIONS[0], *OPTIONS)

yearGenBtn = Button(frame2, text="Generate", command=generatWatchlist, width=7)

GenListYear.pack(side=LEFT, padx=10, pady=7)
yearInput.pack(side=LEFT, padx=10, pady=7, anchor="w")
yearGenBtn.pack(side=LEFT, padx=10, pady=7)
frame2.pack()

# ----------------------------------------------------------------------------------

# MISC uttons section
frame3 = Frame(root)
BadDateGenBtn = Button(frame3, text="Get Bad Dates", command=getBadDatesFunc)

showAvilableShowsBtn = Button(frame3, text="Show Avilable Shows", command=showAvilableShowsBtnFunc)

FirstDateGenBtn = Button(frame3, text="Get First Dates", command=getDateOfFirstEpisodeInListFunc)

GenerateAllWatchlistsBtn = Button(frame3, text="Generate All Watchlists", command=generatAllWatchlistsFunc)

BadDateGenBtn.pack(side=LEFT, padx=10, pady=7)
showAvilableShowsBtn.pack(side=LEFT, padx=10, pady=7)
FirstDateGenBtn.pack(side=LEFT, padx=10, pady=7)
GenerateAllWatchlistsBtn.pack(side=LEFT, padx=10, pady=7)
frame3.pack()

frame4 = Frame(root)
refreshShowStatusBtn = Button(frame4, text="Refresh Show Status", command=refreshShowStatusFunc)


refreshDBBtn = Button(frame4, text="Refresh DB (Active)", command=refreshDBFuncActive)

refreshDBBtn = Button(frame4, text="Refresh DB (All)", command=refreshDBFuncAll)


refreshShowStatusBtn.pack(side=LEFT, padx=10, pady=7)
refreshDBBtn.pack(side=LEFT, padx=10, pady=7)
frame4.pack()


# ----------------------------------------------------------------------------------

Lb1 = Listbox(root, width=70, height=25)
Lb1.bind('<<ListboxSelect>>', onselect)
Lb1.pack()

root.mainloop()
