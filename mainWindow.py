from tkinter import Tk, Frame, Button, LEFT
import runpy
import pathlib


def openWtachlistGenerator():
    directory = pathlib.Path().absolute()
    runpy.run_path(str(directory) +
                   '/pythonWtachListGenerator/watchListGenerator.py')


def openDataAnalysis():
    directory = pathlib.Path().absolute()
    runpy.run_path(str(directory) + '/pythonWtachListGenerator/timeTrak.py')


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
