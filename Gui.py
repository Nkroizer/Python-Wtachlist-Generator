from tkinter import Tk, messagebox, Frame, Label, LEFT, Entry, Button, Listbox, END, Menu
from WatchListFunctions import checkIfContainsYear, mainWatchlistGeneratorFunction, getBadDatesFunc, getDateOfFirstEpisodeInListFunc, generatAllWatchlists, addShowClickedMed, refreshShowStatus, refreshDB
from ConversionFunctions import cleanFileName
from imdb import IMDb
import csv
import pathlib
import os

window = Tk()

window.title("Watchlist Generator")

window.geometry('600x700')


def rClicker(e):
    try:
        def rClick_Copy(e, apnd=0):
            print("why?")
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


def addShowClick():
    link = showInput.get()
    cleanTitle = addShowClickedMed(link)
    messagebox.showinfo("info", cleanTitle)


def generatWatchlist():
    directory = pathlib.Path().absolute()
    shows = []
    year = yearInput.get()
    for filename in os.listdir(str(directory) + r"\Local DB"):
        if ".csv" in filename:
            if checkIfContainsYear(filename, year):
                shows.append(filename)
    mainWatchlistGeneratorFunction(shows, year, True)


def showAvilableShowsBtnFunc():
    directory = pathlib.Path().absolute()
    for filename in os.listdir(str(directory) + r"\Local DB"):
        if ".csv" in filename:
            showname = filename[0: len(filename) - 4]
            Lb1.insert(END, showname)


def refreshShowStatusFunc():
    refreshShowStatus()


def refreshDBFunc():
    refreshDB()


# Add show section
frame = Frame(window)
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
frame2 = Frame(window)
GenListYear = Label(frame2, text="Year: ")

yearInput = Entry(frame2, width=20)

yearInput.bind('<Button-3>', rClicker, add='')

yearGenBtn = Button(frame2, text="Generate", command=generatWatchlist, width=7)

GenListYear.pack(side=LEFT, padx=10, pady=7)
yearInput.pack(side=LEFT, padx=10, pady=7, anchor="w")
yearGenBtn.pack(side=LEFT, padx=10, pady=7)
frame2.pack()

# ----------------------------------------------------------------------------------

# MISC uttons section
frame3 = Frame(window)
BadDateGenBtn = Button(frame3, text="Get Bad Dates", command=getBadDatesFunc)

showAvilableShowsBtn = Button(
    frame3, text="Show Avilable Shows", command=showAvilableShowsBtnFunc)

FirstDateGenBtn = Button(frame3, text="Get First Dates",
                         command=getDateOfFirstEpisodeInListFunc)

GenerateAllWatchlistsBtn = Button(
    frame3, text="Generate All Watchlists", command=generatAllWatchlists)

BadDateGenBtn.pack(side=LEFT, padx=10, pady=7)
showAvilableShowsBtn.pack(side=LEFT, padx=10, pady=7)
FirstDateGenBtn.pack(side=LEFT, padx=10, pady=7)
GenerateAllWatchlistsBtn.pack(side=LEFT, padx=10, pady=7)
frame3.pack()

frame4 = Frame(window)
refreshShowStatusBtn = Button(
    frame4, text="Refresh Show Status", command=refreshShowStatusFunc)
refreshShowStatusBtn.pack(side=LEFT, padx=10, pady=7)

refreshDBBtn = Button(
    frame4, text="Refresh DB", command=refreshDBFunc)
refreshDBBtn.pack(side=LEFT, padx=10, pady=7)
frame4.pack()


# ----------------------------------------------------------------------------------

Lb1 = Listbox(window, width=70, height=25)
Lb1.pack()

window.mainloop()
