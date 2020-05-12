from tkinter import Tk, messagebox, Frame, Label, LEFT, Entry, Button, Listbox, END, Menu
from WatchListFunctions import extractIMDBIdFromLink, cleanFileName, checkIfContainsYear, mainWatchlistGeneratorFunction, getBadDatesFunc, getDateOfFirstEpisodeInListFunc, generatAllWatchlists
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


def addShowClicked():
    link = showInput.get()
    showToAdd = extractIMDBIdFromLink(link)
    ia = IMDb()
    series = ia.get_movie(showToAdd)
    ia.update(series, "episodes")
    SeasonsArr = sorted(series["episodes"].keys())
    ShowTitle = series["title"]
    cleanTitle = cleanFileName(str(ShowTitle))
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
                        print("E: " + str(EAirdate))
                        EAirdate = "1 Jan. 2000"
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
                            [str(ESeason), str(Eepisode), "bad tite encoding", str(EAirdate), str(Erate)])
            except:
                print("An exception occurred trying to extract an episode")
        print("Finished working on: " + cleanTitle)
        print("-----------------------------------------")
    messagebox.showinfo("info", cleanTitle + " Added successfuly")


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


# Add show section
frame = Frame(window)
frame.pack()

# year watchist generator section
frame2 = Frame(window)
frame2.pack()

# MISC uttons section
frame3 = Frame(window)
frame3.pack()


addShowLbl = Label(frame, text="Add Show: ")

addShowLbl.pack(side=LEFT, padx=10, pady=7)

showInput = Entry(frame, width=53)

showInput.pack(side=LEFT, padx=10, pady=7, anchor="w")

showInput.bind('<Button-3>', rClicker, add='')

addShowBtn = Button(frame, text="+ Add", command=addShowClicked, width=7)

addShowBtn.pack(side=LEFT, padx=10, pady=7)

# ----------------------------------------------------------------------------------

GenListYear = Label(frame2, text="Year: ")

GenListYear.pack(side=LEFT, padx=10, pady=7)

yearInput = Entry(frame2, width=20)

yearInput.pack(side=LEFT, padx=10, pady=7, anchor="w")

yearInput.bind('<Button-3>', rClicker, add='')

yearGenBtn = Button(frame2, text="Generate", command=generatWatchlist, width=7)

yearGenBtn.pack(side=LEFT, padx=10, pady=7)

# ----------------------------------------------------------------------------------

BadDateGenBtn = Button(frame3, text="Get Bad Dates", command=getBadDatesFunc)

BadDateGenBtn.pack(side=LEFT, padx=10, pady=7)

# ----------------------------------------------------------------------------------

showAvilableShowsBtn = Button(
    frame3, text="Show Avilable Shows", command=showAvilableShowsBtnFunc)

showAvilableShowsBtn.pack(side=LEFT, padx=10, pady=7)

# ----------------------------------------------------------------------------------

FirstDateGenBtn = Button(frame3, text="Get first Dates",
                         command=getDateOfFirstEpisodeInListFunc)

FirstDateGenBtn.pack(side=LEFT, padx=10, pady=7)

# ----------------------------------------------------------------------------------

GenerateAllWatchlistsBtn = Button(
    frame3, text="Generate All watchlists", command=generatAllWatchlists)

GenerateAllWatchlistsBtn.pack(side=LEFT, padx=10, pady=7)

# ----------------------------------------------------------------------------------

Lb1 = Listbox(window, width=70, height=35)
Lb1.pack()

window.mainloop()
