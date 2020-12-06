import os
import csv


def checkIfFolderExistAndCreate(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)


def checkIfContainsYear(show, YOF):
    checkIfFolderExistAndCreate("/pythonWtachListGenerator/watchListGenerator/Local DB")
    with open(r"pythonWtachListGenerator/watchListGenerator/Local DB/" + show, newline='') as csvfile:
        showReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in showReader:
            if str(YOF) in row[3]:
                return True
    return False


class VerifyingFunctions:
    pass
