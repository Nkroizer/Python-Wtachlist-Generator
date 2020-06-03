import csv
import os
import pathlib

directory = pathlib.Path().absolute()
for filename in os.listdir(str(directory) + r"\Local DB2"):
    if ".csv" in filename:
        with open(r"Local DB2\\" + filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row[0])
