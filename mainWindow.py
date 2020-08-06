from tkinter import Tk, Frame, Button, LEFT


def openWtachlistGenerator():
    exec(open('pythonWtachListGenerator/watchListGenerator.py').read())


def openDataAnalysis():
    exec(open('pythonWtachListGenerator/timeTrak2.0.py').read())


window = Tk()

window.title("Main Window")

window.geometry('350x150')

frame = Frame(window)

WtachlistGeneratorBtn = Button(
    frame, text="Watchlist Generator", command=openWtachlistGenerator, width=15)

DataAnalysisBtn = Button(frame, text="Data Analysis",
                         command=openDataAnalysis, width=15)

WtachlistGeneratorBtn.pack(side=LEFT, padx=10, pady=30)
DataAnalysisBtn.pack(side=LEFT, padx=10, pady=30)
frame.pack()

window.mainloop()
