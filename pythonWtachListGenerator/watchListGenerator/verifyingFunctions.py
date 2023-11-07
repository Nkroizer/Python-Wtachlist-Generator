import csv
import os

class VerifyingFunctions:
    def check_if_folder_exist_and_create(self, folderName):
        if not os.path.exists(folderName):
            os.makedirs(folderName)


    def check_if_contains_year(self, show, YOF):
        self.check_if_folder_exist_and_create("/pythonWtachListGenerator/watchListGenerator/Local DB")
        with open(r"pythonWtachListGenerator/watchListGenerator/Local DB/" + show, newline='') as csvfile:
            showReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in showReader:
                if str(YOF) in row[3]:
                    return True
        return False