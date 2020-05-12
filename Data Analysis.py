from tkinter import Tk, messagebox, Frame, Label, LEFT, Entry, Button, Listbox, END, Menu
from WatchListFunctions import getDateOfFirstEpisodeInListFunc, intializeRawFile, turnRawFileIntoExcel

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


# Add show section
frame = Frame(window)
frame.pack()

frame2 = Frame(window)
frame2.pack()

frame3 = Frame(window)
frame3.pack()

# ----------------------------------------------------------------------------------

createNewFileBtn = Button(
    frame, text="Create New Raw File", command=intializeRawFile, width=18)

createNewFileBtn.pack(side=LEFT, padx=10, pady=7)

addShowLbl = Label(frame2, text="Current Date of episode reached (MM/DD/YYYY)")

addShowLbl.pack(side=LEFT, padx=10, pady=7)

showInput = Entry(frame2, width=53)

showInput.pack(side=LEFT, padx=10, pady=7, anchor="w")

showInput.bind('<Button-3>', rClicker, add='')

convertRawFileBtn = Button(
    frame3, text="Convert Raw File to Excel", command=turnRawFileIntoExcel, width=22)

convertRawFileBtn.pack(side=LEFT, padx=10, pady=7)

# f=open("raw.txt", "a+")
# for i in range(2):
#     f.write("Appended line %d\r" % (i+1))
#     f.close()

window.mainloop()
