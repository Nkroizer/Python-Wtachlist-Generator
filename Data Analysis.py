from tkinter import Tk, messagebox, Frame, Label, LEFT, RIGHT, Entry, Button, Listbox, END, Menu
from WatchListFunctions import getDateOfFirstEpisodeInListFunc, intializeRawFile, turnRawFileIntoExcel, addNewEntryToTimeTrak

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


def addNewEntryToTimeTrakBridge():
    inputDateReached = inputDateReachedInput.get()
    inputLastEpisodePlace = inputLastEpisodePlaceInput.get()
    InputLastEpisodeReached = InputLastEpisodeReachedInput.get()
    addNewEntryToTimeTrak(inputDateReached, inputLastEpisodePlace, InputLastEpisodeReached)

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

# ----------------------------------------------------------------------------------

createNewFileBtn = Button(
    frame, text="Create New Raw File", command=intializeRawFile, width=18)

createNewFileBtn.pack(side=LEFT, padx=10, pady=7)

convertRawFileBtn = Button(
    frame2, text="Convert Raw File to Excel", command=turnRawFileIntoExcel, width=22)

convertRawFileBtn.pack(side=LEFT, padx=10, pady=7)

inputDateReachedLbl = Label(frame3, text="Current Date of episode reached (MM/DD/YYYY)")

inputDateReachedLbl.pack(side=LEFT, padx=10, pady=7)

inputDateReachedInput = Entry(frame3, width=53)

inputDateReachedInput.pack(side=LEFT, padx=10, pady=7, anchor="w")

inputDateReachedInput.bind('<Button-3>', rClicker, add='')


inputLastEpisodePlaceLbl = Label(frame4, text="Last Episode Place")

inputLastEpisodePlaceLbl.pack(side=LEFT, padx=10, pady=7)

inputLastEpisodePlaceInput = Entry(frame4, width=53)

inputLastEpisodePlaceInput.pack(side=LEFT, padx=10, pady=7, anchor="w")

inputLastEpisodePlaceInput.bind('<Button-3>', rClicker, add='')


inputLastEpisodeReachedLbl = Label(frame5, text="Last Episode Reached")

inputLastEpisodeReachedLbl.pack(side=LEFT, padx=10, pady=7)

InputLastEpisodeReachedInput = Entry(frame5, width=53)

InputLastEpisodeReachedInput.pack(side=RIGHT, padx=10, pady=7, anchor="w")

InputLastEpisodeReachedInput.bind('<Button-3>', rClicker, add='')

convertRawFileBtn = Button(
    frame6, text="Add TimeTrak Line", command=addNewEntryToTimeTrakBridge, width=22)

convertRawFileBtn.pack(side=LEFT, padx=10, pady=7)



window.mainloop()
